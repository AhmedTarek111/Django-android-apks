from django.urls import path
from .views import signup,logout

urlpatterns = [
    path('sign-up/',signup,name='sign-up'),
    path('login-again/',logout,name='login-again')
]
