from django.urls import path
from . import views

urlpatterns = [
    path('news/', views.show_news, name='show_news'),
]
