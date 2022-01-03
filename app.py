#!bin/python3
import os
from dotenv import load_dotenv
import json
from datetime import datetime as dt
import click
from config import Config as cfg
from modules.twitter import Twitter
from modules.wallet import Wallet

load_dotenv()  # take environment variables from .env.


@click.group()
def cli():
    pass

@click.command()
@click.option("--screen_name", prompt="Twitter screen name", help="Twitter screen name")
def add_twitter_target(screen_name):
    ''' add twitter target to the queue'''
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
@click.option("--with_discord", default='y', prompt="Send on discord (Y/n)", help="Send on discord")
def listen_twitter(with_discord):
    ''' listen twitter following account '''
    
    click.echo('listening twitter...')
    
    w_discord = True

    if with_discord.lower() == 'n':
        w_discord = False

    twitter = Twitter(w_discord)

    with open(cfg.FILE_TWITTER_ACCOUNT, 'r') as json_file:
        json_decoded = json.load(json_file)

    for key, value in json_decoded.items():
        twitter.fetch_new_following(key)

@click.command()
@click.option("--chain_id", default=1, prompt="Select specific network", help="Selected network to listen")
def listen_single_network(chain_id):
    click.echo('listening...')
    
    wallet = Wallet()
    
    with open(cfg.FILE_WALLET_QUEUE, 'r') as json_file:
        json_decoded = json.load(json_file)

    for key, value in json_decoded.items():
        address = key
        last_block = value.get(str(chain_id), {}).get('last_block', 0)
        username = value.get('username')
        user = {
            'address': address,
            'username': username,
            'last_block': last_block
        }
        wallet.listen_single_network(user, chain_id=chain_id)

@click.command()
@click.option("--address", prompt="Address you want to listen", help="Address you want to listen")
@click.option("--username", prompt="Give a username to address", help="Give username's address")
def add_address(address, username):
    ''' add new address target to the queue'''
    with open(cfg.FILE_WALLET_QUEUE) as json_file:
        json_decoded = json.load(json_file)

    if address in json_decoded:
        click.echo('address already added to the queue')
        return False

    json_decoded[address] = {
        'username': username,
        'datetime': str(dt.now())
    }
    with open(cfg.FILE_WALLET_QUEUE, 'w') as json_file:
        json.dump(json_decoded, json_file)
    
    json_file.close()

    click.echo('address added to the queue')

@click.command()
@click.option("--address", prompt="Wallet address", help="Wallet address")
def del_wallet_target(address):
    ''' delete wallet target from the queue'''
    with open(cfg.FILE_WALLET_QUEUE) as json_file:
        json_decoded = json.load(json_file)

    if not address in json_decoded:
        click.echo('wallet not in the queue')
        return False

    del json_decoded[address]

    with open(cfg.FILE_WALLET_QUEUE, 'w') as json_file:
        json.dump(json_decoded, json_file)
    
    json_file.close()

    click.echo('wallet deleted from the queue')

@click.command()
def show_wallet_queue():
    ''' show current twitter queue '''
    with open(cfg.FILE_WALLET_QUEUE) as json_file:
        json_decoded = json.load(json_file)
    
    click.echo('Number of element: {0}'.format(len(json_decoded)))
    for key, value in json_decoded.items():
        click.echo((key, value))
    json_file.close()


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
    cli.add_command(listen_single_network)
    cli.add_command(add_address)
    cli.add_command(show_wallet_queue)
    cli.add_command(del_wallet_target)
    cli.add_command(listen_twitter)
    
    cli()
