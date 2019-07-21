from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# create instance of Flask app
app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

@app.route("/scrape")
def scraped():
    print("Running... ")
    scrapedata = scrape_mars.scrape()
    print(scrapedata)
    mongo.db.collection.update({}, scrapedata, upsert = True)

    return redirect("/", code=302)

@app.route("/")
def home():
    mars_data = mongo.db.collection.find_one()
    return render_template("index.html", mars_data=mars_data)

if __name__ == "__main__":
    app.run(debug=True)
