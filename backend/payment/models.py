from django.db import models
from order.models import Order

class Payment(models.Model):
    order       = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='payment')
    amount      = models.PositiveIntegerField()
    status      = models.CharField(max_length=99)
    created_at  = models.DateTimeField(auto_now_add=True)
