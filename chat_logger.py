from typing import List, Dict, Any
import os
from datetime import datetime
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("chat_logger")

def ensure_logs_directory():
    """Ensure the logs directory exists"""
    if not os.path.exists("chat_logs"):
        os.makedirs("chat_logs")

def format_message(message: Dict[str, Any]) -> str:
    """Format message into Markdown format"""
    role = message.get("role", "unknown")
    content = message.get("content", "")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    return f"""
### {role.capitalize()} - {timestamp}

{content}

---
"""

@mcp.tool()
async def save_chat_history(messages: List[Dict[str, Any]], conversation_id: str = None) -> str:
    """
    Save chat history as a Markdown file
    
    Args:
        messages: List of chat messages, each containing role and content
        conversation_id: Optional conversation ID for file naming
    """
    ensure_logs_directory()
    
    # Generate filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"chat_logs/chat_{conversation_id}_{timestamp}.md" if conversation_id else f"chat_logs/chat_{timestamp}.md"
    
    # Format all messages
    formatted_content = "# Chat History\n\n"
    formatted_content += f"Conversation ID: {conversation_id}\n" if conversation_id else ""
    formatted_content += f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    
    for message in messages:
        formatted_content += format_message(message)
    
    # Save file
    with open(filename, "w", encoding="utf-8") as f:
        f.write(formatted_content)
    
    return f"Chat history has been saved to file: {filename}"

if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio') 