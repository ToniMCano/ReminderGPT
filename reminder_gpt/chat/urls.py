from django.urls import path , include
from . import views

urlpatterns = [
  path("" , views.chat , name = 'chat'),
  path("sended/" , views.send_message , name = 'send_message')
]
