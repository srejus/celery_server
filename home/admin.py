from django.contrib import admin
from .models import *

# Register your models here.
class EmailLogAdmin(admin.ModelAdmin):
    list_display = ['from_email','to_email','subject','created_at']


admin.site.register(EmailLog,EmailLogAdmin)