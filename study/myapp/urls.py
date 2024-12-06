from django.urls import path
from . import views

version = "v1"

urlpatterns = [
    path(version + '/' + 'data/', views.get_data, name='get_data'),  # 데이터 가져오는 API
    path(version + '/' + 'stocks/', views.get_stock_data, name='get_stock_data'),
    path(version + '/' + 'stocks/add/', views.add_stock, name='add_stock'),
]