from django.shortcuts import render

# Create your views here.
from .rss_parser import parse_rss_feed

def show_news(request):
    rss_feed_url = 'https://moxie.foxbusiness.com/google-publisher/latest.xml'
    news_items = parse_rss_feed(rss_feed_url).entries
    print(news_items)
    return render(request, 'news_parser/news.html', {'news_items': news_items})
