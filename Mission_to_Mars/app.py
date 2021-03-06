from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import pymongo
from pymongo import MongoClient
import mars_scrape

# Create an instance of Flask
app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://127.0.0.1:27017/mars_db"
mongo = PyMongo(app)

# Route to render index.html template using data from Mongo
@app.route("/")
def index():

    # Find one record of data from the mongo database
    mars_update = mongo.db.mars_info.find_one()

    # Return template and data
    return render_template("index.html", mars_update=mars_update)

# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():

    # Run the scrape function
    mars_update = mars_scrape.scrape()

    # Update the Mongo database using update and upsert=True
    mongo.db.mars_info.update({}, mars_update, upsert=True)

    # Redirect back to home page
    return redirect("/", code = 302)

if __name__ == "__main__":
    app.run(debug=True)
