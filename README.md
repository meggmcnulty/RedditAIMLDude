# Reddit AI/ML Discussion Bot

This bot automatically engages with AI and machine learning discussions on Reddit by posting thoughtful, helpful comments. It runs 6 times per day (every 4 hours) and focuses on the top 20 AI/ML-related subreddits.

## Features

- Posts thoughtful comments on AI/ML discussions
- Runs 6 times per day (every 4 hours)
- Focuses on English content only
- Targets top 20 AI/ML subreddits
- Uses GPT-4 for generating high-quality comments
- Tracks activity to prevent duplicate comments
- Includes comprehensive logging
- Language detection to ensure English-only content

## Prerequisites

- Python 3.8 or higher
- Reddit API credentials (set up as a **script** app)
- OpenAI API key

## Setup

1. Clone this repository:
```bash
git clone https://github.com/meggmcnulty/RedditAIMLDude.git
cd RedditAIMLDude
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project root with your API credentials. **Do not use your real keys in the README or commit them to GitHub!**

Example `.env` file:
```
REDDIT_CLIENT_ID=your_personal_use_script
REDDIT_CLIENT_SECRET=your_secret
REDDIT_USERNAME=your_reddit_username
REDDIT_PASSWORD=your_reddit_password
OPENAI_API_KEY=your_openai_api_key
```

To get Reddit API credentials:
1. Go to https://www.reddit.com/prefs/apps
2. Click "create another app..."
3. Fill in the required information
4. Select **"script"** as the application type
5. Use "http://localhost:8080" as the redirect URI
6. Note down the client ID (personal use script) and client secret

## Usage

Run the bot:
```bash
python reddit_bot.py
```

Or, for a single test run (shows the comment before posting):
```bash
python test_bot.py
```

The bot will:
- Start running immediately
- Post comments every 4 hours
- Log all activity to `bot.log`
- Store comment history in `bot_activity.db`

To stop the bot, press Ctrl+C. The bot will perform a clean shutdown.

## Configuration

You can modify the bot's behavior by editing `config.py`:

- `TARGET_SUBREDDITS`: List of subreddits to monitor
- `COMMENT_INTERVAL_HOURS`: Time between comments
- `MAX_COMMENTS_PER_DAY`: Maximum comments per day
- `MIN_POST_SCORE`: Minimum score for posts to engage with
- `MAX_POST_AGE_HOURS`: Maximum age of posts to comment on
- `MIN_COMMENT_LENGTH`: Minimum length for generated comments
- `MAX_COMMENT_LENGTH`: Maximum length for generated comments

## Safety Features

- Language detection to ensure English-only content
- Comment length limits
- Post age and score thresholds
- Duplicate comment prevention
- Rate limiting through scheduling
- Comprehensive error handling and logging

## Monitoring

The bot logs all activity to `bot.log`. You can monitor the bot's behavior by checking this file:
```bash
tail -f bot.log
```

## Contributing

Feel free to submit issues and enhancement requests! 