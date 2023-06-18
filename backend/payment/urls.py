from django.urls import path
from . import views

app_name = 'payment'

urlpatterns = [
    path('<str:order_id>/', views.payment, name='payment'),
]