from django.contrib import admin
from .models import Product, Option, Image

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'discounted', 'price',)  # 관리자 페이지 목록에 표시될 필드
    list_filter = ('priority',)  # 필드를 기준으로 필터링할 수 있는 옵션
    search_fields = ('name',)

admin.site.register(Product, ProductAdmin)
admin.site.register(Option)
admin.site.register(Image)