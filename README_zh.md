# MCP Chat Logger

MCP Chat Logger是一个简单而强大的聊天记录保存工具，可以将聊天历史保存为Markdown格式文件，便于后续查看和分享。

## 功能特点

- 支持大模型调用工具将聊天历史保存为格式化的Markdown文件
- 自动为每条消息添加时间戳
- 自定义保存目录
- 支持会话ID标识不同的对话
  
## 下一阶段
添加Overview功能

### 安装步骤

1. 克隆这个代码库：

```bash
git clone https://github.com/yourusername/MCP_Chat_Logger.git
cd MCP_Chat_Logger
```

2. 安装依赖：
提前安装uv

```bash
uv add "mcp[cli]"
```

## 使用方法

1. 在项目目录启动mcp服务
```bash
uv run chat_logger.py
```

2. 在cursor/cherry studio中添加mcp服务器配置
"chat_logger": {
      "name": "chat_logger",
      "isActive": false,
      "command": "uv",
      "args": [
        "--directory",
        "项目路径（例如~/MCP_Chat_Logger/）",
        "run",
        "chat_logger.py"
      ]
    }

## 项目结构

```
MCP_Chat_Logger/
├── chat_logger.py      # 核心功能实现
├── chat_logs/          # 默认保存目录
├── README.md           # 项目说明
└── .gitignore          # Git忽略文件
```

## 贡献指南

欢迎提交问题和拉取请求！如果您想贡献代码，请遵循以下步骤：

1. Fork这个仓库
2. 创建您的特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交您的更改 (`git commit -m 'Add some amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 开启一个Pull Request

## 许可证

该项目采用MIT许可证 - 详情请查看 LICENSE 文件。 