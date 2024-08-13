from django.shortcuts import render,redirect
from django.views.generic import ListView , CreateView , UpdateView , DeleteView , DetailView
from django.contrib.auth.models import User
from .models import App
from .forms import AppForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import translation
from django.conf import settings


class AppList(LoginRequiredMixin,ListView):
    model = App
    fields = '__all__'
    template_name = 'app/home.html'
    context_object_name = 'myapp'
    login_url = 'accounts/login/'
    
    
    def get_queryset(self):
        return App.objects.filter(uploaded_by = self.request.user)
    
    
class AppCreate(LoginRequiredMixin,CreateView):
    model = App
    template_name = 'app/app_create.html'
    form_class = AppForm
    success_url = '/'
    def form_valid(self, form):
        form.instance.uploaded_by = self.request.user
        return super().form_valid(form)
    
class AppUpdate(LoginRequiredMixin,UpdateView):
    model = App
    template_name = 'app/app_update.html'
    form_class = AppForm
    success_url = '/'

    
class AppDelete(LoginRequiredMixin,DeleteView):
    model = App
    template_name = 'app/app_delete.html'
    success_url  = '/'
    

class AppDetail(LoginRequiredMixin,DetailView):
    model = App
    template_name = 'app/app_Detail.html'
    context_object_name = 'apk'
    fields = '__all__'

def changeLanguage(request):
    language = request.POST['language']
    translation.activate(language)
    response = redirect('/')  
    return response