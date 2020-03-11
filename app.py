from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

@app.route("/")
def index():
    mars = mongo.db.mars.find_one()
    image =   ["https://www.jpl.nasa.gov/spaceimages/images/largesize/PIA23741_hires.jpg","https://www.jpl.nasa.gov/spaceimages/images/largesize/PIA23515_hires.jpg","https://www.jpl.nasa.gov/spaceimages/images/largesize/PIA23514_hires.jpg", "https://www.jpl.nasa.gov/spaceimages/images/largesize/PIA23513_hires.jpg"]
    return render_template("index.html", mars_scraped_data = mars, image = image)

@app.route("/scrape")
def scrape():
    mars = mongo.db.mars 
    mars_data = scrape_mars.scrape()
    mars.update({}, mars_data, upsert=True)
    return redirect("http://localhost:5000/", code=302)

if __name__ == "__main__":
    app.run(debug=True)