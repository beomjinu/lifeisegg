from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from shop.views import redirect_index

urlpatterns = [
    path('adminpage/', admin.site.urls),
    path('shop/', include("shop.urls")),
    path('', redirect_index),
    path('terms/', include("terms.urls"))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
