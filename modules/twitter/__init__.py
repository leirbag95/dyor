from config import Config as cfg
DATA_FILE = cfg.FILE_TWITTER_QUEUE #source file
MAX_FETCHED_ACCOUNT = 10 #max account to fetch

from modules.twitter.models import Twitter