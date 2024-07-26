from django.urls import path , include
from . import views
from .chat_views import test_openai , send_message , chat


urlpatterns = [
    path("" , views.home, name = "home"),
    path("create_user/" , views.create_user , name = "create_user"),
    path("chat/" , chat , name = 'chat'),
    path("sended/" , send_message , name = 'send_message'),
    path("sign_up/" , views.sign_up , name = "sign_up"),
]

