#!/usr/bin/env python3
"""
Instagram Bot - Example Usage Script

This script demonstrates how to use the Instagram Bot with different configurations
and scenarios. It's designed for educational purposes and safe testing.

Author: Instagram Bot Project
Version: 1.0
"""

import sys
import os
from datetime import datetime

# Add src directory to path
sys.path.append('src')

from instagram_bot import InstagramBot
from utils import Logger

def basic_usage_example():
    """Basic usage example with default configuration."""
    print("=== Basic Usage Example ===")
    
    try:
        # Initialize bot with default config
        bot = InstagramBot()
        
        # Login to Instagram
        print("Attempting to login...")
        if bot.login():
            print("[+] Login successful!")
            
            # Start automation
            print("Starting automation...")
            bot.start_automation()
            
            # Get session summary
            summary = bot.get_analytics_summary()
            print(f"[*] Session Summary: {summary}")
            
        else:
            print("[-] Login failed. Please check your credentials.")
            
    except Exception as e:
        print(f"[-] Error in basic usage: {str(e)}")
    
    finally:
        # Cleanup
        if 'bot' in locals():
            bot._cleanup()

def analytics_example():
    """Example of generating analytics reports."""
    print("\n=== Analytics Example ===")
    
    try:
        bot = InstagramBot()
        
        # Generate daily report
        daily_report = bot.generate_report("daily")
        print("[*] Daily Report:")
        for key, value in daily_report.items():
            print(f"  {key}: {value}")
        
        # Generate weekly report
        weekly_report = bot.generate_report("weekly")
        print("\n[*] Weekly Report:")
        for key, value in weekly_report.items():
            print(f"  {key}: {value}")
        
        # Create performance charts
        chart_path = bot.create_performance_charts()
        if chart_path:
            print(f"[*] Performance charts saved to: {chart_path}")
        
    except Exception as e:
        print(f"[-] Error in analytics example: {str(e)}")

def safe_testing_example():
    """Example with very conservative settings for safe testing."""
    print("\n=== Safe Testing Example ===")
    
    # Create a test configuration
    test_config = {
        "credentials": {
            "username": "your_test_username",
            "password": "your_test_password"
        },
        "targeting": {
            "target_hashtags": ["test"],  # Use safe hashtag
            "blacklist_users": []
        },
        "limits": {
            "daily_follows": 2,
            "daily_unfollows": 1,
            "daily_likes": 5,
            "daily_comments": 1,
            "hourly_actions": 3
        },
        "delays": {
            "min_delay": 60,  # Longer delays for safety
            "max_delay": 120,
            "action_delay": 10
        },
        "engagement": {
            "like_probability": 0.5,
            "comment_probability": 0.1,
            "follow_probability": 0.2
        },
        "safety": {
            "headless_mode": False,  # Show browser for monitoring
            "use_proxy": False,
            "user_agent_rotation": True
        }
    }
    
    print("[*] Test configuration created with conservative limits:")
    print(f"  Max likes per day: {test_config['limits']['daily_likes']}")
    print(f"  Max follows per day: {test_config['limits']['daily_follows']}")
    print(f"  Delay range: {test_config['delays']['min_delay']}-{test_config['delays']['max_delay']}s")
    
    # Save test config
    import json
    with open('config/test_config.json', 'w') as f:
        json.dump(test_config, f, indent=2)
    
    print("[+] Test configuration saved to config/test_config.json")
    print("[!] Remember to update credentials before testing!")

def monitoring_example():
    """Example of monitoring bot performance in real-time."""
    print("\n=== Monitoring Example ===")
    
    try:
        # Initialize logger
        logger = Logger("data/logs/monitoring.log")
        
        # Simulate monitoring session
        logger.info("Starting monitoring session")
        
        # Example metrics to monitor
        metrics_to_watch = [
            "Success rate",
            "Action frequency",
            "Error rate",
            "Response times"
        ]
        
        print("[*] Key metrics to monitor:")
        for metric in metrics_to_watch:
            print(f"  - {metric}")
        
        # Example alert conditions
        alert_conditions = {
            "success_rate_below": 70,
            "error_rate_above": 10,
            "response_time_above": 30
        }
        
        print("\n[!] Alert conditions:")
        for condition, threshold in alert_conditions.items():
            print(f"  - {condition.replace('_', ' ').title()}: {threshold}%")
        
        logger.info("Monitoring example completed")
        
    except Exception as e:
        print(f"[-] Error in monitoring example: {str(e)}")

def main():
    """Main function to run examples."""
    print("Instagram Bot - Example Usage")
    print("=" * 40)
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Safety warning
    print("\n[!] IMPORTANT SAFETY NOTICE:")
    print("  - Always test with a secondary Instagram account first")
    print("  - Start with very conservative limits")
    print("  - Monitor your account for any restrictions")
    print("  - Comply with Instagram's Terms of Service")
    print("  - Use at your own risk")
    
    # Ask for user confirmation
    response = input("\nDo you want to proceed with examples? (y/N): ")
    if response.lower() != 'y':
        print("Exiting safely. Good choice!")
        return
    
    try:
        # Run examples (commented out for safety)
        # Uncomment only after proper configuration
        
        # basic_usage_example()
        analytics_example()
        safe_testing_example()
        monitoring_example()
        
        print("\n[+] All examples completed successfully!")
        print("\nNext steps:")
        print("1. Update config/config.json with your credentials")
        print("2. Start with config/test_config.json for initial testing")
        print("3. Monitor logs in data/logs/ directory")
        print("4. Review analytics in data/analytics/ directory")
        
    except KeyboardInterrupt:
        print("\n[!] Examples interrupted by user")
    except Exception as e:
        print(f"\n[-] Unexpected error: {str(e)}")
    
    print("\n[*] Remember: Responsible automation is key to success!")

if __name__ == "__main__":
    main()