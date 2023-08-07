from django.db import models
from django.urls import reverse 

class Page(models.Model):
    name            = models.CharField(max_length=99, unique=True)
    display_name    = models.CharField(max_length=99, null=True)
    content         = models.TextField()
    created_at      = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('terms:page', kwargs={'page_name': self.name})

    

