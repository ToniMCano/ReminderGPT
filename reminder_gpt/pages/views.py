from typing import Any
from django.shortcuts import render 
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView , UpdateView , DeleteView
from django.urls import reverse , reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .models import Registry



# Create your views here.

@method_decorator(login_required, name='dispatch')
class PagesListView(ListView):
    
    model = Registry
    
    def get_context_data(self, **kwargs):
        
        context = super().get_context_data(**kwargs)
        
        context['title'] = "Hola Mundo"
        
        return context
    
    
@method_decorator(login_required, name='dispatch')
class PagesDetailView(DetailView):
    
    model = Registry
    
    
@method_decorator(login_required, name='dispatch')
class PageCreate(CreateView):
    
    model = Registry
    
    fields = ["project_name" , "log"]
    
    def form_valid(self, form):
        form.instance.user = self.request.user  # Establece el usuario al usuario que ha iniciado sesión
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('pages:pages_home')


@method_decorator(login_required, name='dispatch')   
class PageUpdate(UpdateView):
    
    model = Registry
    
    fields = ["project_name" , "log"]
    
    template_name_suffix = "_update_form"
    
    def get_success_url(self):
        return reverse_lazy("pages:update" , args = [self.object.id]) + '?ok'
    

@method_decorator(login_required, name='dispatch')   
class PageDelete(DeleteView):
    
    model = Registry
    
    success_url =  reverse_lazy('pages:pages_home')