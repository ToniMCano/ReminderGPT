from django.urls import path , include
from . import views

urlpatterns = [
    path("" , views.home, name = "home"),
    path("sign_in/" , views.sing_in, name = "sign_in"),
    path("sign_up/" , views.signup , name = "sign_up")
]
