from django.urls import path
from . import views

app_name = 'order'

urlpatterns = [
    path('form/', views.form, name='form'),
    path('<str:order_id>', views.inquiry, name='inquiry'),
]