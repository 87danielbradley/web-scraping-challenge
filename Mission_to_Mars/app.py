#import necessary libraries
from flask import Flask, render_template, redirect
from flask_pymongo import pymongo
# import pymongo
import scrape_mars

#create instance of Flask app
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
#mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")


# Initialize PyMongo to work with MongoDBs
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)

mars_db = client.mars


#create route that renders index.html template
@app.route("/")
def home():
    # Find one record of data from the mongo database
    mars_data = mars_db.output.find()
    return render_template("index.html", mars_data=mars_data)

@app.route("/scrape")
def scrape():
    mars_db.output.drop()
    mars_data = scrape_mars.scrape()
    mars_db.output.insert_one(mars_data)
    return redirect('/')

if __name__  == "__main__":
    app.run(debug=True)