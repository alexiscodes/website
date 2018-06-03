import feedparser
from flask import Flask
from flask import request
#Import to render html templates
from flask import render_template
#GET requests
from flask import request
#Use CCY data
import json
import urllib



app = Flask(__name__)

RSS_FEEDS =  {'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
             'cnn': 'http://rss.cnn.com/rss/edition.rss',
             'fox': 'http://feeds.foxnews.com/foxnews/latest',
             'iol': 'http://www.iol.co.za/cmlink/1.640'}

DEFAULTS = {'publication': 'bbc', 'currency_from': 'GBP', 'currency_to': 'EUR'}

CURRENCY_URL = 'https://openexchangerates.org//api/latest.json?app_id=a08dd44731fe409f9c7f7539b3874ab8'

@app.route("/")
def home():
    publication = request.args.get('publication')
    if not publication:
        publication = DEFAULTS['publication']
    articles = get_news(publication)

    currency_from = request.args.get("currency_from")
    if not currency_from:
        currency_from = DEFAULTS['currency_from']
    currency_to = request.args.get("currency_to")
    if not currency_to:
        currency_to = DEFAULTS['currency_to']
    
    #Get all available rates
    rate, currencies = get_rate(currency_from, currency_to)
    
    return render_template("home.html", articles=articles, currency_from=currency_from, currency_to=currency_to, rate=rate, currencies=sorted(currencies))

#@app.route("/<publication>")
#Use <> for URL to refer to variables
#def get_news(publication="bbc"):
#  feed = feedparser.parse(RSS_FEEDS[publication])
#  return render_template("home.html", articles=feed['entries'])
def get_news(query):
    if not query or query.lower() not in RSS_FEEDS:
        publication = DEFAULTS["publication"]
    else:
        publication = query.lower()
    feed = feedparser.parse(RSS_FEEDS[publication])
    return feed['entries']


def get_rate(frm, to):
    all_currency = urllib.request.urlopen(CURRENCY_URL).read()

    parsed=json.loads(all_currency).get('rates')
    frm_rate=parsed.get(frm.upper())
    to_rate=parsed.get(to.upper())
    return (to_rate / frm_rate, parsed.keys())  

if __name__ == '__main__':
    app.run(port=5000, debug= True)

