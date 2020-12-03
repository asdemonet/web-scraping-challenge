from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import pymongo
from pymongo import MongoClient
import mars_scrape



# client = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
# db = client.mars_db
# collection = db.mars_info

# Create an instance of Flask
app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://127.0.0.1:27017/mars_db"
mongo = PyMongo(app)

# conn = "mongodb://localhost:27017/"
# client = pymongo.MongoClient(conn)

# Use PyMongo to establish Mongo connection
# mongo = PyMongo(app, uri="mongodb://localhost:27017/")




# Route to render index.html template using data from Mongo
@app.route("/")
def index():

    # Find one record of data from the mongo database
    mars_data = mongo.db.mars_info.find()

    # Return template and data
    return render_template("index.html", mars=mars_data)


# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():

    # Run the scrape function
    mars_scrape.scrape()

    # Update the Mongo database using update and upsert=True
    # collection.drop()
    mongo.db.mars_info.update({}, scrape, upsert=True)

    # Redirect back to home page
    return redirect("/", code = 302)

# collection.drop()

if __name__ == "__main__":
    app.run(debug=True)
