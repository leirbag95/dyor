import os
from os import path
import tweepy
import json
import requests
from discord import Webhook, RequestsWebhookAdapter
from config import Config as cfg
from modules.message import Message
import click

from modules.twitter import DATA_FILE, MAX_FETCHED_ACCOUNT

class Twitter():

    def __init__(self, with_discord=True):
        self.with_discord = with_discord

        if with_discord:
            self.webhook = Webhook.from_url(cfg.DISCORD_WEBHOOK, adapter=RequestsWebhookAdapter())
        
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
    
    
    def update_file(self, data):
        ''' update cache from data '''
        with open(DATA_FILE, 'w') as json_file:
            json.dump(self.data, json_file)
            json_file.close()

    def fetch_new_following(self, screen_name):
        """Retrieve all last 10 accounts followed by `screen_name`

        Args:
            screen_name (str): twitter username (without @)

        Raises:
            Exception: An error related to twitter, usually it can be due to a 
            twitter account that does not exist
        """
        with open(DATA_FILE) as f:
            self.data = json.load(f)

        last_friend = self.data.get(screen_name)
        try:
            for (index, user) in enumerate(tweepy.Cursor(self.api.friends, screen_name=screen_name, wait_on_rate_limit=True).items(MAX_FETCHED_ACCOUNT)):
                if index == 0:
                    new_last_friend = user.id_str
                elif index == MAX_FETCHED_ACCOUNT - 1:
                    #store first user_id to the cache
                    self.data[screen_name] = new_last_friend
                    self.update_file(self.data)

                if not last_friend:
                    #not in cache
                    self.data[screen_name] = user.id_str
                    self.update_file(self.data)
                    break

                if user.id_str == last_friend:
                    #reach last friend stored
                    self.data[screen_name] = new_last_friend
                    self.update_file(self.data)
                    break
                
                obj = {
                    'username': screen_name,
                    'target': 'https://twitter.com/@{0}'.format(user.screen_name)
                }
                Message.send(obj, cfg.MESSAGE_T.TWITTER)
                f.close()
        except Exception as e:
            raise Exception('twitter error: {0}'.format(screen_name))