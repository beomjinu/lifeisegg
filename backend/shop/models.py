from django.db import models

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
