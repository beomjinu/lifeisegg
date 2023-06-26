from django.contrib.sitemaps import Sitemap
from django.urls import reverse

class TermsSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9

    def items(self):
        return [
            'terms:policy',
            'terms:privacy',
        ]
    
    def location(self, item):
        return reverse(item)