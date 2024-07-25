from django.urls import path , include
from . import views
from chatgpt import views_copy

urlpatterns = [
  path("" , views.chat , name = 'chat'),
  path("sended/" , views.send_message , name = 'send_message'),
  path("test2/" , views_copy.test_openai , name = 'test'),
]
