from dbconnection.dbconnection import MongoDbConnection
import json

from datetime import datetime
"""

"""
class Product:
    @classmethod
    def get(self,name,startDate,finishDate):
        productlist = self.find_by_category(name,startDate,finishDate)
        if productlist:
            return productlist
        return {'message':'product not found'},404

    @classmethod
    def find_by_category(cls,categoryname,startDate,endDate):
        productlist = {}
        with MongoDbConnection('localhost',27017) as connection:
            db = connection.sanalmarket
            if startDate:
                date1 =  datetime.strptime(startDate, '%Y-%m-%d')
                date2 = datetime.strptime(endDate, '%Y-%m-%d')
                productlist = db.productlist.find(
                    {"categories":{"$elemMatch":{"$eq":categoryname}},
                     "prices.insertDatetime":{
                         "$gte": date1,
                         "$lt": date2}})
            else:
                productlist = db.productlist.find({"categories":{"$elemMatch":{"$eq":categoryname}}})

            productlist = [{
                "barcode":product["barcode"],
                "name":product["name"],
                "lastPrice":product["lastPrice"],
                "PromoPrice":product["PromoPrice"],
                "lastModifiedTime":product["lastModifiedTime"].strftime("%d %m %Y %H:%M"),
                "categoryName": product["categoryName"]
            } for product in productlist]

            #for product in productlist:
                #print(product)


        return productlist

