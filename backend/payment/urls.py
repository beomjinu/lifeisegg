from django.urls import path
from . import views

app_name = 'payment'

urlpatterns = [
    path('open/<str:order_id>/', views.open, name='open'),
    path('success/', views.success, name='success'),
    path('fail/', views.fail, name='fail'),
]