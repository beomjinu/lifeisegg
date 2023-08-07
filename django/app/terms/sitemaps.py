from django.contrib.sitemaps import Sitemap
from .models import Page

class TermsSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9

    def items(self):
        return Page.objects.all().order_by('id')
