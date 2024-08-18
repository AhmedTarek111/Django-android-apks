from django.urls import path
from .views import AppList , AppCreate , AppDelete ,AppDetail ,AppUpdate,run_test

urlpatterns = [
    path('create/',AppCreate.as_view(),name='app-create'),
    path('update/<int:pk>/',AppUpdate.as_view(),name='app-update'),
    path('delete/<int:pk>/',AppDelete.as_view(),name='app-delete'),
    path('detail/<int:pk>/',AppDetail.as_view(),name='app-detail'),
    path('test/<int:app_id>',run_test,name='app-test')
]

