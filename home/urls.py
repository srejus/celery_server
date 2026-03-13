from django.urls import path
from .views import *

urlpatterns = [
    path('schedule/',schedule_task_view,name='schedule_task_view'),
    path('send-email/',send_email_view,name='send_email_view'),
]