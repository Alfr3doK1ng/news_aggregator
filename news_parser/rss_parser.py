import feedparser

def parse_rss_feed(url):
    return feedparser.parse(url)