.PHONY: help install setup-env start-rabbitmq stop-rabbitmq test-rabbitmq run clean

# 기본 타겟
help:
	@echo "🐰 MCP Chat Logger with RabbitMQ"
	@echo "================================"
	@echo ""
	@echo "사용 가능한 명령어:"
	@echo "  install         - 의존성 설치"
	@echo "  setup-env       - 환경변수 파일 설정"
	@echo "  start-rabbitmq  - RabbitMQ 서버 시작 (Docker)"
	@echo "  stop-rabbitmq   - RabbitMQ 서버 정지"
	@echo "  test-rabbitmq   - RabbitMQ 연결 테스트"
	@echo "  run             - MCP 서버 실행"
	@echo "  clean           - 임시 파일 정리"
	@echo ""

# 의존성 설치
install:
	@echo "📦 의존성 설치 중..."
	uv add "mcp[cli]>=1.6.0"
	uv add "pika>=1.3.0"
	uv add "python-dotenv>=1.0.0"
	@echo "✅ 의존성 설치 완료!"

# 환경변수 파일 설정
setup-env:
	@if [ ! -f .env ]; then \
		echo "🔧 환경변수 파일 생성 중..."; \
		cp .env.example .env; \
		echo "✅ .env 파일이 생성되었습니다. 필요에 따라 수정하세요."; \
	else \
		echo "ℹ️  .env 파일이 이미 존재합니다."; \
	fi

# RabbitMQ 서버 시작
start-rabbitmq:
	@echo "🐰 RabbitMQ 서버 시작 중..."
	docker-compose up -d rabbitmq
	@echo "✅ RabbitMQ 서버가 시작되었습니다!"
	@echo "🌐 관리 UI: http://localhost:15672 (guest/guest)"

# RabbitMQ 서버 정지
stop-rabbitmq:
	@echo "🛑 RabbitMQ 서버 정지 중..."
	docker-compose down
	@echo "✅ RabbitMQ 서버가 정지되었습니다."

# RabbitMQ 연결 테스트
test-rabbitmq:
	@echo "🔍 RabbitMQ 연결 테스트 중..."
	uv run test_rabbitmq.py

# MCP 서버 실행
run:
	@echo "🚀 MCP Chat Logger 서버 실행 중..."
	uv run chat_logger.py

# 임시 파일 정리
clean:
	@echo "🧹 임시 파일 정리 중..."
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.log" -delete
	@echo "✅ 정리 완료!"

# 전체 설정 (처음 사용시)
setup: install setup-env
	@echo "🎉 초기 설정이 완료되었습니다!"
	@echo ""
	@echo "다음 단계:"
	@echo "1. make start-rabbitmq  # RabbitMQ 서버 시작"
	@echo "2. make test-rabbitmq   # 연결 테스트"
	@echo "3. make run             # MCP 서버 실행"
