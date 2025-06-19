# Instagram Bot - Professional Automation Tool

A sophisticated Instagram automation bot built with Python, featuring intelligent engagement, content management, and analytics capabilities.

## 🚀 Features

- **Smart Following/Unfollowing**: Target users based on hashtags, locations, and user interactions
- **Intelligent Liking**: Like posts with customizable filters and rate limiting
- **Comment Management**: Post contextual comments with anti-spam protection
- **Analytics Dashboard**: Track performance metrics and engagement rates
- **Safety First**: Built-in rate limiting and Instagram API compliance
- **Configurable Settings**: Easy-to-modify configuration for different strategies

## 📋 Requirements

- Python 3.8+
- Instagram account
- Stable internet connection

## 🛠️ Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd instagram-bot
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure your settings:
```bash
cp config/config_template.json config/config.json
```

4. Update `config/config.json` with your Instagram credentials and preferences.

## 🎯 Usage

### Basic Usage
```python
from src.instagram_bot import InstagramBot

bot = InstagramBot()
bot.login()
bot.start_automation()
```

### Advanced Usage
See the `Instagram_Bot_Tutorial.ipynb` notebook for detailed examples and explanations.

## 📊 Project Structure

```
instagram-bot/
├── src/
│   ├── instagram_bot.py      # Main bot class
│   ├── engagement.py         # Engagement strategies
│   ├── analytics.py          # Analytics and reporting
│   └── utils.py             # Utility functions
├── config/
│   ├── config.json          # Configuration file
│   └── config_template.json # Template configuration
├── data/
│   ├── logs/               # Bot activity logs
│   └── analytics/          # Analytics data
├── notebooks/
│   └── Instagram_Bot_Tutorial.ipynb
├── requirements.txt
└── README.md
```

## ⚙️ Configuration

Key configuration options in `config/config.json`:

- `username`: Your Instagram username
- `password`: Your Instagram password
- `target_hashtags`: Hashtags to target for engagement
- `daily_follows`: Maximum follows per day
- `daily_likes`: Maximum likes per day
- `comment_probability`: Probability of commenting (0-1)

## 📈 Analytics

The bot provides comprehensive analytics including:
- Engagement rates
- Follower growth
- Activity logs
- Performance metrics

## ⚠️ Important Notes

- **Rate Limiting**: The bot includes built-in delays to avoid Instagram's rate limits
- **Account Safety**: Use responsibly to avoid account restrictions
- **Terms of Service**: Ensure compliance with Instagram's Terms of Service
- **Testing**: Always test with a secondary account first

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is for educational purposes only. Use responsibly and in accordance with Instagram's Terms of Service.

## 🔧 Troubleshooting

Common issues and solutions:

1. **Login Issues**: Check credentials and 2FA settings
2. **Rate Limiting**: Reduce activity rates in configuration
3. **Element Not Found**: Instagram may have updated their interface

For more help, check the Jupyter notebook tutorial or open an issue.

## 📞 Support

For questions and support, please refer to the documentation in the Jupyter notebook or create an issue in the repository.