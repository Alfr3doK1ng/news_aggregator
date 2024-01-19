# news_aggregator
News aggregator for latest financial news using Django, Redis, Celery, feedparser and newspaper3k.
# Run
```
python3 manage.py runserver # Starting the server
celery -A news_aggregator worker --loglevel=info # Starting a worker to pull the news
celery -A news_aggregator beat --loglevel=info # Starting a Celery scheduler to send tasks to worker periodically
```
Navigate to localhost:8000/latest_news to see what are some latest news that has been stored into vector store.
# How it works
It first subscribes to some major news provider RSS feeds. Then for each worker it has a Redis setup with it. Then it uses feedparser to parse out the url, title, content etc. Then the url will be fed into a open-source library newspaper3k which will take a step further to parse the full content of the news, in case some RSS feed only provides a abstract of the news and this is not really what we want. Then it calls the api of a locally deployed nlp library called NLTK and generates a short summary of the full news.

After gathering all the data, it then provides an API to call so the main app can make a GET request and get the latest news. The API is exposed at localhost:8000/latest_news
