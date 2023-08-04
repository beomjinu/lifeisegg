from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from django.shortcuts import render, HttpResponse

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

    # summernote
    path(r'^summernote/', include('django_summernote.urls')),
    
    # sitemap.xml
    path('sitemap.xml', sitemap, {'sitemaps': {'Product': ProductSitemap, 'Trems': TermsSitemap}}, name='sitemap'),

    # 404.html
    path('404.html', lambda request: render(request, '404.html')),

    # robots.txt
    path('robots.txt', lambda request: render(request, 'robots.txt', content_type='text/plain')),

    # naver site verification
    path('naver19af3aceb3c4654e177ebb055319e0b3.html', lambda _: HttpResponse('naver-site-verification: naver19af3aceb3c4654e177ebb055319e0b3.html'))

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
