from typing import List, Dict, Any
import os
from datetime import datetime
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
from rabbitmq_publisher import publish_chat_message, get_publisher

# Load environment variables
load_dotenv()

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
    Save chat history as a Markdown file and publish to RabbitMQ
    
    Args:
        messages: List of chat messages, each containing role and content
        conversation_id: Optional conversation ID for file naming
    """
    # 1. Validate messages parameter
    if not messages:
        return "❌ Error: messages parameter is empty or missing."
    
    if not isinstance(messages, list):
        return "❌ Error: messages must be a list."
    
    # 2. Validate individual messages
    for i, message in enumerate(messages):
        if not isinstance(message, dict):
            return f"❌ Error: Message #{i} is not in proper format."
        
        if 'role' not in message or 'content' not in message:
            return f"❌ Error: Message #{i} is missing 'role' or 'content'."
    
    
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
    
    result_message = f"Chat history has been saved to file: {filename}"
    
    # Publish message to RabbitMQ
    try:
        additional_metadata = {
            "filename": filename,
            "file_size": os.path.getsize(filename),
            "message_count": len(messages),
            "save_timestamp": timestamp
        }
        
        publish_success = publish_chat_message(
            messages=messages,
            conversation_id=conversation_id,
            additional_metadata=additional_metadata
        )
        
        if publish_success:
            result_message += "\n✓ RabbitMQ message published successfully"
        else:
            result_message += "\n⚠ RabbitMQ message publish failed (file saved successfully)"
            
    except Exception as e:
        result_message += f"\n⚠ RabbitMQ publish error: {str(e)} (file saved successfully)"
    
    return result_message

@mcp.tool()
async def test_rabbitmq_connection() -> str:
    """
    Test RabbitMQ connection and configuration
    
    Returns:
        str: Connection test result
    """
    try:
        publisher = get_publisher()
        
        # Display connection information
        connection_info = f"""
🔗 RabbitMQ Connection Settings:
- Host: {publisher.host}:{publisher.port}
- Virtual Host: {publisher.virtual_host}
- Exchange: {publisher.exchange}
- Routing Key: {publisher.routing_key}
- Queue Name: {publisher.queue_name}
        """
        
        # Test connection
        if publisher.test_connection():
            return connection_info + "\n\n✅ RabbitMQ connection test successful!"
        else:
            return connection_info + "\n\n❌ RabbitMQ connection test failed. Please check your configuration."
            
    except Exception as e:
        return f"❌ Error occurred during RabbitMQ connection test: {str(e)}"

@mcp.tool()
async def get_rabbitmq_config() -> str:
    """
    Get current RabbitMQ configuration from environment variables
    
    Returns:
        str: Current RabbitMQ configuration
    """
    config = {
        "RABBITMQ_HOST": os.getenv('RABBITMQ_HOST', 'localhost'),
        "RABBITMQ_PORT": os.getenv('RABBITMQ_PORT', '5672'),
        "RABBITMQ_USERNAME": os.getenv('RABBITMQ_USERNAME', 'guest'),
        "RABBITMQ_PASSWORD": "[HIDDEN]" if os.getenv('RABBITMQ_PASSWORD') else "[NOT SET]",
        "RABBITMQ_VIRTUAL_HOST": os.getenv('RABBITMQ_VIRTUAL_HOST', '/'),
        "RABBITMQ_EXCHANGE": os.getenv('RABBITMQ_EXCHANGE', 'llmLogger'),
        "RABBITMQ_ROUTING_KEY": os.getenv('RABBITMQ_ROUTING_KEY', 'llm_logger'),
        "RABBITMQ_QUEUE_NAME": os.getenv('RABBITMQ_QUEUE_NAME', 'llm_logger')
    }
    
    config_text = "📋 Current RabbitMQ Configuration:\n\n"
    for key, value in config.items():
        config_text += f"- {key}: {value}\n"
    
    config_text += "\n💡 To change settings: Edit .env file or set environment variables."
    
    return config_text

if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio') 