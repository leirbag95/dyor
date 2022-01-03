import os
from dotenv import load_dotenv
from enum import Enum

load_dotenv()  # take environment variables from .env.

class Config:

    #MESSAGE TYPE
    class MESSAGE_T(Enum):
        TWITTER = 'Twitter'
        TX = 'Tx'

    DISCORD_WEBHOOK = os.getenv('DISCORD_WEBHOOK')
    
    TWITTER_ACCESS_TOKEN        = os.getenv('TWITTER_ACCESS_TOKEN')
    TWITTER_ACCESS_TOKEN_SECRET = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
    TWITTER_CONSUMER_KEY        = os.getenv('TWITTER_CONSUMER_KEY')
    TWITTER_CONSUMER_SECRET     = os.getenv('TWITTER_CONSUMER_SECRET')

    COVALENT_API_KEY = os.getenv('COVALENT_API_KEY')

    FILE_TWITTER_QUEUE   = '.data/twitter/queue.json'
    FILE_TWITTER_ACCOUNT = '.data/twitter/account.json'
    
    FILE_WALLET_QUEUE = '.data/wallet/queue.json'