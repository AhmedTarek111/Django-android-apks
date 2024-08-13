from django.shortcuts import render
from django.views.generic import ListView , CreateView , UpdateView , DeleteView , DetailView
from .models import App
from .forms import AppForm


class AppList(ListView):
    model = App
    fields = '__all__'
    template_name = 'app/app_list.html'
    
    
class AppCreate(CreateView):
    model = App
    template_name = 'app/app_create.html'
    form_class = AppForm
    success_url = '/'
    
    
class AppUpdate(UpdateView):
    model = App
    template_name = 'app/app_update.html'
    form_class = AppForm
    success_url = '/'

    
class AppDelete(DeleteView):
    model = App
    template_name = 'app/app_delete.html'
    success_url  = '/'
    

class AppDetail(DetailView):
    model = App
    template_name = 'app/app_Detail.html'
    context_object_name = 'apk'
    form_class = AppForm

    