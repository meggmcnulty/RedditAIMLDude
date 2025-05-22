import praw
import openai
import random
import time
from datetime import datetime, timedelta
import schedule
import logging
from textblob import TextBlob
import config
from db_handler import DatabaseHandler

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler()
    ]
)

class RedditBot:
    def __init__(self):
        # Initialize Reddit client
        self.reddit = praw.Reddit(
            client_id=config.REDDIT_CLIENT_ID,
            client_secret=config.REDDIT_CLIENT_SECRET,
            username=config.REDDIT_USERNAME,
            password=config.REDDIT_PASSWORD,
            user_agent=config.REDDIT_USER_AGENT
        )
        
        # Initialize OpenAI client
        openai.api_key = config.OPENAI_API_KEY
        
        # Initialize database handler
        self.db = DatabaseHandler()
        
        logging.info("Bot initialized successfully")
    
    def is_english(self, text):
        """Check if text is primarily English using TextBlob."""
        try:
            blob = TextBlob(text)
            return blob.detect_language() == 'en'
        except:
            return False
    
    def generate_comment(self, post_title, post_content, post_url):
        """Generate a thoughtful comment using OpenAI's API."""
        try:
            prompt = f"""Post Title: {post_title}
Post Content: {post_content}
Post URL: {post_url}

Write a thoughtful, helpful comment in the style of James Owen Weatherall that:
1. Is structured in 1-4 clear paragraphs
2. Includes at least one practical tip or recommendation
3. Makes complex ideas accessible through analogies or examples
4. Addresses the specific needs or questions in the post
5. Is between {config.MIN_COMMENT_LENGTH} and {config.MAX_COMMENT_LENGTH} characters
6. Maintains a warm, engaging tone while being informative

Focus on being genuinely helpful to the original poster while making connections to broader AI/ML concepts.

Comment:"""

            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": config.SYSTEM_PROMPT},
                    {"role": "user", "content": prompt}
                ],
                temperature=config.TEMPERATURE,
                max_tokens=config.MAX_TOKENS
            )
            
            comment = response.choices[0].message.content.strip()
            
            # Verify comment length, language, and paragraph count
            if (len(comment) < config.MIN_COMMENT_LENGTH or 
                len(comment) > config.MAX_COMMENT_LENGTH or 
                not self.is_english(comment) or
                comment.count('\n\n') > 3):  # Ensure no more than 4 paragraphs
                return None
                
            return comment
            
        except Exception as e:
            logging.error(f"Error generating comment: {str(e)}")
            return None
    
    def find_suitable_post(self):
        """Find a suitable post to comment on."""
        for subreddit_name in config.TARGET_SUBREDDITS:
            try:
                subreddit = self.reddit.subreddit(subreddit_name)
                
                # Get hot posts from the last 24 hours
                for post in subreddit.hot(limit=20):
                    # Skip if post is too old
                    post_age = datetime.now() - datetime.fromtimestamp(post.created_utc)
                    if post_age > timedelta(hours=config.MAX_POST_AGE_HOURS):
                        continue
                    
                    # Skip if post score is too low
                    if post.score < config.MIN_POST_SCORE:
                        continue
                    
                    # Skip if we've already commented on this post
                    if self.db.has_commented_on_post(post.id):
                        continue
                    
                    # Skip if post is not in English
                    if not self.is_english(post.title + " " + post.selftext):
                        continue
                    
                    return post
                    
            except Exception as e:
                logging.error(f"Error processing subreddit {subreddit_name}: {str(e)}")
                continue
        
        return None
    
    def post_comment(self):
        """Main function to find a post and post a comment."""
        if not self.db.can_post_today():
            logging.info("Daily comment limit reached")
            return
        
        if not self.db.can_post_now():
            logging.info("Waiting for comment interval")
            return
        
        post = self.find_suitable_post()
        if not post:
            logging.info("No suitable posts found")
            return
        
        comment_text = self.generate_comment(
            post.title,
            post.selftext,
            f"https://reddit.com{post.permalink}"
        )
        
        if not comment_text:
            logging.info("Failed to generate suitable comment")
            return
        
        try:
            comment = post.reply(comment_text)
            self.db.add_comment(post.id, comment.id, post.subreddit.display_name)
            logging.info(f"Successfully posted comment on r/{post.subreddit.display_name}")
            
        except Exception as e:
            logging.error(f"Error posting comment: {str(e)}")
    
    def run(self):
        """Run the bot on a schedule."""
        logging.info("Starting bot...")
        
        # Schedule the bot to run every 4 hours
        schedule.every(config.COMMENT_INTERVAL_HOURS).hours.do(self.post_comment)
        
        # Run immediately on startup
        self.post_comment()
        
        while True:
            try:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
            except Exception as e:
                logging.error(f"Error in main loop: {str(e)}")
                time.sleep(300)  # Wait 5 minutes before retrying
    
    def cleanup(self):
        """Clean up resources."""
        self.db.close()
        logging.info("Bot shutdown complete")

if __name__ == "__main__":
    bot = RedditBot()
    try:
        bot.run()
    except KeyboardInterrupt:
        logging.info("Shutting down bot...")
        bot.cleanup() 