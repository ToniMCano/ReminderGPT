from django.urls import path , include
from . import views
from .chat_views import send_message , chat

handler403 = views.custom_permission_denied_view

urlpatterns = [
    path("" , views.home, name = "home"),
    path("create_user/" , views.create_user , name = "create_user"),
    path("chat/" , chat , name = 'chat'),
    path("send_message/" , send_message , name = 'send_message'),
    path("sign_up/" , views.sign_up , name = "sign_up"),
]

