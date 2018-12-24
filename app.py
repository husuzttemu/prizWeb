
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

#test
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
        labels = [x["insertDatetime"].strftime("%d %m %Y") for x in product["prices"]]
        values = [float(str.replace(x["price"], ",", ".")) for x in product["prices"]]
        #hus = [{"date":x["insertDatetime"],"price":float(str.replace(x["price"], ",", "."))} for x in product["prices"]]
        #print(hus)

    return render_template('graph.html', barcode=barcode,name=name,values=values, labels=labels)

@app.route('/productreport', methods=['GET',"POST"])
def productreport():
    if request.method == 'POST':
        # do stuff when the form is submitted

        # redirect to end the POST handling
        # the redirect can be to the same route or somewhere else

        category = request.form.get('category')

        startDate = request.form.get("startDatePicker")
        endDate = request.form.get("endDatePicker")

        #print(f" {startDatePicker}")

        productlist = Product.get(category,startDate,endDate)

        return render_template('queryproducts.html',productlist=productlist)
    categories = mongo.db.categories.find({})
    categoryList = set([x["categories"][0] for x in categories])

    return render_template('productreport.html', categories=categoryList)


@app.route('/queryproducts', methods=['GET'])
def queryproducts():

    #return render_template('productreport.html', productlist=productlist)
    return render_template('queryproducts.html')

@app.route('/productlist/<categoryname>', methods=['GET'])
def productlist(categoryname):
    productlist = Product.get(categoryname,None,None)

    return render_template("products.html",
                           productlist=productlist)
    #return productlist
    # categories = mongo.db.categories.find({})

@app.route('/linechart/<barcodeParam>', methods=['GET'])
def linechart(barcodeParam):
    productlist = mongo.db.productlist.find({"barcode": barcodeParam})
    maxprice = 10

    for product in productlist:
        barcode = product["barcode"]
        name = product["name"]
        labels = [x["insertDatetime"].strftime("%d %m %Y") for x in product["prices"]]
        values = [float(str.replace(x["price"], ",", ".")) for x in product["prices"]]
        if int(round(max(values),0)) > maxprice: maxprice = int(round(max(values),0)) + 1

    return render_template('linechart.html', barcode=barcode, name=name, values=values, labels=labels, maxprice=maxprice)

if __name__ == '__main__':
    app.run(debug=True)

