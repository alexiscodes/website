import feedparser
import datetime
from flask import Flask
from flask import request
#Import to render html templates
from flask import render_template
#GET requests
from flask import request
#Use CCY data
import json
import urllib

#Start using Cookies -> REMEMBER Fallback logic!
from flask import make_response



app = Flask(__name__)

RSS_FEEDS =  {'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
             'cnn': 'http://rss.cnn.com/rss/edition.rss',
             'fox': 'http://feeds.foxnews.com/foxnews/latest',
             'iol': 'http://www.iol.co.za/cmlink/1.640'}

DEFAULTS = {'publication': 'bbc', 'currency_from': 'GBP', 'currency_to': 'EUR'}

CURRENCY_URL = 'https://openexchangerates.org//api/latest.json?app_id=a08dd44731fe409f9c7f7539b3874ab8'

@app.route("/")
def home():
    #Use fallback logics for cookies
    publication = get_value_with_fallback('publication')
    articles = get_news(publication)

    currency_from = get_value_with_fallback("currency_from")
    currency_to = get_value_with_fallback("currency_to")
    
    #Get all available rates
    rate, currencies = get_rate(currency_from, currency_to)
    
    #Add Cookie response to this
    #return render_template("home.html", articles=articles, currency_from=currency_from, currency_to=currency_to, rate=rate, currencies=sorted(currencies))
    response = make_response(render_template("home.html", articles=articles, currency_from=currency_from, currency_to=currency_to, rate=rate, currencies=sorted(currencies)))
    expires = datetime.datetime.now() + datetime.timedelta(days=365)
    response.set_cookie("publication", publication, expires=expires)
    response.set_cookie("currency_from", currency_from, expires=expires)
    response.set_cookie("currency_to", currency_to, expires=expires)
    return response




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

#Fallback logic for cookies
def get_value_with_fallback(key):
    if request.args.get(key):
        return request.args.get(key)
    if request.cookies.get(key):
        return request.cookies.get(key)
    return DEFAULTS[key]

if __name__ == '__main__':
    app.run(port=5000, debug= True)

