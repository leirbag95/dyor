#!bin/python3
import os
from dotenv import load_dotenv
import json
from datetime import datetime as dt
import click
from config import Config as cfg
from modules.twitter import Twitter

load_dotenv()  # take environment variables from .env.


@click.group()
def cli():
    pass

@click.command()
@click.option("--screen_name", prompt="Twitter screen name", help="Twitter screen name")
def add_twitter_target(screen_name):
    ''' add twitter target to the queue'''
    print(cfg.FILE_TWITTER_ACCOUNT)
    with open(cfg.FILE_TWITTER_ACCOUNT) as json_file:
        json_decoded = json.load(json_file)

    if screen_name in json_decoded:
        click.echo('screen name already added to the queue')
        return False

    json_decoded[screen_name] = str(dt.now())
    with open(cfg.FILE_TWITTER_ACCOUNT, 'w') as json_file:
        json.dump(json_decoded, json_file)
    
    json_file.close()

    click.echo('screen name added to the queue')

@click.command()
@click.option("--screen_name", prompt="Twitter screen name", help="Twitter screen name")
def del_twitter_target(screen_name):
    ''' delete twitter target from the queue'''
    with open(cfg.FILE_TWITTER_ACCOUNT) as json_file:
        json_decoded = json.load(json_file)

    if not screen_name in json_decoded:
        click.echo('screen name not in the queue')
        return False

    del json_decoded[screen_name]

    with open(cfg.FILE_TWITTER_ACCOUNT, 'w') as json_file:
        json.dump(json_decoded, json_file)
    
    json_file.close()

    click.echo('screen name deleted from the queue')

@click.command()
def show_twitter_queue():
    ''' show current twitter queue '''
    with open(cfg.FILE_TWITTER_ACCOUNT) as json_file:
        json_decoded = json.load(json_file)
    
    click.echo('Number of element: {0}'.format(len(json_decoded)))
    for key, value in json_decoded.items():
        click.echo((key, value))
    json_file.close()

@click.command()
@click.option("--with_discord", prompt="Send on discord (Y/n)", help="Send on discord")
def run(with_discord):
    ''' run dyor program '''
    
    click.echo('running...')
    
    w_discord = True

    if with_discord.lower() == 'n':
        w_discord = False

    twitter = Twitter(w_discord)

    with open(cfg.FILE_TWITTER_ACCOUNT, 'r') as json_file:
        json_decoded = json.load(json_file)

    for key, value in json_decoded.items():
        twitter.fetch_new_following(key)

if __name__ == "__main__":
    ascii_art = '''
 /$$$$$$$  /$$     /$$ /$$$$$$  /$$$$$$$ 
| $$__  $$|  $$   /$$//$$__  $$| $$__  $$
| $$  \ $$ \  $$ /$$/| $$  \ $$| $$  \ $$
| $$  | $$  \  $$$$/ | $$  | $$| $$$$$$$/
| $$  | $$   \  $$/  | $$  | $$| $$__  $$
| $$  | $$    | $$   | $$  | $$| $$  \ $$
| $$$$$$$/    | $$   |  $$$$$$/| $$  | $$
|_______/     |__/    \______/ |__/  |__/

'''

    # print(ascii_art)
    # func list
    cli.add_command(add_twitter_target)
    cli.add_command(del_twitter_target)
    cli.add_command(show_twitter_queue)
    cli.add_command(run)
    
    cli()
