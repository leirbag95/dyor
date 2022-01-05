import discord
from discord import Webhook, RequestsWebhookAdapter
from config import Config as cfg
import click

class Message:

    @classmethod
    def send(self, argv, message_t):
        """Send message through all channel

        Args:
            argv (dict): metadata of message
            message_t (str): type of alert
        """
        if message_t == cfg.MESSAGE_T.TWITTER:
            embed = self.twitter_body_discord(argv)
        if message_t == cfg.MESSAGE_T.TX:
            embed = self.tx_body_discord(argv)
        
        self.send_discord(embed)

    @classmethod
    def tx_body_discord(self, argv):
        """return embeded discord body

        Args:
            argv (dict): metadata of message

        Returns:
            Embed: Embed discord message ready to send
        """
        username = argv.get('username', 'No Username')
        block_height = argv.get('block_height')
        block_signed_at = argv.get('block_signed_at')
        chain_id = argv.get('chain_id')
        tx_hash = argv.get('tx_hash')

        with open(cfg.FILE_NETWORKS, 'r') as json_file:
            networks = json.load(json_file)

        body = f"A new event took place from **{username}** at the block **{block_height} ({block_signed_at})** of chain id **{chain_id}**. Here the tx hash: **{tx_hash}**\n"

        #discord body message style
        embed = discord.Embed(description=body,
                        color=0xFF5733)
        
        embed.set_author(name='New TX 📒 ', 
                    icon_url='https://upload.wikimedia.org/wikipedia/commons/6/6f/Ethereum-icon-purple.svg')
        
        embed.add_field(name="Network", value=networks.get(str(chain_id), chain_id))
        embed.add_field(name="Block", value=f"{block_height} ({block_signed_at})")
        embed.add_field(name="Username", value=username)

        events = argv.get('events', [])

        for event in events:
            name = event.get('name', 'No name')
            sender_contract_ticker_symbol = event.get('sender_contract_ticker_symbol')
            sender_name = event.get('sender_name')
            from_address = '..'.join([event.get('from_address', '')[0:5], event.get('from_address', '')[-5:]])
            to_address = '..'.join([event.get('to_address', '')[0:5], event.get('to_address', '')[-5:]])
            value = f"from {from_address} to {to_address} for {event.get('value', 0)} {sender_contract_ticker_symbol} ({sender_name})"

            embed.add_field(name=event.get('name', 'No name'), value=value, inline=False)
        
        return embed

    @classmethod
    def twitter_body_discord(self, argv):
        """return embeded discord body for twitter alert

        Args:
            argv (dict): metadata of message

        Returns:
            Embed: Embed discord message ready to send
        """
        username = argv.get('username', 'No Username')
        target = argv.get('target', 'No Target') # url which has been followed

        body = f"New following alert from **@{username}** (https://twitter.com/@{username})"

        #discord body message style
        embed = discord.Embed(description=body,
                        color=0xFF5733)
        
        embed.set_author(name='New Twitter Alert 🐦 ', 
                    icon_url='https://upload.wikimedia.org/wikipedia/commons/6/6f/Ethereum-icon-purple.svg')
        
        embed.add_field(name="New account", value=target, inline=False)
        
        return embed

    @classmethod
    def send_discord(self, embed):
        """Send message on discord

        Args:
            embed (Embed): Embed discord body
        """
        webhook = Webhook.from_url(cfg.DISCORD_WEBHOOK, adapter=RequestsWebhookAdapter())

        webhook.send(embed=embed)