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
                     'https://rsshub.app/abc',
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
                     ]
    
    for rss_feed_url in rss_feed_urls:

        news_items = parse_rss_feed(rss_feed_url).entries
        latest_news = []
        for entry in news_items:
            # print(rss_feed_url)
            publish_time = datetime(*entry.published_parsed[:6]).isoformat()
            # print(publish_time)
            key = f"news:{publish_time}"

            if not cache.get(key):
                # Store the news item in Redis. You might want to store more details.
                cache.set(key, entry.title, timeout=None)  # 'timeout=None' for indefinite storage
                latest_news.append(entry)
        
        if latest_news:
            print(rss_feed_url)
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
