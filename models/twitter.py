from lightdb import LightDB
from datetime import datetime as dt

class Queue:
    
    def __init__(self, path):
        self.db = LightDB(path)
    
    def update(self, name, twitter_id):
        self.db.set(name, twitter_id)
    
    def get(self, name):
        return self.db.get(name)
    
    def is_exist(self, name):
        return not self.get(name) is None
    
    def get_all(self):
        return dict(self.db)
    
    def delete(self, name):
        self.db.pop(name)

class Account:
    
    def __init__(self, path):
        self.db = LightDB(path)
    
    def update(self, name):
        self.db.set(name, str(dt.now()))
    
    def get(self, name):
        return self.db.get(name)
    
    def is_exist(self, name):
        return not self.get(name) is None
    
    def get_all(self):
        return dict(self.db)
    
    def delete(self, name):
        self.db.pop(name)