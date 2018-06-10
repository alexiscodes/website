import feedparser

feed = feedparser.parse('http://feeds.bbci.co.uk/news/rss.xml')

feed['feed']['title']