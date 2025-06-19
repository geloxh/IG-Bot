import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
from typing import Dict, List, Any
import os
from utils import DataManager, Logger

class AnalyticsManager:
    """Manages analytics and reporting for Instagram bot activities."""
    
    def __init__(self, logger: Logger):
        self.logger = logger
        self.data_manager = DataManager()
        self.analytics_dir = "data/analytics"
        os.makedirs(self.analytics_dir, exist_ok=True)
    
    def record_session(self, session_data: Dict[str, Any]):
        """Record a bot session with metrics."""
        session_data['timestamp'] = datetime.now().isoformat()
        
        # Save to CSV
        csv_path = f"{self.analytics_dir}/sessions.csv"
        self.data_manager.append_to_csv([session_data], csv_path)
        
        self.logger.info(f"Session recorded: {session_data}")
    
    def record_action(self, action_type: str, target: str, success: bool, details: Dict[str, Any] = None):
        """Record individual actions."""
        action_data = {
            'timestamp': datetime.now().isoformat(),
            'action_type': action_type,
            'target': target,
            'success': success,
            'details': str(details) if details else ''
        }
        
        csv_path = f"{self.analytics_dir}/actions.csv"
        self.data_manager.append_to_csv([action_data], csv_path)
    
    def generate_daily_report(self, date: str = None) -> Dict[str, Any]:
        """Generate daily performance report."""
        if not date:
            date = datetime.now().strftime('%Y-%m-%d')
        
        try:
            # Load session data
            sessions_df = pd.read_csv(f"{self.analytics_dir}/sessions.csv")
            sessions_df['date'] = pd.to_datetime(sessions_df['timestamp']).dt.date
            
            # Filter for specific date
            daily_sessions = sessions_df[sessions_df['date'] == pd.to_datetime(date).date()]
            
            if daily_sessions.empty:
                return {"error": f"No data found for {date}"}
            
            # Calculate metrics
            report = {
                'date': date,
                'total_sessions': len(daily_sessions),
                'total_likes': daily_sessions['likes_count'].sum(),
                'total_follows': daily_sessions['follows_count'].sum(),
                'total_comments': daily_sessions['comments_count'].sum(),
                'avg_session_duration': daily_sessions['duration_minutes'].mean(),
                'success_rate': daily_sessions['success_rate'].mean(),
                'most_active_hashtag': self._get_most_active_hashtag(daily_sessions)
            }
            
            # Save report
            report_path = f"{self.analytics_dir}/daily_report_{date}.json"
            self.data_manager.save_to_json(report, report_path)
            
            return report
            
        except FileNotFoundError:
            return {"error": "No analytics data available"}
        except Exception as e:
            self.logger.error(f"Error generating daily report: {str(e)}")
            return {"error": str(e)}
    
    def generate_weekly_report(self) -> Dict[str, Any]:
        """Generate weekly performance report."""
        try:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=7)
            
            sessions_df = pd.read_csv(f"{self.analytics_dir}/sessions.csv")
            sessions_df['timestamp'] = pd.to_datetime(sessions_df['timestamp'])
            
            # Filter for last 7 days
            weekly_sessions = sessions_df[
                (sessions_df['timestamp'] >= start_date) & 
                (sessions_df['timestamp'] <= end_date)
            ]
            
            if weekly_sessions.empty:
                return {"error": "No data found for the past week"}
            
            report = {
                'period': f"{start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}",
                'total_sessions': len(weekly_sessions),
                'total_likes': weekly_sessions['likes_count'].sum(),
                'total_follows': weekly_sessions['follows_count'].sum(),
                'total_comments': weekly_sessions['comments_count'].sum(),
                'avg_daily_likes': weekly_sessions['likes_count'].sum() / 7,
                'avg_daily_follows': weekly_sessions['follows_count'].sum() / 7,
                'best_performing_day': self._get_best_performing_day(weekly_sessions),
                'engagement_trend': self._calculate_engagement_trend(weekly_sessions)
            }
            
            return report
            
        except Exception as e:
            self.logger.error(f"Error generating weekly report: {str(e)}")
            return {"error": str(e)}
    
    def create_performance_charts(self):
        """Create visualization charts for performance metrics."""
        try:
            sessions_df = pd.read_csv(f"{self.analytics_dir}/sessions.csv")
            sessions_df['timestamp'] = pd.to_datetime(sessions_df['timestamp'])
            sessions_df['date'] = sessions_df['timestamp'].dt.date
            
            # Set up the plotting style
            plt.style.use('seaborn-v0_8')
            fig, axes = plt.subplots(2, 2, figsize=(15, 12))
            fig.suptitle('Instagram Bot Performance Analytics', fontsize=16, fontweight='bold')
            
            # Daily activity chart
            daily_activity = sessions_df.groupby('date').agg({
                'likes_count': 'sum',
                'follows_count': 'sum',
                'comments_count': 'sum'
            }).reset_index()
            
            axes[0, 0].plot(daily_activity['date'], daily_activity['likes_count'], marker='o', label='Likes')
            axes[0, 0].plot(daily_activity['date'], daily_activity['follows_count'], marker='s', label='Follows')
            axes[0, 0].plot(daily_activity['date'], daily_activity['comments_count'], marker='^', label='Comments')
            axes[0, 0].set_title('Daily Activity Trends')
            axes[0, 0].set_xlabel('Date')
            axes[0, 0].set_ylabel('Count')
            axes[0, 0].legend()
            axes[0, 0].tick_params(axis='x', rotation=45)
            
            # Success rate distribution
            axes[0, 1].hist(sessions_df['success_rate'], bins=20, alpha=0.7, color='skyblue', edgecolor='black')
            axes[0, 1].set_title('Success Rate Distribution')
            axes[0, 1].set_xlabel('Success Rate (%)')
            axes[0, 1].set_ylabel('Frequency')
            
            # Session duration analysis
            axes[1, 0].boxplot(sessions_df['duration_minutes'])
            axes[1, 0].set_title('Session Duration Analysis')
            axes[1, 0].set_ylabel('Duration (minutes)')
            
            # Hashtag performance (if available)
            if 'target_hashtags' in sessions_df.columns:
                hashtag_performance = sessions_df.groupby('target_hashtags')['likes_count'].sum().head(10)
                axes[1, 1].bar(range(len(hashtag_performance)), hashtag_performance.values)
                axes[1, 1].set_title('Top Performing Hashtags')
                axes[1, 1].set_xlabel('Hashtags')
                axes[1, 1].set_ylabel('Total Likes')
                axes[1, 1].set_xticks(range(len(hashtag_performance)))
                axes[1, 1].set_xticklabels(hashtag_performance.index, rotation=45)
            
            plt.tight_layout()
            chart_path = f"{self.analytics_dir}/performance_charts.png"
            plt.savefig(chart_path, dpi=300, bbox_inches='tight')
            plt.close()
            
            self.logger.info(f"Performance charts saved to {chart_path}")
            return chart_path
            
        except Exception as e:
            self.logger.error(f"Error creating performance charts: {str(e)}")
            return None
    
    def get_engagement_metrics(self) -> Dict[str, float]:
        """Calculate key engagement metrics."""
        try:
            sessions_df = pd.read_csv(f"{self.analytics_dir}/sessions.csv")
            
            if sessions_df.empty:
                return {}
            
            metrics = {
                'avg_likes_per_session': sessions_df['likes_count'].mean(),
                'avg_follows_per_session': sessions_df['follows_count'].mean(),
                'avg_comments_per_session': sessions_df['comments_count'].mean(),
                'overall_success_rate': sessions_df['success_rate'].mean(),
                'total_engagement_actions': (
                    sessions_df['likes_count'].sum() + 
                    sessions_df['follows_count'].sum() + 
                    sessions_df['comments_count'].sum()
                ),
                'avg_session_duration': sessions_df['duration_minutes'].mean()
            }
            
            return metrics
            
        except Exception as e:
            self.logger.error(f"Error calculating engagement metrics: {str(e)}")
            return {}
    
    def _get_most_active_hashtag(self, sessions_df: pd.DataFrame) -> str:
        """Get the most frequently used hashtag."""
        try:
            if 'target_hashtags' in sessions_df.columns:
                hashtag_counts = sessions_df['target_hashtags'].value_counts()
                return hashtag_counts.index[0] if not hashtag_counts.empty else "N/A"
            return "N/A"
        except:
            return "N/A"
    
    def _get_best_performing_day(self, sessions_df: pd.DataFrame) -> str:
        """Get the day with highest engagement."""
        try:
            sessions_df['day'] = sessions_df['timestamp'].dt.day_name()
            daily_engagement = sessions_df.groupby('day')['likes_count'].sum()
            return daily_engagement.idxmax()
        except:
            return "N/A"
    
    def _calculate_engagement_trend(self, sessions_df: pd.DataFrame) -> str:
        """Calculate if engagement is trending up or down."""
        try:
            sessions_df = sessions_df.sort_values('timestamp')
            first_half = sessions_df.iloc[:len(sessions_df)//2]['likes_count'].mean()
            second_half = sessions_df.iloc[len(sessions_df)//2:]['likes_count'].mean()
            
            if second_half > first_half:
                return "Increasing"
            elif second_half < first_half:
                return "Decreasing"
            else:
                return "Stable"
        except:
            return "Unknown"