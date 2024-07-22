from django.urls import path , include
from . import views
from pages.urls import page_patterns

urlpatterns = [
    path("" , views.home, name = "home"),
    path("sign_in/" , views.sing_in, name = "sign_in"),
    path("sign_up/" , views.sign_up , name = "sign_up"),
    path("test/" , views.test , name ="test") , 
    path("pages/" , include(page_patterns)),
]
