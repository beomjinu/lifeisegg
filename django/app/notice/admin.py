from django_summernote.admin import SummernoteModelAdmin
from django.contrib import admin
from .models import Notice

@admin.register(Notice)
class NoticeAdmin(SummernoteModelAdmin):
    list_display = ['title', 'created_at']

