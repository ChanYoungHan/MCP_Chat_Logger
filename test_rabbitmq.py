#!/usr/bin/env python3
"""
RabbitMQ 설정 및 테스트 유틸리티

이 스크립트는 RabbitMQ 연결을 테스트하고 필요한 Exchange, Queue를 설정합니다.
"""

import os
import sys
from dotenv import load_dotenv
from rabbitmq_publisher import RabbitMQPublisher

def main():
    """메인 함수"""
    print("🐰 RabbitMQ 설정 및 테스트 유틸리티")
    print("=" * 50)
    
    # 환경변수 로드
    load_dotenv()
    
    # RabbitMQ 설정 표시
    publisher = RabbitMQPublisher()
    print(f"""
📋 현재 RabbitMQ 설정:
- Host: {publisher.host}:{publisher.port}
- Virtual Host: {publisher.virtual_host}
- Username: {publisher.username}
- Exchange: {publisher.exchange}
- Routing Key: {publisher.routing_key}
- Queue Name: {publisher.queue_name}
    """)
    
    # 연결 테스트
    print("🔍 RabbitMQ 연결 테스트 중...")
    if publisher.test_connection():
        print("✅ RabbitMQ 연결 테스트 성공!")
        
        # 테스트 메시지 발행
        print("\n📤 테스트 메시지 발행 중...")
        test_messages = [
            {
                "role": "user",
                "content": "이것은 테스트 메시지입니다."
            },
            {
                "role": "assistant", 
                "content": "네, 테스트 메시지를 잘 받았습니다!"
            }
        ]
        
        if publisher.publish_chat_log(
            messages=test_messages,
            conversation_id="test_conversation",
            additional_metadata={"test": True, "utility_script": True}
        ):
            print("✅ 테스트 메시지 발행 성공!")
            print("🎉 모든 테스트가 완료되었습니다!")
        else:
            print("❌ 테스트 메시지 발행 실패")
            sys.exit(1)
            
    else:
        print("❌ RabbitMQ 연결 테스트 실패")
        print("\n🔧 다음 사항을 확인해주세요:")
        print("1. RabbitMQ 서버가 실행 중인지 확인")
        print("2. .env 파일의 설정이 올바른지 확인")
        print("3. 네트워크 연결 상태 확인")
        print("4. 방화벽 설정 확인")
        sys.exit(1)

if __name__ == "__main__":
    main()
