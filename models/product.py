from dbconnection.dbconnection import MongoDbConnection
import json
"""

"""
class Product:
    @classmethod
    def get(self,name):
        productlist = self.find_by_category(name)
        if productlist:
            return productlist
        return {'message':'product not found'},404

    @classmethod
    def find_by_category(cls,categoryname):
        productlist = {}
        with MongoDbConnection('localhost',27017) as connection:
            db = connection.sanalmarket
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
             #   print(product)


        return json.dumps({'products':productlist})

