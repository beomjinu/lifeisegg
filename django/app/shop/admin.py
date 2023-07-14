from django.contrib import admin
from .models import Product, Option, Image

class OptionInline(admin.TabularInline):
    model = Option

class ImageInline(admin.TabularInline):
    model = Image

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'discounted', 'price'] 
    list_filter = ['priority']
    search_fields = ['name']
    inlines = [OptionInline, ImageInline]

admin.site.register(Product, ProductAdmin)