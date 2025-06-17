# MCP Chat Logger

[![smithery badge](https://smithery.ai/badge/@AlexiFeng/MCP_Chat_Logger)](https://smithery.ai/server/@AlexiFeng/MCP_Chat_Logger)

<div align="center">
  <a href="README_ko.md">한국어</a> | <a href="README_en.md">English</a>
</div>

---

MCP Chat Logger是一个简单而强大的聊天记录保存工具，可以将聊天历史保存为Markdown格式文件，并支持通过RabbitMQ进行实时消息发布。

## 🚀 快速开始

### 使用Makefile简便设置

```bash
# 1. 完整初始设置（安装依赖+环境设置）
make setup

# 2. 启动RabbitMQ服务器
make start-rabbitmq

# 3. 测试RabbitMQ连接
make test-rabbitmq

# 4. 运行MCP服务器
make run
```

### 可用的Make命令

| 命令 | 说明 |
|------|------|
| `make help` | 显示所有可用命令 |
| `make install` | 安装项目依赖 |
| `make setup-env` | 设置环境变量（.env文件） |
| `make start-rabbitmq` | 启动RabbitMQ服务器（Docker） |
| `make stop-rabbitmq` | 停止RabbitMQ服务器 |
| `make test-rabbitmq` | 测试RabbitMQ连接 |
| `make run` | 运行MCP Chat Logger服务器 |
| `make clean` | 清理临时文件 |
| `make setup` | 完整初始设置（install + setup-env） |

## 功能特点

- 🐰 **RabbitMQ集成**：实时消息发布和订阅支持
- 📝 **Markdown存储**：将聊天记录保存为整洁的Markdown格式
- ⏰ **时间戳**：自动为每条消息添加时间戳
- 📁 **自定义目录**：支持用户自定义保存目录
- 🔍 **会话管理**：支持会话ID标识不同的对话
- 🛠️ **环境变量**：通过`.env`文件进行配置管理
- 🔧 **测试工具**：提供RabbitMQ连接和配置验证工具

## RabbitMQ配置

### 环境变量

创建`.env`文件来管理RabbitMQ设置：

```bash
# .env文件示例
RABBITMQ_HOST=localhost
RABBITMQ_PORT=5672
RABBITMQ_USERNAME=guest
RABBITMQ_PASSWORD=guest
RABBITMQ_VIRTUAL_HOST=/
RABBITMQ_EXCHANGE=llmLogger
RABBITMQ_ROUTING_KEY=llm_logger
RABBITMQ_QUEUE_NAME=llm_logger
```

### Exchange设计

- **Exchange名称**：`llmLogger`
- **Exchange类型**：`direct`
- **路由键**：`llm_logger`
- **队列名称**：`llm_logger`
- **绑定**：队列`llm_logger`通过路由键`llm_logger`绑定到Exchange `llmLogger`

### 新的MCP工具

1. **test_rabbitmq_connection**：测试RabbitMQ连接
2. **get_rabbitmq_config**：检查当前RabbitMQ配置
3. **save_chat_history**：文件保存 + RabbitMQ消息发布（扩展功能）

## 安装和设置

### 通过Smithery自动安装

通过[Smithery](https://smithery.ai/server/@AlexiFeng/MCP_Chat_Logger)为Claude Desktop自动安装MCP Chat Logger：

```bash
npx -y @smithery/cli install @AlexiFeng/MCP_Chat_Logger --client claude
```

### 手动安装

1. **克隆仓库**：
```bash
git clone https://github.com/yourusername/MCP_Chat_Logger.git
cd MCP_Chat_Logger
```

2. **前提条件**：提前安装`uv`

3. **安装依赖**：
```bash
make install
# 或手动：
uv add "mcp[cli]>=1.6.0"
uv add "pika>=1.3.0"
uv add "python-dotenv>=1.0.0"
```

4. **环境设置**：
```bash
make setup-env
# 或手动：
cp .env.example .env
nano .env  # 根据需要修改
```

## 使用方法

### RabbitMQ环境

1. **启动RabbitMQ服务器**：
```bash
make start-rabbitmq
# Web管理界面：http://localhost:15672 (guest/guest)
```

2. **测试连接**：
```bash
make test-rabbitmq
```

3. **运行MCP服务器**：
```bash
make run
```

### Claude Desktop / Cursor配置

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

### 可用的MCP工具

1. **save_chat_history**：将聊天记录保存为Markdown文件并发布到RabbitMQ
2. **test_rabbitmq_connection**：测试RabbitMQ连接状态
3. **get_rabbitmq_config**：检查当前RabbitMQ配置

## 项目结构

```
MCP_Chat_Logger/
├── chat_logger.py         # 主MCP服务器（RabbitMQ集成）
├── rabbitmq_publisher.py  # RabbitMQ消息发布模块
├── test_rabbitmq.py       # RabbitMQ连接测试脚本
├── Makefile              # 便利命令
├── .env.example           # 环境变量示例
├── .env                   # 环境变量配置（用户创建）
├── docker-compose.yml     # RabbitMQ Docker配置
├── rabbitmq_init/        # RabbitMQ初始化脚本
│   └── init.sh
├── chat_logs/            # 默认保存目录
├── pyproject.toml        # 项目设置和依赖
├── README.md             # 项目说明（中文）
├── README_ko.md          # 韩语说明
├── README_en.md          # 英文说明
└── .gitignore            # Git忽略文件
```

## 开发和维护

### 清理命令

```bash
# 清理临时文件
make clean

# 停止RabbitMQ服务器
make stop-rabbitmq
```

## 下一阶段

- 添加Overview功能
- 消息格式自定义选项
- 额外的消息代理支持

## 贡献指南

欢迎提交问题和拉取请求！如果您想贡献代码，请遵循以下步骤：

1. Fork这个仓库
2. 创建您的特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交您的更改 (`git commit -m 'Add some amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 开启一个Pull Request

## 许可证

该项目采用MIT许可证 - 详情请查看 LICENSE 文件。
