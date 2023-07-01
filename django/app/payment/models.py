from django.db import models
from app.order.models import Order

class Payment(models.Model):
    order       = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='payment')
    amount      = models.PositiveIntegerField()
    status      = models.CharField(max_length=99)
    created_at  = models.DateTimeField(auto_now_add=True)

    def format_amount(self):
        return format(self.amount, ',')
    
    def korean_created_at(self):
        return self.created_at.strftime("%Y년 %m월 %d일 %H시 %M분")
