from django.urls import path
from . import views

version = "v1"

urlpatterns = [
    path(version + "/" + "ask/", views.get_answer, name="ask_question"),
]
