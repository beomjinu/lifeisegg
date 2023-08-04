from django.db import models
from django.urls import reverse

class Product(models.Model):
    name        = models.CharField(max_length=99)
    og_img      = models.ImageField(upload_to='', null=True, blank=True)
    price       = models.PositiveIntegerField()
    discounted  = models.PositiveIntegerField()
    description = models.TextField(null=True, blank=True)
    post        = models.TextField(null=True, blank=True)
    priority    = models.IntegerField()

    def __str__(self):
        return self.name
    
    @property
    def is_sold_out(self) -> bool:
        return all([option.is_sold_out for option in self.options.all()])
    
    @property
    def solted_images(self):
        return self.images.all().order_by('priority')
    
    @property
    def solted_options(self):
        return self.options.all().order_by('priority')
    
    def get_absolute_url(self):        
        return reverse('shop:detail', kwargs={'product_id': self.id})

class Option(models.Model):
    product     = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='options')
    content     = models.CharField(max_length=99)
    price       = models.IntegerField(default=0)
    is_sold_out = models.BooleanField(default=False)
    priority    = models.IntegerField()

    def __str__(self):
        return f'{self.product.name} | {self.content}'
    
    @property
    def total_price(self) -> int:
        return self.product.discounted + self.price

class Image(models.Model):
    product     = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image       = models.ImageField(upload_to='')
    priority    = models.IntegerField()

    def __str__(self):
        return f'{self.product} - {self.priority}'
