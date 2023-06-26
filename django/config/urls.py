from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap

from shop.views import redirect_index

from shop.sitemaps import ProductSitemap
from terms.sitemaps import TermsSitemap

sitemaps = {
    'Product': ProductSitemap,
    'Trems': TermsSitemap, 
}

urlpatterns = [
    # admin
    path('adminpage/', admin.site.urls),
    
    # apps
    path('shop/', include("shop.urls")),
    path('', redirect_index), # redirect shop/
    path('terms/', include("terms.urls")),
    path('order/', include("order.urls")),
    path('payment/', include('payment.urls')),
    path('cart/', include('cart.urls')),
    
    # sitemaps
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='sitemap'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
