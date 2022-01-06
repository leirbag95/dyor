from lightdb import LightDB
from datetime import datetime as dt

class Queue:
    
    def __init__(self, path):
        self.db = LightDB(path)
    
    def update(self, address, name):
        """add or update information related to the target, except network 
        information

        Args:
            address (str): target's address
            name (str): target's name
        """
        obj = {
            'name': name,
            'datetime': str(dt.now())
        }
        self.db.set(address, obj)
    
    def update_network(self, address, chain_id, block):
        """update or add a network and its tracking block

        Args:
            address (str): target's address
            chain_id (str): network's chain id
            block (str): tracking block to save last visited block
        """
        if self.is_exist(address):
            obj = self.get(address)
            obj[chain_id] = block
            self.db.set(address, obj)
    
    def get(self, address):
        return self.db.get(address)
    
    def is_exist(self, address):
        return not self.get(address) is None
    
    def get_all(self):
        return dict(self.db)
    
    def delete(self, address):
        self.db.pop(address)