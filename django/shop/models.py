from django.db import models
from django.urls import reverse

class Product(models.Model):
    name        = models.CharField(max_length=99)
    price       = models.PositiveIntegerField()
    discounted  = models.PositiveIntegerField()
    post        = models.TextField(default='')
    priority    = models.IntegerField()

    def __str__(self):
        return self.name
    
    def format_price(self):
        return format(self.price, ',')

    def format_discounted(self):
        return format(self.discounted, ',')
    
    def is_sold_out(self):
        return all([option.is_sold_out for option in self.options.all()])
    
    def get_absolute_url(self):        
        return reverse('shop:detail', kwargs={'product_id': self.id})

class Option(models.Model):
    product     = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='options')
    content     = models.CharField(max_length=99)
    price       = models.IntegerField(default=0)
    is_sold_out = models.BooleanField(default=False)
    priority    = models.IntegerField()

    def __str__(self):
        return f'{self.product} | {self.content}'
    
    def total_price(self):
        return self.product.discounted + self.price
    
    def format_price(self):
        return format(self.price, ',')
    
    def format_total_price(self):
        return format(self.total_price(), ',')
    
    def full_content(self):
        return f'{self.product.name} | {self.content}'


class Image(models.Model):
    product     = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image       = models.ImageField(upload_to='')
    priority    = models.IntegerField()

    def __str__(self):
        return f'{self.product} - {self.priority}'
