## 🤔 The Problem

We've all been there - your girlfriend sends you dozens of Instagram reels daily, expecting reactions and comments on each one.

## 💡 The Solution

This script automatically:
1. Monitors incoming Telegram messages from your girlfriend
2. Detects Instagram reel links
3. Uses AI (Claude via Hyperbrowser) to analyze the reel content
4. Generates and sends natural, contextual responses

All without you having to watch a single reel!

## 🛠️ How It Works

The system architecture combines:
- Telegram API for message monitoring
- Hyperbrowser for web scraping and AI integration
- Claude AI for content analysis and response generation

## 🚀 Setup Instructions

### Prerequisites
- Python 3.6+
- Telegram account
- Hyperbrowser API key

### Environment Variables
Create a `.env` file with the following:
```
HYPERBROWSER_API_KEY=your_hyperbrowser_api_key
TELEGRAM_API_ID=your_telegram_api_id
TELEGRAM_API_HASH=your_telegram_api_hash
TELEGRAM_PHONE=your_phone_number_with_country_code
GIRLFRIEND_USERNAME=her_telegram_username
```

### Getting API Keys
1. **Hyperbrowser API Key**: Sign up at [hyperbrowser.ai](https://hyperbrowser.ai) and get your key from [app.hyperbrowser.ai](https://app.hyperbrowser.ai)
2. **Telegram API Credentials**: Visit [my.telegram.org/auth](https://my.telegram.org/auth), log in, and create API credentials in the "API development tools" section

### Installation

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install telethon requests python-dotenv
```

### Running the Script

```bash
python tg_auto_react.py
```

On first run, you'll be prompted to authenticate your Telegram account.

## 🧠 Behind the Scene

The script uses Model Context Protocol (MCP) architecture to connect AI models with data sources - specifically connecting Claude to Telegram.

## 🤣 Use Responsibly

This project was created as a fun experiment. Use it responsibly and ethically - honesty in relationships is still the best policy!

*Disclaimer: This project is meant for educational and entertainment purposes. The creator takes no responsibility for any relationship issues that may arise from its use.*