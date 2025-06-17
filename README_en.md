# MCP Chat Logger

[![smithery badge](https://smithery.ai/badge/@AlexiFeng/MCP_Chat_Logger)](https://smithery.ai/server/@AlexiFeng/MCP_Chat_Logger)

<div align="center">
  <a href="README.md">中文</a> | <a href="README_ko.md">한국어</a>
</div>

---

MCP Chat Logger is a simple yet powerful tool for saving chat history as Markdown format files with real-time message publishing through RabbitMQ support.

## 🚀 Quick Start

### Easy Setup with Makefile

```bash
# 1. Complete initial setup (install dependencies + environment setup)
make setup

# 2. Start RabbitMQ server
make start-rabbitmq

# 3. Test RabbitMQ connection
make test-rabbitmq

# 4. Run MCP server
make run
```

### Available Make Commands

| Command | Description |
|---------|-------------|
| `make help` | Display all available commands |
| `make install` | Install project dependencies |
| `make setup-env` | Setup environment variables (.env file) |
| `make start-rabbitmq` | Start RabbitMQ server (Docker) |
| `make stop-rabbitmq` | Stop RabbitMQ server |
| `make test-rabbitmq` | Test RabbitMQ connection |
| `make run` | Run MCP Chat Logger server |
| `make clean` | Clean temporary files |
| `make setup` | Complete initial setup (install + setup-env) |

## Features

- 🐰 **RabbitMQ Integration**: Real-time message publishing and subscription support
- 📝 **Markdown Storage**: Save chat history in clean Markdown format
- ⏰ **Timestamps**: Automatically add timestamps to each message
- 📁 **Custom Directory**: Support for user-defined save directories
- 🔍 **Session Management**: Support session IDs to identify different conversations
- 🛠️ **Environment Variables**: Configuration management through `.env` files
- 🔧 **Testing Tools**: RabbitMQ connection and configuration verification tools

## RabbitMQ Configuration

### Environment Variables

Create a `.env` file to manage RabbitMQ settings:

```bash
# .env file example
RABBITMQ_HOST=localhost
RABBITMQ_PORT=5672
RABBITMQ_USERNAME=guest
RABBITMQ_PASSWORD=guest
RABBITMQ_VIRTUAL_HOST=/
RABBITMQ_EXCHANGE=llmLogger
RABBITMQ_ROUTING_KEY=llm_logger
RABBITMQ_QUEUE_NAME=llm_logger
```

### Exchange Design

- **Exchange Name**: `llmLogger`
- **Exchange Type**: `direct`
- **Routing Key**: `llm_logger`
- **Queue Name**: `llm_logger`
- **Binding**: Queue `llm_logger` bound to Exchange `llmLogger` with Routing Key `llm_logger`

### New MCP Tools

1. **test_rabbitmq_connection**: Test RabbitMQ connection
2. **get_rabbitmq_config**: Check current RabbitMQ configuration
3. **save_chat_history**: File saving + RabbitMQ message publishing (extended functionality)

## Installation & Setup

### Automatic Installation via Smithery

Install MCP Chat Logger for Claude Desktop automatically via [Smithery](https://smithery.ai/server/@AlexiFeng/MCP_Chat_Logger):

```bash
npx -y @smithery/cli install @AlexiFeng/MCP_Chat_Logger --client claude
```

### Manual Installation

1. **Clone Repository**:
```bash
git clone https://github.com/yourusername/MCP_Chat_Logger.git
cd MCP_Chat_Logger
```

2. **Prerequisites**: Install `uv` beforehand

3. **Install Dependencies**:
```bash
make install
# Or manually:
uv add "mcp[cli]>=1.6.0"
uv add "pika>=1.3.0"
uv add "python-dotenv>=1.0.0"
```

4. **Environment Setup**:
```bash
make setup-env
# Or manually:
cp .env.example .env
nano .env  # Modify as needed
```

## Usage

### RabbitMQ Environment

1. **Start RabbitMQ Server**:
```bash
make start-rabbitmq
# Web management UI: http://localhost:15672 (guest/guest)
```

2. **Test Connection**:
```bash
make test-rabbitmq
```

3. **Run MCP Server**:
```bash
make run
```

### Claude Desktop / Cursor Configuration

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

### Available MCP Tools

1. **save_chat_history**: Save chat history as Markdown files and publish to RabbitMQ
2. **test_rabbitmq_connection**: Test RabbitMQ connection status
3. **get_rabbitmq_config**: Check current RabbitMQ configuration

## Project Structure

```
MCP_Chat_Logger/
├── chat_logger.py         # Main MCP server (RabbitMQ integration)
├── rabbitmq_publisher.py  # RabbitMQ message publishing module
├── test_rabbitmq.py       # RabbitMQ connection test script
├── Makefile              # Convenience commands
├── .env.example           # Environment variables example
├── .env                   # Environment variables config (user-created)
├── docker-compose.yml     # RabbitMQ Docker configuration
├── rabbitmq_init/        # RabbitMQ initialization scripts
│   └── init.sh
├── chat_logs/            # Default save directory
├── pyproject.toml        # Project settings and dependencies
├── README.md             # Project description (Korean)
├── README_zh.md          # Chinese description
├── README_en.md          # English description
└── .gitignore            # Git ignore file
```

## Development & Maintenance

### Cleanup Commands

```bash
# Clean temporary files
make clean

# Stop RabbitMQ server
make stop-rabbitmq
```

## Next Steps

- Add Overview functionality
- Message format customization options
- Additional message broker support

## Contribution Guidelines

Issues and pull requests are welcome! If you want to contribute code, please follow these steps:

1. Fork this repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 