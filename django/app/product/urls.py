from django.urls import path
from . import views

app_name = 'product'

urlpatterns = [
    path('<int:product_id>/', views.detail, name='detail'),
    path('ep/<str:name>/', views.enginePage, name='ep'),
]
