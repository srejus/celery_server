from django.urls import path
from .views import *

urlpatterns = [
    path('schedule/',schedule_task_view,name='schedule_task_view'),
]