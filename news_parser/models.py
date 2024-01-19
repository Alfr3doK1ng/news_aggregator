from django.db import models

# Create your models here.

class NewsItem(models.Model):
    title = models.CharField(max_length=200)
    image_url = models.CharField(max_length=200, null=True)
    news_url = models.CharField(max_length=200, null=True)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title