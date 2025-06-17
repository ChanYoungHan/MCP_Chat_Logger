"""
RabbitMQ 메시지 발행 모듈

이 모듈은 채팅 로그를 RabbitMQ 큐로 발행하는 기능을 제공합니다.
환경변수를 통해 RabbitMQ 연결 설정을 관리합니다.
"""

import os
import json
import logging
from typing import Dict, Any, Optional
from datetime import datetime
import pika
from pika.exceptions import AMQPConnectionError, AMQPChannelError

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RabbitMQPublisher:
    """RabbitMQ 메시지 발행을 담당하는 클래스"""
    
    def __init__(self):
        """환경변수에서 RabbitMQ 설정을 로드하고 초기화"""
        self.host = os.getenv('RABBITMQ_HOST', 'localhost')
        self.port = int(os.getenv('RABBITMQ_PORT', '5672'))
        self.username = os.getenv('RABBITMQ_USERNAME', 'guest')
        self.password = os.getenv('RABBITMQ_PASSWORD', 'guest')
        self.virtual_host = os.getenv('RABBITMQ_VIRTUAL_HOST', '/')
        self.exchange = os.getenv('RABBITMQ_EXCHANGE', 'llmLogger')
        self.routing_key = os.getenv('RABBITMQ_ROUTING_KEY', 'llm_logger')
        self.queue_name = os.getenv('RABBITMQ_QUEUE_NAME', 'llm_logger')
        
        # 연결 설정
        self.connection_timeout = int(os.getenv('RABBITMQ_CONNECTION_TIMEOUT', '30'))
        self.heartbeat = int(os.getenv('RABBITMQ_HEARTBEAT', '600'))
        self.blocked_connection_timeout = int(os.getenv('RABBITMQ_BLOCKED_CONNECTION_TIMEOUT', '300'))
        
        self.connection = None
        self.channel = None
        
        logger.info(f"RabbitMQ Publisher 초기화됨 - Host: {self.host}:{self.port}, Exchange: {self.exchange}")
    
    def _create_connection(self) -> bool:
        """RabbitMQ 연결을 생성하고 설정"""
        try:
            credentials = pika.PlainCredentials(self.username, self.password)
            parameters = pika.ConnectionParameters(
                host=self.host,
                port=self.port,
                virtual_host=self.virtual_host,
                credentials=credentials,
                connection_attempts=3,
                retry_delay=2,
                socket_timeout=self.connection_timeout,
                heartbeat=self.heartbeat,
                blocked_connection_timeout=self.blocked_connection_timeout
            )
            
            self.connection = pika.BlockingConnection(parameters)
            self.channel = self.connection.channel()
            
            # Exchange 선언 (존재하지 않으면 생성)
            self.channel.exchange_declare(
                exchange=self.exchange,
                exchange_type='direct',
                durable=True
            )
            
            # Queue 선언 (존재하지 않으면 생성)
            self.channel.queue_declare(
                queue=self.queue_name,
                durable=True
            )
            
            # Queue를 Exchange에 바인딩
            self.channel.queue_bind(
                exchange=self.exchange,
                queue=self.queue_name,
                routing_key=self.routing_key
            )
            
            logger.info("RabbitMQ 연결 및 설정 완료")
            return True
            
        except AMQPConnectionError as e:
            logger.error(f"RabbitMQ 연결 실패: {e}")
            return False
        except Exception as e:
            logger.error(f"RabbitMQ 설정 중 예상치 못한 오류: {e}")
            return False
    
    def _close_connection(self):
        """RabbitMQ 연결 종료"""
        try:
            if self.channel and not self.channel.is_closed:
                self.channel.close()
            if self.connection and not self.connection.is_closed:
                self.connection.close()
            logger.info("RabbitMQ 연결 종료됨")
        except Exception as e:
            logger.error(f"RabbitMQ 연결 종료 중 오류: {e}")
    
    def publish_chat_log(self, 
                        messages: list, 
                        conversation_id: Optional[str] = None,
                        additional_metadata: Optional[Dict[str, Any]] = None) -> bool:
        """
        채팅 로그를 RabbitMQ로 발행
        
        Args:
            messages: 채팅 메시지 리스트
            conversation_id: 대화 ID (선택사항)
            additional_metadata: 추가 메타데이터 (선택사항)
            
        Returns:
            bool: 발행 성공 여부
        """
        try:
            # 연결이 없거나 닫혀있다면 새로 생성
            if not self.connection or self.connection.is_closed:
                if not self._create_connection():
                    return False
            
            # 메시지 페이로드 구성
            payload = {
                "timestamp": datetime.now().isoformat(),
                "conversation_id": conversation_id,
                "messages": messages,
                "metadata": additional_metadata or {}
            }
            
            # JSON으로 직렬화
            message_body = json.dumps(payload, ensure_ascii=False, indent=2)
            
            # 메시지 발행
            self.channel.basic_publish(
                exchange=self.exchange,
                routing_key=self.routing_key,
                body=message_body.encode('utf-8'),
                properties=pika.BasicProperties(
                    delivery_mode=2,  # 메시지 영속성
                    content_type='application/json',
                    content_encoding='utf-8',
                    timestamp=int(datetime.now().timestamp())
                )
            )
            
            logger.info(f"채팅 로그 발행 성공 - Conversation ID: {conversation_id}, 메시지 수: {len(messages)}")
            return True
            
        except AMQPChannelError as e:
            logger.error(f"RabbitMQ 채널 오류: {e}")
            # 채널 오류시 연결 재설정 시도
            self._close_connection()
            return False
        except Exception as e:
            logger.error(f"메시지 발행 중 오류: {e}")
            return False
    
    def test_connection(self) -> bool:
        """
        RabbitMQ 연결 테스트
        
        Returns:
            bool: 연결 테스트 성공 여부
        """
        try:
            if self._create_connection():
                self._close_connection()
                logger.info("RabbitMQ 연결 테스트 성공")
                return True
            else:
                logger.error("RabbitMQ 연결 테스트 실패")
                return False
        except Exception as e:
            logger.error(f"연결 테스트 중 오류: {e}")
            return False
    
    def __enter__(self):
        """컨텍스트 매니저 진입"""
        self._create_connection()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """컨텍스트 매니저 종료"""
        self._close_connection()


# 글로벌 퍼블리셔 인스턴스
_publisher_instance = None


def get_publisher() -> RabbitMQPublisher:
    """
    싱글톤 패턴으로 RabbitMQ 퍼블리셔 인스턴스 반환
    
    Returns:
        RabbitMQPublisher: 퍼블리셔 인스턴스
    """
    global _publisher_instance
    if _publisher_instance is None:
        _publisher_instance = RabbitMQPublisher()
    return _publisher_instance


def publish_chat_message(messages: list, 
                        conversation_id: Optional[str] = None,
                        additional_metadata: Optional[Dict[str, Any]] = None) -> bool:
    """
    편의 함수: 채팅 메시지를 RabbitMQ로 발행
    
    Args:
        messages: 채팅 메시지 리스트
        conversation_id: 대화 ID (선택사항)
        additional_metadata: 추가 메타데이터 (선택사항)
        
    Returns:
        bool: 발행 성공 여부
    """
    publisher = get_publisher()
    return publisher.publish_chat_log(messages, conversation_id, additional_metadata)
