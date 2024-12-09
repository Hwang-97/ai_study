from django.urls import path
from . import views

version = "v1"

urlpatterns = [
    path(version + "/" + "chat/", views.chat_with_ai, name="chat_with_ai"),
    path(version + "/" + "news/", views.analyze_news, name="analyze_news"),
    path(version + "/" + "decision/", views.make_trading_decision, name="make_trading_decision"),
]
