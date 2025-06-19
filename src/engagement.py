import random
import time
from typing import List, Dict, Any
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from utils import Logger, RateLimiter

class EngagementStrategy:
    """Handles Instagram engagement strategies."""
    
    def __init__(self, driver, config: Dict[str, Any], logger: Logger, rate_limiter: RateLimiter):
        self.driver = driver
        self.config = config
        self.logger = logger
        self.rate_limiter = rate_limiter
        self.wait = WebDriverWait(driver, 10)
    
    def like_posts_by_hashtag(self, hashtag: str, max_likes: int = 20) -> int:
        """Like posts from a specific hashtag."""
        likes_count = 0
        
        try:
            # Navigate to hashtag page
            hashtag_url = f"https://www.instagram.com/explore/tags/{hashtag.replace('#', '')}/"
            self.driver.get(hashtag_url)
            time.sleep(3)
            
            # Find and click on posts
            posts = self.wait.until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "article a"))
            )
            
            for i, post in enumerate(posts[:max_likes]):
                if not self.rate_limiter.can_perform_action('likes'):
                    self.logger.warning("Daily like limit reached")
                    break
                
                try:
                    post.click()
                    time.sleep(2)
                    
                    # Like the post
                    if self._like_current_post():
                        likes_count += 1
                        self.rate_limiter.record_action('likes')
                        self.logger.info(f"Liked post {i+1} from #{hashtag}")
                    
                    # Close post modal
                    self._close_post_modal()
                    self.rate_limiter.wait_random_delay()
                    
                except Exception as e:
                    self.logger.error(f"Error liking post: {str(e)}")
                    continue
        
        except Exception as e:
            self.logger.error(f"Error in like_posts_by_hashtag: {str(e)}")
        
        return likes_count
    
    def follow_users_by_hashtag(self, hashtag: str, max_follows: int = 10) -> int:
        """Follow users who posted with a specific hashtag."""
        follows_count = 0
        
        try:
            hashtag_url = f"https://www.instagram.com/explore/tags/{hashtag.replace('#', '')}/"
            self.driver.get(hashtag_url)
            time.sleep(3)
            
            posts = self.wait.until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "article a"))
            )
            
            for i, post in enumerate(posts[:max_follows]):
                if not self.rate_limiter.can_perform_action('follows'):
                    self.logger.warning("Daily follow limit reached")
                    break
                
                try:
                    post.click()
                    time.sleep(2)
                    
                    # Follow the user
                    if self._follow_current_user():
                        follows_count += 1
                        self.rate_limiter.record_action('follows')
                        self.logger.info(f"Followed user from post {i+1} in #{hashtag}")
                    
                    self._close_post_modal()
                    self.rate_limiter.wait_random_delay()
                    
                except Exception as e:
                    self.logger.error(f"Error following user: {str(e)}")
                    continue
        
        except Exception as e:
            self.logger.error(f"Error in follow_users_by_hashtag: {str(e)}")
        
        return follows_count
    
    def comment_on_posts(self, hashtag: str, max_comments: int = 5) -> int:
        """Comment on posts from a specific hashtag."""
        comments_count = 0
        
        if not self.config['comments']['enabled']:
            return 0
        
        try:
            hashtag_url = f"https://www.instagram.com/explore/tags/{hashtag.replace('#', '')}/"
            self.driver.get(hashtag_url)
            time.sleep(3)
            
            posts = self.wait.until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "article a"))
            )
            
            for i, post in enumerate(posts[:max_comments]):
                if not self.rate_limiter.can_perform_action('comments'):
                    self.logger.warning("Daily comment limit reached")
                    break
                
                if random.random() > self.config['engagement']['comment_probability']:
                    continue
                
                try:
                    post.click()
                    time.sleep(2)
                    
                    # Comment on the post
                    if self._comment_on_current_post():
                        comments_count += 1
                        self.rate_limiter.record_action('comments')
                        self.logger.info(f"Commented on post {i+1} from #{hashtag}")
                    
                    self._close_post_modal()
                    self.rate_limiter.wait_random_delay()
                    
                except Exception as e:
                    self.logger.error(f"Error commenting on post: {str(e)}")
                    continue
        
        except Exception as e:
            self.logger.error(f"Error in comment_on_posts: {str(e)}")
        
        return comments_count
    
    def _like_current_post(self) -> bool:
        """Like the currently opened post."""
        try:
            # Look for like button (heart icon)
            like_selectors = [
                'svg[aria-label="Like"]',
                'button[aria-label="Like"]',
                '[data-testid="like-button"]'
            ]
            
            for selector in like_selectors:
                try:
                    like_button = self.driver.find_element(By.CSS_SELECTOR, selector)
                    like_button.click()
                    time.sleep(1)
                    return True
                except NoSuchElementException:
                    continue
            
            return False
        except Exception as e:
            self.logger.error(f"Error liking post: {str(e)}")
            return False
    
    def _follow_current_user(self) -> bool:
        """Follow the user of the currently opened post."""
        try:
            follow_selectors = [
                'button:contains("Follow")',
                '[data-testid="follow-button"]',
                'button[type="button"]:contains("Follow")'
            ]
            
            for selector in follow_selectors:
                try:
                    follow_button = self.driver.find_element(By.CSS_SELECTOR, selector)
                    if follow_button.text.lower() == "follow":
                        follow_button.click()
                        time.sleep(1)
                        return True
                except NoSuchElementException:
                    continue
            
            return False
        except Exception as e:
            self.logger.error(f"Error following user: {str(e)}")
            return False
    
    def _comment_on_current_post(self) -> bool:
        """Comment on the currently opened post."""
        try:
            # Find comment input
            comment_input = self.driver.find_element(
                By.CSS_SELECTOR, 
                'textarea[placeholder*="comment" i], textarea[aria-label*="comment" i]'
            )
            
            # Select random comment
            comment = random.choice(self.config['comments']['templates'])
            
            comment_input.click()
            comment_input.send_keys(comment)
            time.sleep(1)
            
            # Submit comment
            submit_button = self.driver.find_element(
                By.CSS_SELECTOR, 
                'button[type="submit"], button:contains("Post")'
            )
            submit_button.click()
            time.sleep(2)
            
            return True
        except Exception as e:
            self.logger.error(f"Error commenting: {str(e)}")
            return False
    
    def _close_post_modal(self):
        """Close the post modal/overlay."""
        try:
            # Try different methods to close modal
            close_selectors = [
                'svg[aria-label="Close"]',
                'button[aria-label="Close"]',
                '[data-testid="modal-close-button"]'
            ]
            
            for selector in close_selectors:
                try:
                    close_button = self.driver.find_element(By.CSS_SELECTOR, selector)
                    close_button.click()
                    time.sleep(1)
                    return
                except NoSuchElementException:
                    continue
            
            # If no close button found, press ESC key
            from selenium.webdriver.common.keys import Keys
            self.driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.ESCAPE)
            
        except Exception as e:
            self.logger.error(f"Error closing modal: {str(e)}")