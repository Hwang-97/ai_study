from django.urls import path
from . import views

urlpatterns = [
    path('data/', views.get_data, name='get_data'),  # 데이터 가져오는 API
]