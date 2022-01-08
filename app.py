#!bin/python3
import os
from dotenv import load_dotenv
import json
from datetime import datetime as dt
import click
from config import Config as cfg
from modules.twitter import Twitter
from modules.wallet import Wallet
from models.twitter import Queue as TwtQueue, Account as TwtAccount
from models.wallet import Queue as WQueue

load_dotenv()  # take environment variables from .env.

@click.group()
def cli():
    pass

@click.command()
@click.option("--screen_name", prompt="Twitter screen name", help="Twitter screen name")
def add_twitter(screen_name):
    ''' add twitter target to the queue'''
    twtAccount = TwtAccount(cfg.FILE_TWITTER_ACCOUNT)
    
    if twtAccount.is_exist(screen_name):
        click.echo('screen name already added to the queue')
    else:
        twtAccount.update(screen_name)
        click.echo('screen name added to the queue')

@click.command()
@click.option("--screen_name", prompt="Twitter screen name", help="Twitter screen name")
def del_twitter(screen_name):
    ''' delete twitter target from the queue'''
    twtAccount = TwtAccount(cfg.FILE_TWITTER_ACCOUNT)
    
    if not twtAccount.is_exist(screen_name):
        click.echo('screen name does not exist')
    else:
        twtAccount.delete(screen_name)
        click.echo('screen name deleted from the queue')

@click.command()
def show_twitter():
    ''' show current twitter queue '''
    twtAccount = TwtAccount(cfg.FILE_TWITTER_ACCOUNT)
    click.echo(twtAccount.get_all())

@click.command()
def listen_twitter():
    ''' listen twitter following account '''
    
    click.echo('listening twitter...')
    
    twtAccount = TwtAccount(cfg.FILE_TWITTER_ACCOUNT)
    
    twitter = Twitter()

    t_account = twtAccount.get_all()
    
    for key, value in t_account.items():
        try:
            twitter.fetch_new_following(key)
        except Exception as e:
            click.echo(str(e))

@click.command()
@click.option("--chain_id", default=1, prompt="Select specific network", help="Selected network to listen")
def listen_single_network(chain_id):
    click.echo('listening...')
    
    wallet = Wallet()
    w_queue = WQueue(cfg.FILE_WALLET_QUEUE)

    queue_addresses = w_queue.get_all()

    for key, value in queue_addresses.items():
        address = key
        last_block = value.get(str(chain_id), '1')
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
    wallet = Wallet()
    w_queue = WQueue(cfg.FILE_WALLET_QUEUE)

    queue_addresses = w_queue.get_all()

    if w_queue.is_exist(address):
        click.echo('address already added to the queue')
    else:
        w_queue.update(address, username)
        click.echo('address added to the queue')

@click.command()
@click.option("--address", prompt="Wallet address", help="Wallet address")
def del_wallet_target(address):
    ''' delete wallet target from the queue'''
    wallet = Wallet()
    w_queue = WQueue(cfg.FILE_WALLET_QUEUE)

    queue_addresses = w_queue.get_all()

    if not w_queue.is_exist(address):
        click.echo('wallet not in the queue')
    else:
        w_queue.delete(address)
        click.echo('wallet deleted from the queue')

@click.command()
def show_wallets():
    ''' show current twitter queue '''
    wallet = Wallet()
    w_queue = WQueue(cfg.FILE_WALLET_QUEUE)

    queue_addresses = w_queue.get_all()
    
    click.echo('Number of element: {0}'.format(len(queue_addresses)))
    for key, value in queue_addresses.items():
        click.echo((key, value))

if __name__ == "__main__":
    # func list
    cli.add_command(add_twitter)
    cli.add_command(del_twitter)
    cli.add_command(show_twitter)
    cli.add_command(listen_single_network)
    cli.add_command(add_address)
    cli.add_command(show_wallets)
    cli.add_command(del_wallet_target)
    cli.add_command(listen_twitter)
    
    cli()
