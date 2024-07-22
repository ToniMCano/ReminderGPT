from django.urls import path , include
from .views import PagesListView , PagesDetailView

page_patterns = ([
    path("" , PagesListView.as_view() , name = "pages_home"),
    path("<int:pk>/<slug:page_slug>/" , PagesDetailView.as_view() , name = 'page'),
] , 'pages')
