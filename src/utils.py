import json
import time
import random
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Any
import os

class ConfigManager:
    """Manages configuration loading and validation."""
    
    @staticmethod
    def load_config(config_path: str = "config/config.json") -> Dict[str, Any]:
        """Load configuration from JSON file."""
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"Config file not found: {config_path}")
        except json.JSONDecodeError:
            raise ValueError(f"Invalid JSON in config file: {config_path}")

class Logger:
    """Custom logger for Instagram bot activities."""
    
    def __init__(self, log_file: str = "data/logs/bot_activity.log"):
        self.log_file = log_file
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def info(self, message: str):
        self.logger.info(message)
    
    def warning(self, message: str):
        self.logger.warning(message)
    
    def error(self, message: str):
        self.logger.error(message)

class RateLimiter:
    """Manages rate limiting and delays."""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.action_counts = {
            'likes': 0,
            'follows': 0,
            'unfollows': 0,
            'comments': 0
        }
        self.last_reset = datetime.now()
    
    def can_perform_action(self, action_type: str) -> bool:
        """Check if action can be performed within limits."""
        self._reset_daily_counts()
        
        limits = {
            'likes': self.config['limits']['daily_likes'],
            'follows': self.config['limits']['daily_follows'],
            'unfollows': self.config['limits']['daily_unfollows'],
            'comments': self.config['limits']['daily_comments']
        }
        
        return self.action_counts[action_type] < limits[action_type]
    
    def record_action(self, action_type: str):
        """Record an action and increment counter."""
        self.action_counts[action_type] += 1
    
    def wait_random_delay(self):
        """Wait for a random delay between actions."""
        min_delay = self.config['delays']['min_delay']
        max_delay = self.config['delays']['max_delay']
        delay = random.randint(min_delay, max_delay)
        time.sleep(delay)
    
    def _reset_daily_counts(self):
        """Reset counters if a new day has started."""
        if datetime.now() - self.last_reset > timedelta(days=1):
            self.action_counts = {key: 0 for key in self.action_counts}
            self.last_reset = datetime.now()

class DataManager:
    """Manages data storage and retrieval."""
    
    @staticmethod
    def save_to_json(data: Dict[str, Any], filepath: str):
        """Save data to JSON file."""
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2, default=str)
    
    @staticmethod
    def load_from_json(filepath: str) -> Dict[str, Any]:
        """Load data from JSON file."""
        try:
            with open(filepath, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
    
    @staticmethod
    def append_to_csv(data: List[Dict[str, Any]], filepath: str):
        """Append data to CSV file."""
        import pandas as pd
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        df = pd.DataFrame(data)
        if os.path.exists(filepath):
            df.to_csv(filepath, mode='a', header=False, index=False)
        else:
            df.to_csv(filepath, index=False)

def get_random_user_agent() -> str:
    """Get a random user agent string."""
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    ]
    return random.choice(user_agents)

def validate_hashtag(hashtag: str) -> str:
    """Validate and format hashtag."""
    hashtag = hashtag.strip()
    if not hashtag.startswith('#'):
        hashtag = '#' + hashtag
    return hashtag.lower()