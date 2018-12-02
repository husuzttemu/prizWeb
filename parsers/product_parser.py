from locators.page_locators import PageLocators
import datetime
from parsers.category import Category
from dbconnection.dbconnection import MongoDbConnection
from pymongo.errors import ConnectionFailure,DuplicateKeyError

class ProductParser:
    '''
    parse edilmiş satırlar ile initilize edilir...
    '''

    def __init__(self,parent):
        self.product = {}
        self.parent = parent
        self.setProduct()
        self._insert_data()



    def __repr__(self):
        return f' repr id={self.productBarcode} name={self.productName} price={self.productPrice}'

    def __str__(self):
        return f' str id={self.productBarcode} name={self.productName} price={self.productPrice}'

    def setProduct(self):
        self.product['barcode']=self.productBarcode
        self.product['name']=self.productName
        self.product['categoryName'] = self.productCategoryName
        now = datetime.datetime.now()
        self.product['lastPrice'] = self.productPrice
        self.product['lastModifiedTime'] = now

        prices = []
        prices.append({"price":self.productPrice,
                  "promotionPrice":self.productPromotionPrice,
                  "productUnit" : self.productUnit,
                  "insertDatetime":now})

        self.product['prices']=prices


    @property
    def getProduct(self):
        return self.product

    @property
    def productBarcode(self):
        text = self.parent.select_one(PageLocators.BARCODE)
        barcode = text.attrs['value']
        return barcode

    @property
    def productName(self):
        text = self.parent.select_one(PageLocators.PRODUCTATTR)
        name = text.attrs['data-product-name']
        return name

    @property
    def productPrice(self):
        #text = self.parent.select_one(PageLocators.PRODUCTATTR)
        #price = text.attrs['data-price']
        text = self.parent.select_one(PageLocators.PRODUCTMONITOR)
        price = text.attrs['data-monitor-price']
        return price

    @property
    def productUnit(self):
        text = self.parent.select_one(PageLocators.PRODUCTATTR)
        unit = text.attrs['data-unit']
        return unit

    @property
    def productCode(self):
        text = self.parent.select_one(PageLocators.PRODUCTMONITOR)
        code = text.attrs['data-monitor-id']
        return code

    @property
    def productMonitorName(self):
        text = self.parent.select_one(PageLocators.PRODUCTMONITOR)
        name = text.attrs['data-monitor-name']
        return name

    @property
    def productCategoryName(self):
        text = self.parent.select_one(PageLocators.PRODUCTMONITOR)
        categoryName = text.attrs['data-monitor-category']
        return categoryName

    @property
    def productPromotionPrice(self):
        promotionPrice = '0'
        if self.parent.select_one(PageLocators.PROMOTIONPRICE) is None:
            promotionPrice = '0'
        else:
            text = self.parent.select_one(PageLocators.PROMOTIONPRICE)
            promotionPrice = text.string.strip()
        return promotionPrice

    def _insert_data(self):
        with MongoDbConnection('localhost',27017) as connection:
            db = connection.sanalmarket
            try:
                print(f"product : {self.product}")
                db.productlist.insert_one(self.product)
            except DuplicateKeyError:
                print(f"barkod : {self.product['barcode']}")
                print(f"prices : {self.product['prices']}")
                db.productlist.update_one(
                    {"barcode": self.product['barcode']},
                    {"$set": {
                        "lastrice":self.productPrice,
                        "lastModifiedTime": self.product['lastModifiedTime']
                    },
                        "$push":{
                            "prices": {
                                "price": self.productPrice,
                                "promotionPrice": self.productPromotionPrice,
                                "productUnit": self.productUnit,
                                "insertDatetime": self.product['lastModifiedTime']
                            }
                        }
                    }
                )



            category = {}
            category['categoryName'] = self.productCategoryName
            Category._insert_data(db, category)



"""
        try:
            category = {}
            category['categoryName'] = self.productCategoryName
            Category._insert_data(connection, category)
        except:
            pass

"""





