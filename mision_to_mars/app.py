from flask import Flask, render_template,redirect
import scrape
from flask_pymongo import PyMongo


app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

@app.route("/")
def index():
    new = mongo.db.latestnew.find_one()
    return render_template("index.html",lastnew=new) 


@app.route("/scrape")
def scraper():
    
    lastnew = mongo.db.latestnew
    mars_news= scrape.scrape()
    lastnew.update({},mars_news,upsert=True)
    return redirect("/", code=302)

    
    


if __name__ == "__main__":
    app.run(debug=True)