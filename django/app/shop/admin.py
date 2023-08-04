from django_summernote.admin import SummernoteModelAdmin
from .models import Product, Option, Image
from django.contrib import admin

class OptionInline(admin.TabularInline):
    model = Option

class ImageInline(admin.TabularInline):
    model = Image

@admin.register(Product)
class ProductAdmin(SummernoteModelAdmin):
    list_display = ['name', 'discounted', 'price']
    list_filter = ['priority']
    search_fields = ['name']
    inlines = [OptionInline, ImageInline]