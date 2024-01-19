from django.shortcuts import render

# Create your views here.
from .rss_parser import parse_rss_feed
from datetime import datetime
from django.core.cache import cache


from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OpenAIEmbeddings
import pinecone
from langchain_community.vectorstores import Pinecone
import os

pinecone.init(api_key = "7a27aee2-c409-4a5c-9fa5-4870382fbf7f", environment = "gcp-starter")
from dotenv import load_dotenv, find_dotenv

from django.http import JsonResponse
from .models import NewsItem

from newspaper import Article

load_dotenv(find_dotenv(), override=True)

embeddings = OpenAIEmbeddings()

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=20,
    length_function=len
)

def show_news(request):
    # rss_feed_url = 'https://moxie.foxbusiness.com/google-publisher/latest.xml'
    # rss_feed_url = 'https://moxie.foxbusiness.com/google-publisher/economy.xml'
    # rss_feed_url = 'https://moxie.foxbusiness.com/google-publisher/markets.xml'
    # rss_feed_url = 'https://moxie.foxbusiness.com/google-publisher/technology.xml'
    # rss_feed_url = 'https://moxie.foxbusiness.com/google-publisher/college.xml'
    rss_feed_url = 'https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=100003114'
    news_items = parse_rss_feed(rss_feed_url).entries
    latest_news = []
    for entry in news_items:
        publish_time = datetime(*entry.published_parsed[:6]).isoformat()
        print(publish_time)
        print(entry.link)
        link = entry.link
        article = Article(link)
        article.download()
        article.parse()
        print(article.top_image)
        # print(article.text)
        article.nlp()
        print(article.summary)
        key = f"news:{publish_time}"

        if not cache.get(key):
            # Store the news item in Redis. You might want to store more details.
            cache.set(key, entry.title, timeout=None)  # 'timeout=None' for indefinite storage
            latest_news.append(entry)
    
    if latest_news:

        for entry in latest_news:
            print(entry.title)
            # print(str(entry.content))
            # print(entry.content[0]['value'])
            # chunks = text_splitter.create_documents([entry.content[0]['value']])
             # Extract content from 'content' or 'description' attribute
            news_content = entry.get('content', [{}])[0].get('value') or entry.get('description', '')
            chunks = text_splitter.create_documents([news_content])
            # print(chunks)
            Pinecone.from_documents(chunks, embeddings, index_name = "news")
        
    return render(request, 'news_parser/news.html', {'news_items': latest_news})

def latest_news(request):
    news_items = NewsItem.objects.all().order_by('-published_date')[:10]  # Get the latest 10 news items
    data = list(news_items.values('title', 'content', 'published_date', 'image_url', 'news_url'))
    return JsonResponse(data, safe=False)
