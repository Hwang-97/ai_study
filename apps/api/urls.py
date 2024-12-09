from django.urls import path
from . import views

version = "v1"

urlpatterns = [
    path(version + "/" + "test/", views.get_test, name="get_test"),
    path(version + "/" + "stocks/", views.get_stock_data, name="get_stock_data"),
    path(version + "/" + "stocks/add/", views.add_stock, name="add_stock"),
    path(version + "/" + "chat/", views.chat_page, name='chat_page'),    # 새로 추가한 화면
    path(version + "/" + "news/", views.get_news, name='get_news'),    # 새로 추가한 화면
]
