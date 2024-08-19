from django.shortcuts import render,redirect ,get_object_or_404,HttpResponse
from django.views.generic import ListView , CreateView , UpdateView , DeleteView , DetailView
from django.contrib.auth.models import User
from .models import App
from .forms import AppForm,AppCreateUpdateForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import translation
from django.conf import settings
from appium import webdriver
from appium.options.android import UiAutomator2Options
import os
import subprocess
import time
from django.core.files.base import ContentFile
import base64
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .tasks import appium_script
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
    form_class = AppCreateUpdateForm
    success_url = '/'
    def form_valid(self, form):
        form.instance.uploaded_by = self.request.user
        return super().form_valid(form)
    
class AppUpdate(LoginRequiredMixin,UpdateView):
    model = App
    template_name = 'app/app_update.html'
    form_class = AppCreateUpdateForm
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
    return redirect('/')  

# def run_test(request,app_id):
#     appium_test_app.delay(app_id)
#     return redirect('/')

def run_test(request, app_id):
    appium_script.delay(app_id)  # Call the Celery task
    return redirect('/')