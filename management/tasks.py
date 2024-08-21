from celery import shared_task
from appium import webdriver
from appium.options.android import UiAutomator2Options
from .models import App
from django.core.files.base import ContentFile
import base64
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from django.shortcuts import get_object_or_404

@shared_task
def appium_script(app_id):
    app = get_object_or_404(App, id=app_id)
    apkname = app.apk_file.path.split('/')[-1]
    options = UiAutomator2Options()
    options.platform_name = "Android"
    options.platform_version = "15.0"
    options.device_name = "emulator-5554"
    options.app = fr'C:\docker_share\apks\{apkname}'
    options.no_reset = True
    options.auto_grant_permissions = True

    driver = None
    video_filename = f'recording_{app_id}.mp4'
    f_screenshot_name = f"f_{app.name}_screenshot_{app.id}.png"
    s_screenshot_name = f"s_{app.name}_screenshot_{app.id}.png"

    try:
        #  this for docker 
        driver = webdriver.Remote(
            command_executor='http://host.docker.internal:4723',  
            options=options
        )
        print("Driver connected successfully")
    except:
        # this for local host
        options.app = options.app = app.apk_file.path 
        driver = webdriver.Remote(
            command_executor='http://localhost:4723',  
            options=options
        )
    try:
        driver.start_recording_screen()
        print("Started recording")
        time.sleep(5)

        app.ui_hierarchy = driver.page_source
        app.save()

        f_screenshot = driver.get_screenshot_as_png()
        print('Screenshot 1 Done')

        first_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@clickable="true"]'))
        )
        first_button.click()
        print("First button clicked")
        time.sleep(7)

        if first_button:
            app.screen_changed = True
            app.save()
            print('Screen changed')

            s_screenshot = driver.get_screenshot_as_png()
            print('Screenshot 2 Done')

        time.sleep(4)
        video_base64 = driver.stop_recording_screen()
        print("Stopped recording")

        video_file = ContentFile(base64.b64decode(video_base64), video_filename)
        app.video_recording.save(video_filename, video_file, save=True)

        f_screenshot_file = ContentFile(f_screenshot, f_screenshot_name)
        app.first_screen_shot.save(f_screenshot_name, f_screenshot_file, save=True)

        s_screenshot_file = ContentFile(s_screenshot, s_screenshot_name)
        app.second_screen_shot.save(s_screenshot_name, s_screenshot_file, save=True)
       

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        if driver:
            driver.quit()
        print("Driver disconnected")

    return "Appium test completed successfully!"
