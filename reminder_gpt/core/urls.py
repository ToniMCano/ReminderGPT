from django.urls import path , include
from . import views

urlpatterns = [
    path("" , views.home, name = "home"),
    path("sign_in/" , views.sing_in, name = "sign_in"),
    path("sign_up/" , views.sign_up , name = "sign_up"),
    path("validate/" , views.validate , name ="validate") , 
]
