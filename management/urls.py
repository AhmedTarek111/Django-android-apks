from django.urls import path
from .views import AppList , AppCreate , AppDelete ,AppDetail ,AppUpdate

urlpatterns = [
    path('create/',AppCreate.as_view(),name='app-create'),
    path('update/<int:pk>/',AppUpdate.as_view(),name='app-update'),
    path('delete/<int:pk>/',AppDelete.as_view(),name='app-delete'),
    path('detail/<int:pk>/',AppDetail.as_view(),name='app-detail'),
]

