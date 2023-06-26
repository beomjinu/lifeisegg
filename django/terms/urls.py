from django.urls import path
from . import views

app_name = "terms"

urlpatterns = [
    path("policy/", views.policy, name="policy"),
    path("privacy/", views.privacy, name="privacy"),
]