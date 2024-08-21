Here’s the updated README template with the additional installation instructions:

---

# Django Project with Appium Integration

## Overview

This project is a Django web application with integrated Appium automated testing for Android APKs. It includes user authentication, management features, and a custom setup for automated testing using Appium and Celery. The project is Dockerized for both local development and production.

## Features

- **User Authentication:**
  - Custom authentication backend supporting both email and username.
  - User registration and logout functionality.
  
- **Management App:**
  - Django app for handling management-related features.

- **Automated Testing:**
  - Integration with Appium for automated APK testing.
  - Screenshots and video recordings of tests are captured and stored.

- **Celery Integration:**
  - Background task processing using Celery and Redis.
  
- **Internationalization:**
  - Support for multiple languages (English and French).

- **Dockerized Environment:**
  - Docker Compose configuration for development and production.

## Installation

### Prerequisites
- **run this project in Windows10 or 11 and have space in the particaion C**
- **Python 3.8+**
- **Docker & Docker Compose**
- **MySQL Server** (for local development or Docker container)
- **Appium** 
  - Install Appium by running: `npm install -g appium`
  - Start Appium server using: `appium`
- **Android Studio**
  - Download and install Android Studio from [here](https://developer.android.com/studio).
  - Run a virtual Android device using Android Studio.
  - Verify device connection with: `adb devices`



### Create a Virtual Environment 

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```
### path to clone the repository

```bash
cd ..
 ```

### Clone the Repository

```bash
git clone https://github.com/AhmedTarek111/Django-android-apks.git
cd Django-android-apks
```
### Enter project Folder

```bash
cd  Django-android-apks/project
 ```
### Install Dependencies

```bash
pip install -r requirements.txt
```


### Run Migrations

```bash
python manage.py migrate
```

### Running the Project Locally

```bash
python manage.py runserver
```

### Running with Docker
### Ensure the appium and the android device is running 
#### Build and Start Containers

```bash
docker-compose up --build
```

#### Access the Application

- **Web App:** http://localhost:8000
- **Admin Panel:** http://localhost:8000/admin

### Running Tests

Ensure the Appium server is running and configured. Then, run:

```bash
python manage.py test
```



## Project Structure

- **`accounts/`** - User authentication and management.
- **`management/`** - Custom management features.
- **`project/`** - Main Django project directory.
- **`docker-compose.yml`** - Docker Compose configuration.
- **`Dockerfile`** - Dockerfile for building the project image.

