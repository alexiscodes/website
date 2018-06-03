import feedparser
from flask import Flask
from flask import request
#Import to render html templates
from flask import render_template


app = Flask(__name__)

RSS_FEEDS =  {'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
             'cnn': 'http://rss.cnn.com/rss/edition.rss',
             'fox': 'http://feeds.foxnews.com/foxnews/latest',
             'iol': 'http://www.iol.co.za/cmlink/1.640'}

@app.route("/")


@app.route("/<publication>")
#Use <> for URL to refer to variables
def get_news(publication="bbc"):
  feed = feedparser.parse(RSS_FEEDS[publication])
  return render_template("home.html", articles=feed['entries'])



if __name__ == '__main__':
    app.run(port=5000, debug= True)

feedparser.parse('http://feeds.bbci.co.uk/news/rss.xml')