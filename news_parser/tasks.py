from celery import shared_task

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
load_dotenv(find_dotenv(), override=True)

from .models import NewsItem

from newspaper import Article
import nltk


embeddings = OpenAIEmbeddings()

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=20,
    length_function=len
)

@shared_task
def my_scheduled_task():
    # Your task implementation
    print("Task executed")

    rss_feed_urls = ['https://moxie.foxbusiness.com/google-publisher/latest.xml',
                     'https://www.investmentnews.com/feed',
                     'https://www.vox.com/rss/index.xml',
                     'https://rsshub.app/cnbc/rss',
                     'https://rsshub.app/caixinglobal/latest',
                     'https://rsshub.app/rfi',
                     'https://rsshub.app/rthk-news/en/international',
                     'https://rsshub.app/scmp/3',
                     'https://rsshub.app/economist/espresso',
                     'https://rsshub.app/guardian/editorial',
                     'https://rsshub.app/ainvest/article',
                     'https://rsshub.app/fx-markets/trading',
                     'https://rsshub.app/apnews/topics/apf-topnews',
                     'https://rsshub.app/sputniknews',
                     'https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=10001147',
                     'https://www.cbsnews.com/latest/rss/moneywatch',
                     'https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=10000664',
                     'https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=19854910',
                     'http://rss.cnn.com/rss/money_news_international.rss',
                     ]
    
    for rss_feed_url in rss_feed_urls:
        print(rss_feed_url)
        news_items = parse_rss_feed(rss_feed_url).entries
        latest_news = []
        for entry in news_items:
            publish_time = datetime(*entry.published_parsed[:6]).isoformat()
            key = f"news:{publish_time}"

            if not cache.get(key):
                # Store the news item in Redis. You might want to store more details.
                cache.set(key, entry.title, timeout=None)  # 'timeout=None' for indefinite storage
                latest_news.append(entry)
        
        if latest_news:
            print(rss_feed_url)
            for entry in latest_news:
                print(entry.title)       

                article = Article(entry.link)
                article.download()
                article.parse()
                article.nlp()
                image_url = article.top_image
                news_content = article.text
                summary = article.summary

                NewsItem.objects.create(title=entry.title, content=summary, image_url=image_url, news_url=entry.link)

                chunks = text_splitter.create_documents([news_content])
                Pinecone.from_documents(chunks, embeddings, index_name = "news")
