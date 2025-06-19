from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import random
from datetime import datetime
from typing import Dict, List, Any

from utils import ConfigManager, Logger, RateLimiter, get_random_user_agent
from engagement import EngagementStrategy
from analytics import AnalyticsManager

class InstagramBot:
    """Main Instagram Bot class for automated engagement."""
    
    def __init__(self, config_path: str = "config/config.json"):
        """Initialize the Instagram bot."""
        self.config = ConfigManager.load_config(config_path)
        self.logger = Logger()
        self.rate_limiter = RateLimiter(self.config)
        self.analytics = AnalyticsManager(self.logger)
        self.driver = None
        self.engagement = None
        self.session_start_time = None
        
        self.logger.info("Instagram Bot initialized")
    
    def setup_driver(self):
        """Set up Chrome WebDriver with appropriate options."""
        try:
            chrome_options = Options()
            
            # Configure Chrome options
            if self.config['safety']['headless_mode']:
                chrome_options.add_argument('--headless')
            
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-blink-features=AutomationControlled')
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            
            # Set user agent
            if self.config['safety']['user_agent_rotation']:
                user_agent = get_random_user_agent()
                chrome_options.add_argument(f'--user-agent={user_agent}')
            
            # Set up driver
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            
            # Execute script to remove webdriver property
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            self.logger.info("WebDriver setup completed")
            
        except Exception as e:
            self.logger.error(f"Error setting up WebDriver: {str(e)}")
            raise
    
    def login(self) -> bool:
        """Login to Instagram."""
        try:
            if not self.driver:
                self.setup_driver()
            
            self.logger.info("Attempting to login to Instagram")
            
            # Navigate to Instagram login page
            self.driver.get("https://www.instagram.com/accounts/login/")
            time.sleep(3)
            
            # Wait for login form to load
            wait = WebDriverWait(self.driver, 10)
            
            # Find and fill username
            username_input = wait.until(
                EC.presence_of_element_located((By.NAME, "username"))
            )
            username_input.send_keys(self.config['credentials']['username'])
            
            # Find and fill password
            password_input = self.driver.find_element(By.NAME, "password")
            password_input.send_keys(self.config['credentials']['password'])
            
            # Click login button
            login_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
            login_button.click()
            
            # Wait for login to complete
            time.sleep(5)
            
            # Check if login was successful
            if "instagram.com" in self.driver.current_url and "login" not in self.driver.current_url:
                self.logger.info("Successfully logged in to Instagram")
                
                # Handle "Save Your Login Info" popup
                self._handle_save_login_popup()
                
                # Handle notifications popup
                self._handle_notifications_popup()
                
                return True
            else:
                self.logger.error("Login failed - still on login page")
                return False
                
        except Exception as e:
            self.logger.error(f"Error during login: {str(e)}")
            return False
    
    def start_automation(self):
        """Start the main automation process."""
        if not self.driver:
            self.logger.error("Driver not initialized. Please login first.")
            return
        
        self.session_start_time = datetime.now()
        self.engagement = EngagementStrategy(self.driver, self.config, self.logger, self.rate_limiter)
        
        session_stats = {
            'likes_count': 0,
            'follows_count': 0,
            'comments_count': 0,
            'target_hashtags': [],
            'success_rate': 0,
            'duration_minutes': 0
        }
        
        try:
            self.logger.info("Starting automation process")
            
            # Process each target hashtag
            for hashtag in self.config['targeting']['target_hashtags']:
                self.logger.info(f"Processing hashtag: {hashtag}")
                session_stats['target_hashtags'].append(hashtag)
                
                # Like posts
                if random.random() <= self.config['engagement']['like_probability']:
                    likes = self.engagement.like_posts_by_hashtag(hashtag, max_likes=20)
                    session_stats['likes_count'] += likes
                
                # Follow users
                if random.random() <= self.config['engagement']['follow_probability']:
                    follows = self.engagement.follow_users_by_hashtag(hashtag, max_follows=10)
                    session_stats['follows_count'] += follows
                
                # Comment on posts
                if self.config['comments']['enabled']:
                    comments = self.engagement.comment_on_posts(hashtag, max_comments=5)
                    session_stats['comments_count'] += comments
                
                # Wait between hashtags
                self.rate_limiter.wait_random_delay()
            
            # Calculate session metrics
            total_actions = session_stats['likes_count'] + session_stats['follows_count'] + session_stats['comments_count']
            session_stats['success_rate'] = (total_actions / len(self.config['targeting']['target_hashtags'])) * 100 if total_actions > 0 else 0
            session_stats['duration_minutes'] = (datetime.now() - self.session_start_time).total_seconds() / 60
            session_stats['target_hashtags'] = ', '.join(session_stats['target_hashtags'])
            
            # Record session analytics
            self.analytics.record_session(session_stats)
            
            self.logger.info(f"Automation session completed: {session_stats}")
            
        except Exception as e:
            self.logger.error(f"Error during automation: {str(e)}")
        
        finally:
            self._cleanup()
    
    def get_analytics_summary(self) -> Dict[str, Any]:
        """Get analytics summary."""
        return self.analytics.get_engagement_metrics()
    
    def generate_report(self, report_type: str = "daily") -> Dict[str, Any]:
        """Generate analytics report."""
        if report_type == "daily":
            return self.analytics.generate_daily_report()
        elif report_type == "weekly":
            return self.analytics.generate_weekly_report()
        else:
            return {"error": "Invalid report type. Use 'daily' or 'weekly'"}
    
    def create_performance_charts(self):
        """Create performance visualization charts."""
        return self.analytics.create_performance_charts()
    
    def _handle_save_login_popup(self):
        """Handle the 'Save Your Login Info' popup."""
        try:
            not_now_button = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Not Now')]"))
            )
            not_now_button.click()
            time.sleep(2)
        except:
            pass  # Popup might not appear
    
    def _handle_notifications_popup(self):
        """Handle the notifications popup."""
        try:
            not_now_button = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Not Now')]"))
            )
            not_now_button.click()
            time.sleep(2)
        except:
            pass  # Popup might not appear
    
    def _cleanup(self):
        """Clean up resources."""
        if self.driver:
            self.driver.quit()
            self.logger.info("WebDriver closed")
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self._cleanup()

# Example usage
if __name__ == "__main__":
    # Create bot instance
    bot = InstagramBot()
    
    try:
        # Login and start automation
        if bot.login():
            bot.start_automation()
            
            # Generate reports
            daily_report = bot.generate_report("daily")
            print("Daily Report:", daily_report)
            
            # Create charts
            chart_path = bot.create_performance_charts()
            if chart_path:
                print(f"Performance charts saved to: {chart_path}")
        
    except Exception as e:
        print(f"Error: {e}")
    
    finally:
        bot._cleanup()