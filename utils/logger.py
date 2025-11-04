import logging
import json
from datetime import datetime
from pathlib import Path

def setup_logger():
    # Ensure logs directory exists
    Path("logs").mkdir(exist_ok=True)
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('logs/app.log'),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)

def log_conversation(data: dict, filename: str = "data/conversations.json"):
    Path("data").mkdir(exist_ok=True)
    
    try:
        with open(filename, 'r') as f:
            conversations = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        conversations = []
    
    conversations.append(data)
    
    with open(filename, 'w') as f:
        json.dump(conversations, f, indent=2, default=str)