import os
import tweepy
import json
import requests
from discord import Webhook, RequestsWebhookAdapter
from config import Config as cfg
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
        
        with open(DATA_FILE) as f:
            self.data = json.load(f)
        
        self.api = tweepy.API(auth)
    
    def __logs__(self, message, with_discord=True):
        ''' manage logs and notification (like discord, telegram...) '''

        click.echo(message)

        if with_discord:
            try:
                self.webhook.send(message)
            except Exception as e:
                raise Exception('discord notification error: {0}'.format(str(e)))

    def update_file(self, data):
        ''' update cache from data '''
        with open(DATA_FILE, 'w') as json_file:
            json.dump(self.data, json_file)

    def fetch_new_following(self, screen_name):
        """ return list of new account followed by `screen_name` """
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
                message = 'New following alert from @{0}: https://twitter.com/@{1}'.format(screen_name, user.screen_name)
                self.__logs__(message, self.with_discord)
        except Exception as e:
            raise Exception('twitter error: {0}'.format(screen_name))