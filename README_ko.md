# MCP Chat Logger

[![smithery badge](https://smithery.ai/badge/@AlexiFeng/MCP_Chat_Logger)](https://smithery.ai/server/@AlexiFeng/MCP_Chat_Logger)

<div align="center">
  <a href="README.md">中文</a> | <a href="README_en.md">English</a>
</div>

---

MCP Chat Logger는 채팅 기록을 Markdown 형식으로 저장하는 간단하면서도 강력한 도구입니다. RabbitMQ를 통한 실시간 메시지 발행 기능도 지원합니다.

## 🚀 빠른 시작

### Makefile을 사용한 간편 설정

```bash
# 1. 전체 초기 설정 (의존성 설치 + 환경변수 설정)
make setup

# 2. RabbitMQ 서버 시작
make start-rabbitmq

# 3. RabbitMQ 연결 테스트
make test-rabbitmq

# 4. MCP 서버 실행
make run
```

### 사용 가능한 Make 명령어

| 명령어 | 설명 |
|--------|------|
| `make help` | 사용 가능한 모든 명령어 표시 |
| `make install` | 프로젝트 의존성 설치 |
| `make setup-env` | 환경변수 파일 (.env) 설정 |
| `make start-rabbitmq` | RabbitMQ 서버 시작 (Docker) |
| `make stop-rabbitmq` | RabbitMQ 서버 정지 |
| `make test-rabbitmq` | RabbitMQ 연결 테스트 |
| `make run` | MCP Chat Logger 서버 실행 |
| `make clean` | 임시 파일 정리 |
| `make setup` | 전체 초기 설정 (install + setup-env) |

## 기능 특점

- 🐰 **RabbitMQ 통합**: 실시간 메시지 발행 및 구독 지원
- 📝 **Markdown 저장**: 채팅 기록을 깔끔한 Markdown 형식으로 저장
- ⏰ **타임스탬프**: 각 메시지에 자동으로 타임스탬프 추가
- 📁 **커스텀 디렉토리**: 사용자 정의 저장 디렉토리 지원
- 🔍 **세션 관리**: 세션 ID를 통한 서로 다른 대화 식별 지원
- 🛠️ **환경변수**: `.env` 파일을 통한 설정 관리
- 🔧 **테스트 도구**: RabbitMQ 연결 및 설정 확인 도구 제공

## RabbitMQ 설정

### 환경변수

`.env` 파일을 생성하여 RabbitMQ 설정을 관리할 수 있습니다:

```bash
# .env 파일 예시
RABBITMQ_HOST=localhost
RABBITMQ_PORT=5672
RABBITMQ_USERNAME=guest
RABBITMQ_PASSWORD=guest
RABBITMQ_VIRTUAL_HOST=/
RABBITMQ_EXCHANGE=llmLogger
RABBITMQ_ROUTING_KEY=llm_logger
RABBITMQ_QUEUE_NAME=llm_logger
```

### Exchange 설계

- **Exchange 이름**: `llmLogger`
- **Exchange 타입**: `direct`
- **라우팅 키**: `llm_logger`
- **큐 이름**: `llm_logger`
- **바인딩**: 큐 `llm_logger`가 Exchange `llmLogger`에 라우팅 키 `llm_logger`로 바인딩됨

### 새로운 MCP 도구들

1. **test_rabbitmq_connection**: RabbitMQ 연결 테스트
2. **get_rabbitmq_config**: 현재 RabbitMQ 설정 확인
3. **save_chat_history**: 파일 저장 + RabbitMQ 메시지 발행 (기존 기능 확장)

## 설치 및 설정

### Smithery를 통한 자동 설치

[Smithery](https://smithery.ai/server/@AlexiFeng/MCP_Chat_Logger)를 통해 Claude Desktop용 MCP Chat Logger를 자동으로 설치할 수 있습니다:

```bash
npx -y @smithery/cli install @AlexiFeng/MCP_Chat_Logger --client claude
```

### 수동 설치

1. **저장소 클론**:
```bash
git clone https://github.com/yourusername/MCP_Chat_Logger.git
cd MCP_Chat_Logger
```

2. **사전 요구사항**: `uv` 설치 필요

3. **의존성 설치**:
```bash
make install
# 또는 수동으로:
uv add "mcp[cli]>=1.6.0"
uv add "pika>=1.3.0"
uv add "python-dotenv>=1.0.0"
```

4. **환경변수 설정**:
```bash
make setup-env
# 또는 수동으로:
cp .env.example .env
nano .env  # 필요에 따라 수정
```

## 사용법

### RabbitMQ 환경

1. **RabbitMQ 서버 시작**:
```bash
make start-rabbitmq
# 웹 관리 UI: http://localhost:15672 (guest/guest)
```

2. **연결 테스트**:
```bash
make test-rabbitmq
```

3. **MCP 서버 실행**:
```bash
make run
```

### Claude Desktop / Cursor 설정

```json
{
  "chat_logger": {
    "name": "chat_logger",
    "isActive": true,
    "command": "uv",
    "args": [
      "--directory",
      "/path/to/MCP_Chat_Logger",
      "run",
      "chat_logger.py"
    ],
    "env": {
      "RABBITMQ_HOST": "localhost"
    }
  }
}
```

### 사용 가능한 MCP 도구들

1. **save_chat_history**: 채팅 기록을 Markdown 파일로 저장하고 RabbitMQ로 발행
2. **test_rabbitmq_connection**: RabbitMQ 연결 상태 테스트
3. **get_rabbitmq_config**: 현재 RabbitMQ 설정 확인

## 프로젝트 구조

```
MCP_Chat_Logger/
├── chat_logger.py         # 메인 MCP 서버 (RabbitMQ 기능 확장)
├── rabbitmq_publisher.py  # RabbitMQ 메시지 발행 모듈
├── test_rabbitmq.py       # RabbitMQ 연결 테스트 스크립트
├── Makefile              # 편의 명령어들
├── .env.example           # 환경변수 예시 파일
├── .env                   # 환경변수 설정 파일 (개인이 생성)
├── docker-compose.yml     # RabbitMQ Docker 구성
├── rabbitmq_init/        # RabbitMQ 초기화 스크립트
│   └── init.sh
├── chat_logs/            # 기본 저장 디렉토리
├── pyproject.toml        # 프로젝트 설정 및 의존성
├── README.md             # 프로젝트 설명 (중문)
├── README_ko.md          # 한국어 설명
├── README_en.md          # 영어 설명
└── .gitignore            # Git 무시 파일
```

## 개발 및 유지보수

### 정리 명령어

```bash
# 임시 파일 정리
make clean

# RabbitMQ 서버 정지
make stop-rabbitmq
```

## 다음 단계

- Overview 기능 추가
- 메시지 포맷 커스터마이징 옵션
- 추가 메시지 브로커 지원

## 기여 방법

문제 제기와 풀 리퀘스트를 환영합니다! 코드 기여를 원하시면 다음 단계를 따라주세요:

1. 이 저장소를 Fork하세요
2. 기능 브랜치를 생성하세요 (`git checkout -b feature/amazing-feature`)
3. 변경사항을 커밋하세요 (`git commit -m 'Add some amazing feature'`)
4. 브랜치에 푸시하세요 (`git push origin feature/amazing-feature`)
5. Pull Request를 열어주세요

## 라이센스

이 프로젝트는 MIT 라이센스 하에 있습니다 - 자세한 내용은 LICENSE 파일을 참조하세요. 