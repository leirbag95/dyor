import os
from os import path
import tweepy
import json
import requests
from discord import Webhook, RequestsWebhookAdapter
from config import Config as cfg
from modules.message import Message
import click

from modules.twitter import MAX_FETCHED_ACCOUNT
from models.twitter import Queue as TwtQueue

class Twitter():

    def __init__(self):
        
        access_token = cfg.TWITTER_ACCESS_TOKEN
        access_token_secret = cfg.TWITTER_ACCESS_TOKEN_SECRET
        
        consumer_key = cfg.TWITTER_CONSUMER_KEY
        consumer_secret = cfg.TWITTER_CONSUMER_SECRET

        try:
            auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        except Exception as e:
            raise Exception('auth error: {0}'.format(str(e)))

        try:
            auth.set_access_token(access_token, access_token_secret)
        except Exception as e:
            raise Exception('auth error: {0}'.format(str(e)))
        
        self.api = tweepy.API(auth)
    

    def fetch_new_following(self, screen_name):
        """Retrieve all last 10 accounts followed by `screen_name`

        Args:
            screen_name (str): twitter username (without @)

        Raises:
            Exception: An error related to twitter, usually it can be due to a 
            twitter account that does not exist
        """
        twt_queue = TwtQueue(cfg.FILE_TWITTER_QUEUE)
        
        data = twt_queue.get_all()

        last_friend = data.get(screen_name)
        try:
            for (index, user) in enumerate(tweepy.Cursor(self.api.friends, screen_name=screen_name, wait_on_rate_limit=True).items(MAX_FETCHED_ACCOUNT)):
                if index == 0:
                    new_last_friend = user.id_str
                elif index == MAX_FETCHED_ACCOUNT - 1:
                    #store first user_id to the cache
                    self.data[screen_name] = new_last_friend
                    twt_queue.update(screen_name, new_last_friend)

                if not last_friend:
                    #not in cache
                    self.data[screen_name] = user.id_str
                    twt_queue.update(screen_name, user.id_str)
                    break

                if user.id_str == last_friend:
                    #reach last friend stored
                    twt_queue.update(screen_name, new_last_friend)
                    break
                
                obj = {
                    'username': screen_name,
                    'target': 'https://twitter.com/@{0}'.format(user.screen_name)
                }
                try:
                    Message.send(obj, cfg.MESSAGE_T.TWITTER)
                except Exception as e:
                    click.echo(str(e))

        except Exception as e:
            raise Exception('twitter error: {0}'.format(screen_name))