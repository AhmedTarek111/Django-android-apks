from django.urls import path
from .views import signup

urlpatterns = [
    path('sign-up/',signup,name='sign-up'),
]
