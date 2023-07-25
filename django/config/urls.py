from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from django.shortcuts import render

from app.shop.sitemaps import ProductSitemap
from app.terms.sitemaps import TermsSitemap

sitemaps = {
    'Product': ProductSitemap,
    'Trems': TermsSitemap, 
}

urlpatterns = [
    # admin
    path('adminpage/', admin.site.urls),
    
    # apps
    path('', include("app.shop.urls")),
    path('terms/', include("app.terms.urls")),
    path('order/', include("app.order.urls")),
    path('payment/', include('app.payment.urls')),
    path('cart/', include('app.cart.urls')),
    
    # sitemaps
    path('sitemap.xml', sitemap, {'sitemaps': {'Product': ProductSitemap, 'Trems': TermsSitemap}}, name='sitemap'),

    # 404
    path('404.html', lambda request: render(request, '404.html', {}))

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
