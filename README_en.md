# MCP Chat Logger

MCP Chat Logger is a simple yet powerful tool for saving chat history as Markdown format files, making it convenient for later viewing and sharing.

## Features

- Supports large models calling tools to save chat history as formatted Markdown files
- Automatically adds timestamps to each message
- Customizable save directory
- Supports session IDs to identify different conversations
  
## Next Phase
Add Overview functionality

### Installation Steps

1. Clone this repository:

```bash
git clone https://github.com/yourusername/MCP_Chat_Logger.git
cd MCP_Chat_Logger
```

2. Install dependencies:
Install uv beforehand

```bash
uv add "mcp[cli]"
```

## Usage

1. Start the mcp service in the project directory
```bash
uv run chat_logger.py
```

2. Add mcp server configuration in cursor/cherry studio
"chat_logger": {
      "name": "chat_logger",
      "isActive": false,
      "command": "uv",
      "args": [
        "--directory",
        "project path (e.g., ~/MCP_Chat_Logger/)",
        "run",
        "chat_logger.py"
      ]
    }

## Project Structure

```
MCP_Chat_Logger/
├── chat_logger.py      # Core functionality implementation
├── chat_logs/          # Default save directory
├── README.md           # Project description
└── .gitignore          # Git ignore file
```

## Contribution Guidelines

Issues and pull requests are welcome! If you want to contribute code, please follow these steps:

1. Fork this repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 