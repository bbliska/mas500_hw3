from flask import Flask, render_template
import json
import feedparser
import globalvoices
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient()
db_stories=client.gv.stories

@app.route("/")
def index():
    return render_template("stories.html",
        country_list_json_text=json.dumps(globalvoices.country_list())
    )

@app.route("/country/<country>")
def country(country):
    # check db for stories
    if db_stories.find({'country':country}).count() > 0:
        # load and return db stories
        stories = db_stories.find({'country':country})
    else:
        #else if no stories in db, grab them from the server and add to db
        stories = globalvoices.recent_stories_from( country )
        for story in stories:
            db_stories.insert(story)

    return render_template("stories.html",
        country_list_json_text=json.dumps(globalvoices.country_list()),
        country_name=country,
        stories=stories
    )

if __name__ == "__main__":
    app.debug = True
    app.run()
