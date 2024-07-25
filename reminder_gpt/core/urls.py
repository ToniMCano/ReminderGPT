from django.urls import path , include
from . import views
from pages.urls import page_patterns

urlpatterns = [
    path("" , views.home, name = "home"),
    path("create_user/" , views.create_user , name = "create_user"),
    path("sign_up/" , views.sign_up , name = "sign_up"),
    path("test/" , views.test , name ="test"), # TODO este se eliminará
    path("pages/" , include(page_patterns)),
]
