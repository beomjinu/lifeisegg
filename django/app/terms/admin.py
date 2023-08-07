from django_summernote.admin import SummernoteModelAdmin
from .models import Page
from django.contrib import admin

@admin.register(Page)
class TermsAdmin(SummernoteModelAdmin):
    list_display = ['display_name', 'created_at']
