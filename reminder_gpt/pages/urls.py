from django.urls import path , include
from .views import PagesListView , PagesDetailView , PageCreate , PageUpdate , PageDelete

page_patterns = ([
    path("" , PagesListView.as_view() , name = "pages_home"),
    path("<int:pk>/<slug:page_slug>/" , PagesDetailView.as_view() , name = 'page'),
    path("create/" , PageCreate.as_view() , name = "create"),
    path("update/<int:pk>/" , PageUpdate.as_view() , name = "update"),
    path('delete/<int:pk>' , PageDelete.as_view() , name = "delete")
] , 'pages')
