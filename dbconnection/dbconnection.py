"""
Context manager for mongodb connectionpo
"""

from pymongo import MongoClient

class MongoDbConnection():

    def __init__(self,host,port):
        self.connection = None
        self.host = host
        self.port = port

    def __enter__(self):
        self.connection = MongoClient(self.host, self.port)
        return self.connection

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()