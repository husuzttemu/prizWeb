
from flask import Flask,render_template,request,url_for,redirect,jsonify
from flask_pymongo import PyMongo
import datetime
import pygal

from search_engine.engine import Engine
from models.product import Product

import json
from urllib.request import urlopen
from pygal.style import DarkSolarizedStyle



app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'sanalmarket'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/sanalmarket'

mongo = PyMongo(app)


@app.route('/')
def home():
    categoryList = mongo.db.categories.find().limit(20000)

    return render_template("home.html")

#127.0.0.1:5000/post/create?title=...&content=...
@app.route('/categories', methods=['GET'])
def categories():
    categoryList = mongo.db.categories.find().limit(20000)
    return render_template("categories.html",
                           categoryList=categoryList)

#127.0.0.1:5000/post/create?title=...&content=...
@app.route('/products/<categoryName>', methods=['GET'])
def products(categoryName):
    print(categoryName)
    if categoryName:
        productlist = mongo.db.productlist.find({"categoryName": categoryName}).limit(20000)
    else:
        productlist = mongo.db.productlist.find().limit(20000)
    return render_template("products.html",
                           productlist=productlist)

@app.route('/allproducts/', methods=['GET'])
def allproducts():
    productlist = mongo.db.productlist.find().limit(20000)
    return render_template("products.html",
                           productlist=productlist)



#127.0.0.1:5000/post/create?title=...&content=...
@app.route('/create', methods=['GET','POST'])
def create():
    if request.method=='POST':
        productlist = mongo.db.productlist

        myEngine = Engine()
        myEngine.find_products_from_all_categories()

        return redirect(url_for('home'))
    return render_template('create.html')

@app.route('/chart/<barcodeParam>', methods=['GET'])
def chart(barcodeParam):
    productlist = mongo.db.productlist.find({"barcode":barcodeParam})


    for product in productlist:
        barcode = product["barcode"]
        name = product["name"]
        labels = [x["insertDatetime"].strftime("%d %m %Y %H:%M") for x in product["prices"]]
        values = [float(str.replace(x["price"], ",", ".")) for x in product["prices"]]
        #hus = [{"date":x["insertDatetime"],"price":float(str.replace(x["price"], ",", "."))} for x in product["prices"]]
        #print(hus)

    return render_template('graph.html', barcode=barcode,name=name,values=values, labels=labels)

@app.route('/productreport', methods=['GET'])
def productreport():
    categories = mongo.db.categories.find({})
    categoryList = set([x["categories"][0] for x in categories])
    if request.method == 'GET':
        return render_template('productreport.html', categories=categoryList)
    else:
        return render_template('productreport.html', categories=categoryList, productlist=productlist)



"""
    pipeline = [
        { "$match" : { "barcode":"20000027023000" } },
        {"$group" : {"_id":{"barcode":"$barcode","price":"$price",
                            "date": { "$dateToString": { "format": "%d-%m-%Y", "date": "$insertDatetime" } }
                            }}}
    ]
    cursor1 =  mongo.db.productlist.aggregate(pipeline)
    cursor2 = mongo.db.productlist.aggregate(pipeline)

    labels = [x["_id"]["date"]  for x in cursor1]
    values = [float(str.replace(x["_id"]["price"],",","."))  for x in cursor2]
"""


@app.route('/productlist/<categoryname>', methods=['GET'])
def productlist(categoryname):
    productlist = Product.get(categoryname)

    return productlist
    # categories = mongo.db.categories.find({})

@app.route('/linechart/<barcodeParam>', methods=['GET'])
def linechart(barcodeParam):
    productlist = mongo.db.productlist.find({"barcode": barcodeParam})

    for product in productlist:
        barcode = product["barcode"]
        name = product["name"]
        labels = [x["insertDatetime"].strftime("%d %m %Y %H:%M") for x in product["prices"]]
        values = [float(str.replace(x["price"], ",", ".")) for x in product["prices"]]

    return render_template('linechart.html', barcode=barcode, name=name, values=values, labels=labels)

if __name__ == '__main__':
    app.run(debug=True)

