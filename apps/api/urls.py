from django.urls import path
from . import views

version = "v1"

urlpatterns = [
    path(version + "/" + "test/", views.get_test, name="get_test"),
    path(version + "/" + "stocks/", views.get_stock_data, name="get_stock_data"),
    path(version + "/" + "stocks/add/", views.add_stock, name="add_stock"),
]
