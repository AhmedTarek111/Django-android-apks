from celery import shared_task
from appium import webdriver
from appium.options.android import UiAutomator2Options
from .models import App
from django.core.files.base import ContentFile
import base64
import time
import subprocess
import tempfile
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from django.shortcuts import get_object_or_404
import docker

def get_container_id(container_name):
    client = docker.DockerClient(base_url='unix://var/run/docker.sock')
    containers = client.containers.list(all=True)

    for container in containers:
        if container.name == container_name:
            return container.id
    return None

@shared_task
def appium_script(app_id):
    app = get_object_or_404(App, id=app_id)
    apk_file_name = str(app.apk_file.path).split('/')[-1]
    print(f"{30*'#'}{apk_file_name}")
    apk_container_path = f'/app/media/apks/{apk_file_name}'  # Define the container path
    container_name = 'project-backend'
    container_id = get_container_id(container_name)
    
    # Use a temporary file to store the extracted archive
    with tempfile.NamedTemporaryFile(delete=False, suffix='.tar') as temp_tar:
        tar_path = temp_tar.name

    try:
        client = docker.from_env()
        container = client.containers.get(container_name)
        bits, stat = container.get_archive(apk_container_path)
        
        # Write the archive to the temporary file
        with open(tar_path, 'wb') as tar_file:
            for chunk in bits:
                tar_file.write(chunk)
        print(f"APK file extracted to {tar_path}")

        # Unpack the tar file to get the APK
        # Assuming the APK file is directly inside the tar file
        apk_name_local_machine = os.path.join(tempfile.gettempdir(), apk_file_name)
        subprocess.run(['tar', '-xf', tar_path, '-C', tempfile.gettempdir()])
        print(f"APK file extracted to {apk_name_local_machine}")

        # Appium configuration
        options = UiAutomator2Options()
        options.platform_name = "Android"
        options.platform_version = "15.0"
        options.device_name = "emulator-5554"
        options.app = apk_name_local_machine
        options.no_reset = True
        options.auto_grant_permissions = True

        driver = None
        video_filename = f'recording_{app_id}.mp4'
        f_screenshot_name = f"f_{app.name}_screenshot_{app.id}.png"
        s_screenshot_name = f"s_{app.name}_screenshot_{app.id}.png"

        try:
            driver = webdriver.Remote(
                command_executor='http://host.docker.internal:4723',  # Adjust if needed
                options=options
            )
            print("Driver connected successfully")

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

    except Exception as e:
        print(f"An error occurred during APK file extraction: {e}")
    finally:
        # Cleanup the temporary tar and APK files
        if os.path.exists(tar_path):
            os.remove(tar_path)
        if os.path.exists(apk_name_local_machine):
            os.remove(apk_name_local_machine)

    return "Appium test completed successfully!"
