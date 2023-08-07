from django.urls import path
from . import views

app_name = "terms"

urlpatterns = [
    path("<str:page_name>/", views.page, name="page"),
]
