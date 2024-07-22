from typing import Any
from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import Registry



# Create your views here.


class PagesListView(ListView):
    
    model = Registry
    
    def get_context_data(self, **kwargs):
        
        context = super().get_context_data(**kwargs)
        
        context['title'] = "Hola Mundo"
        
        return context
    
class PagesDetailView(DetailView):
    
    model = Registry