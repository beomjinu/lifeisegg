from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from django.shortcuts import render, HttpResponse
from app.product.sitemaps import ProductSitemap
from app.product.views import index
from app.terms.sitemaps import TermsSitemap

sitemaps = {
    'Product': ProductSitemap,
    'Trems': TermsSitemap, 
}

urlpatterns = [
    # admin
    path('adminpage/', admin.site.urls),
    
    # index
    path('', index, name='index'),

    # apps
    path('product/', include("app.product.urls")),
    path('terms/', include("app.terms.urls")),
    path('order/', include("app.order.urls")),
    path('payment/', include('app.payment.urls')),
    path('cart/', include('app.cart.urls')),
    path('notice/', include('app.notice.urls')),

    # summernote
    path('summernote/', include('django_summernote.urls')),
    
    # sitemap.xml
    path('sitemap.xml', sitemap, {'sitemaps': {'Product': ProductSitemap, 'Trems': TermsSitemap}}, name='sitemap'),

    # 404.html
    path('404.html', lambda request: render(request, '404.html')),

    # robots.txt
    path('robots.txt', lambda request: render(request, 'robots.txt', content_type='text/plain')),

    # naver site verification
    path('https://lifeisegg.shop/naverea9d173cbeb8aac596f5da4df2b85695.html', lambda _: HttpResponse('naver-site-verification: naverea9d173cbeb8aac596f5da4df2b85695.html'))

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
