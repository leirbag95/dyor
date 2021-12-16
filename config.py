import os
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

class Config:
    
    TWITTER_JSON_PATH='.data/twitter/account.json'

    DISCORD_WEBHOOK = os.getenv('DISCORD_WEBHOOK')
    
    TWITTER_ACCESS_TOKEN = os.getenv('TWITTER_ACCESS_TOKEN')
    TWITTER_ACCESS_TOKEN_SECRET = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
    TWITTER_CONSUMER_KEY = os.getenv('TWITTER_CONSUMER_KEY')
    TWITTER_CONSUMER_SECRET = os.getenv('TWITTER_CONSUMER_SECRET')