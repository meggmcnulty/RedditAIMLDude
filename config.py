import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Reddit API credentials
REDDIT_CLIENT_ID = os.getenv('REDDIT_CLIENT_ID')
REDDIT_CLIENT_SECRET = os.getenv('REDDIT_CLIENT_SECRET')
REDDIT_USERNAME = os.getenv('REDDIT_USERNAME')
REDDIT_PASSWORD = os.getenv('REDDIT_PASSWORD')
REDDIT_USER_AGENT = 'AI/ML Discussion Bot v1.0'

# OpenAI API credentials
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Target subreddits (AI/ML focused)
TARGET_SUBREDDITS = [
    'artificial',
    'MachineLearning',
    'AIdev',
    'OpenAI',
    'ChatGPT',
    'GPT3',
    'GPT4',
    'StableDiffusion',
    'dalle2',
    'midjourney',
    'learnmachinelearning',
    'datascience',
    'computervision',
    'nlp',
    'deeplearning',
    'reinforcementlearning',
    'tensorflow',
    'pytorch',
    'MLQuestions',
    'AIethics'
]

# Bot behavior settings
COMMENT_INTERVAL_HOURS = 4  # Post every 4 hours
MAX_COMMENTS_PER_DAY = 6
MIN_POST_SCORE = 10  # Minimum score for posts to engage with
MAX_POST_AGE_HOURS = 24  # Don't comment on posts older than 24 hours
MIN_COMMENT_LENGTH = 100  # Minimum length for generated comments
MAX_COMMENT_LENGTH = 500  # Maximum length for generated comments

# Database settings
DB_FILE = 'bot_activity.db'

# Comment generation settings
TEMPERATURE = 0.7
MAX_TOKENS = 400  # Increased to allow for 1-4 paragraphs
SYSTEM_PROMPT = """You are an AI expert who writes in the style of James Owen Weatherall - thoughtful, accessible, and insightful. Your comments should:

1. Be written in a warm, engaging tone that makes complex ideas accessible
2. Always include at least one practical tip, recommendation, or actionable insight
3. Be structured in 1-4 clear paragraphs
4. Use analogies and real-world examples to illustrate points
5. Acknowledge both the strengths and limitations of ideas
6. Be genuinely helpful and supportive to the original poster
7. Avoid technical jargon unless necessary, and explain it when used
8. Draw connections between the post and broader AI/ML concepts
9. Be written in clear, elegant English
10. Maintain a balance between being informative and conversational

Your goal is to be as helpful as possible while maintaining the thoughtful, accessible style of James Owen Weatherall's writing.""" 