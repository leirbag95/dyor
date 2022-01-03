import json
from web3 import Web3
import requests
import time
from config import Config
from modules.message.models import Message

class Wallet:

    def __init__(self, api="https://api.covalenthq.com/v1/"):
        self.api = api
        
    def listen_single_network(self, user, chain_id=1):
        ''' listen events on specific network '''

        address = user.get('address')
        last_block = user.get('last_block', 0)
        username = user.get('username')

        with open(Config.FILE_WALLET_QUEUE) as f:
            address_queue = json.load(f)
        
        url = f"{self.api}{chain_id}/address/{address}/transactions_v2/?quote-currency=USD&format=JSON&block-signed-at-asc=false&no-logs=false&page-number=&page-size=5&key={Config.COVALENT_API_KEY}"
        headers = {
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36',
            'Accept': 'application/json',
            'Sec-GPC': '1',
            'Content-Type': 'application/json'
        }
        try:
            response = requests.request("GET", url, headers=headers)
        except Exception as e:
            raise 'Oups! An error has been occured: {0}'.format(e)
        
        if response.status_code != 200:
            raise f'Response status code != 200: {response.error_message}'
        
        jdata = response.json()
        data = jdata.get('data', {})
        items = data.get('items', [])

        new_last_block = last_block
        
        for item in items:
            block_signed_at = item.get('block_signed_at')
            block_height = item.get('block_height')
            tx_hash = item.get('tx_hash')
            to_address = item.get('to_address')
            events = item.get('log_events')
            
            #block limit to break loop
            if last_block >= block_height:
                break

            new_last_block = max(block_height, new_last_block)
            
            message = Message()
            obj = {
                'username': username,
                'block_height': block_height,
                'block_signed_at': block_signed_at,
                'chain_id': chain_id,
                'tx_hash': tx_hash,
                'events': []
            }

            for event in events:
                #check only decoded events
                if event.get('decoded'):
                    event_decoded = event.get('decoded')
                    name = event_decoded.get('name')
                    sender_name = event.get('sender_name')
                    sender_contract_ticker_symbol = event.get('sender_contract_ticker_symbol')
                    params = event_decoded.get('params', [])
                    
                    event_obj = {
                        'name': name,
                        'sender_name': sender_name,
                        'sender_contract_ticker_symbol': sender_contract_ticker_symbol,
                    }

                    if params and len(params) >= 3:
                        from_address = params[0].get('value')
                        to_address = params[1].get('value')
                        value = params[2].get('value')
                        
                        event_obj['from_address'] = from_address
                        event_obj['to_address'] = to_address
                        event_obj['value'] = value

                    obj['events'].append(event_obj)

            message.send(obj, Config.MESSAGE_T.TX)

        address_queue[address][str(chain_id)] = {
            'last_block': new_last_block
        }

        with open(Config.FILE_WALLET_QUEUE, 'w') as json_file:
            json.dump(address_queue, json_file)

    