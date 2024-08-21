from celery import shared_task
from appium import webdriver
from appium.options.android import UiAutomator2Options
from .models import App
from django.shortcuts import get_object_or_404, HttpResponse
import base64
import os
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@shared_task
def appium_script(app_id):
    app = get_object_or_404(App, id=app_id)
    apkname = app.apk_file.path.split('/')[-1]
    
    # Adjusted path within the Docker container
    apk_path_in_container = f'/root/shared/apks/{apkname}'

    options = UiAutomator2Options()
    options.platform_name = "Android"
    options.platform_version = "15.0"
    options.device_name = "emulator-5554"
    options.app = apk_path_in_container
    options.no_reset = True
    options.auto_grant_permissions = True

    # Paths for saving files
    media_root = '/app/media'  # Adjust this path if necessary
    f_screenshot_name = f"f_{app.name}_screenshot_{app.id}.png"
    s_screenshot_name = f"s_{app.name}_screenshot_{app.id}.png"
    video_filename = f'recording_{app_id}.mp4'

    driver = None

    try:
        driver = webdriver.Remote(
            command_executor='http://host.docker.internal:4723',  # Ensure this is correct
            options=options
        )
        print("Driver connected successfully")

        driver.start_recording_screen()
        print("Started recording")
        time.sleep(5)

        app.ui_hierarchy = driver.page_source
        app.save()

        # Capture first screenshot
        f_screenshot_path = os.path.join(media_root, 'f_screenshot', f_screenshot_name)
        with open(f_screenshot_path, 'wb') as f:
            f.write(driver.get_screenshot_as_png())
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

            # Capture second screenshot
            s_screenshot_path = os.path.join(media_root, 's_screenshot', s_screenshot_name)
            with open(s_screenshot_path, 'wb') as f:
                f.write(driver.get_screenshot_as_png())
            print('Screenshot 2 Done')

        time.sleep(4)

        # Save video recording
        video_base64 = driver.stop_recording_screen()
        video_path = os.path.join(media_root, 'video_recording', video_filename)
        with open(video_path, 'wb') as video_file:
            video_file.write(base64.b64decode(video_base64))
        print("Stopped recording")

        # Update Django model fields with file paths
        app.video_recording = f'video_recording/{video_filename}'
        app.first_screen_shot = f'f_screenshot/{f_screenshot_name}'
        app.second_screen_shot = f's_screenshot/{s_screenshot_name}'
        app.save()

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        if driver:
            driver.quit()
        print("Driver disconnected")

    return HttpResponse("done")
