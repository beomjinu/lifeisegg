from django.db import models

class Product(models.Model):
    name        = models.CharField(max_length=99)
    price       = models.PositiveIntegerField()
    discounted  = models.PositiveIntegerField()
    post        = models.TextField(default='')
    priority    = models.IntegerField()

    def __str__(self):
        return self.name

class Option(models.Model):
    product     = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='options')
    content     = models.CharField(max_length=99)
    price       = models.IntegerField(default=0)
    is_sold_out = models.BooleanField(default=False)
    priority    = models.IntegerField()

    def __str__(self):
        return f'{self.product} - {self.content}'

class Image(models.Model):
    product     = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image       = models.ImageField(upload_to='')
    priority    = models.IntegerField()

    def __str__(self):
        return f'{self.product} - {self.priority}'
