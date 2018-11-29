from typing import Dict
from pymongo import MongoClient
import datetime
from pymongo.errors import ConnectionFailure

class Category:
    '''
    parse edilmiş satırlar ile initilize edilir...
    '''

    def __init__(self,categoryList):
        pass

    @classmethod
    def _insert_data(cls,db ,category):
        try:
            db.categories.insert_one(category)
        except ConnectionFailure:
            print("Server is not available")

