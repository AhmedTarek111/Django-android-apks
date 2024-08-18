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
    # Fetch the app from the database
    app = get_object_or_404(App, id=app_id, uploaded_by=request.user)

    # Set up Appium options
    options = UiAutomator2Options()
    options.platform_name = "Android"
    options.platform_version = "15.0"  # Ensure this matches your emulator version
    options.device_name = "emulator-5554"  # Ensure this matches your emulator device name
    options.app = app.apk_file.path  # Ensure this path is correct
    options.no_reset = True
    options.auto_grant_permissions = True

    driver = None
    video_filename = f'recording_{app_id}.mp4'
    f_screenshot_name = f"f_{app.name}_screenshot_{app.id}.png"
    s_screenshot_name = f"s_{app.name}_screenshot_{app.id}.png"
    try:
        # connect to driver 
        driver = webdriver.Remote(command_executor='http://localhost:4723', options=options)
        print("Driver connected successfully")
        # Start recording video
        driver.start_recording_screen()
        print("Started recording")
        time.sleep(5)
        app.ui_hierarchy = driver.page_source
        app.save()
        # taking first screenshot
        f_screenshot = driver.get_screenshot_as_png()
        print('Screen shot 1 Done')
         # get the first button 
        first_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@clickable="true"]'))
        )
        first_button.click()
        print("first button clicked")
        time.sleep(7)
        if first_button :
                app.screen_changed = True
                app.save()
                print('screen changed')
            # taking second screenshot

                s_screenshot = driver.get_screenshot_as_png()
                print('Screen shot 2 Done')
            
            
        # Stop recording video
        time.sleep(4)
        video_base64 = driver.stop_recording_screen()
        print("Stopped recording")

        # save the video in db 
        video_file = ContentFile(base64.b64decode(video_base64), video_filename)
        app.video_recording.save(video_filename, video_file, save=True)        
        # save f screenshot in db
        f_screenshot_file = ContentFile(f_screenshot , f_screenshot_name)
        app.first_screen_shot.save(f_screenshot_name,f_screenshot_file ,save=True)
        
        # save s screenshot in db
        s_screenshot_file = ContentFile(s_screenshot , s_screenshot_name)
        app.second_screen_shot.save(s_screenshot_name,s_screenshot_file ,save=True)
        
    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        if driver:
            driver.quit()
        print("Driver disconnected")

    return HttpResponse("Appium test completed successfully!")