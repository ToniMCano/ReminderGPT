from django.urls import path , include
from . import views
from chatgpt.views import test_openai

urlpatterns = [
  path("" , views.chat , name = 'chat'),
  path("sended/" , views.send_message , name = 'send_message'),
  path("test2/" , test_openai , name = 'test'),
]
