from utils.tosspayments import TossPayments
from django.db import models

from datetime import datetime


class Order(models.Model):
    order_id         = models.CharField(max_length=99, null=True, blank=True)
    orderer_name     = models.CharField(max_length=99)
    orderer_number   = models.CharField(max_length=99)
    recipient_name   = models.CharField(max_length=99)
    recipient_number = models.CharField(max_length=99)
    address          = models.CharField(max_length=99)
    request          = models.CharField(max_length=99, null=True, blank=True)
    created_at       = models.DateTimeField(auto_now_add=True)
    delivery         = models.CharField(max_length=99, null=True, blank=True)
    
    status_choices   = (
        ('WFP', 'WAITING_FOR_PAYMENT'),
        ('DP', 'DONE_PAYMENT'),
        ('DS', 'DONE_SEND'),
        ('C', 'CANCLED'),
    )

    status           = models.CharField(max_length=99, choices=status_choices)

    @property
    def amount(self) -> int:
        return sum([item.total_price for item in self.items.all()])
    
    @property
    def content(self) -> str:
        return self.items.all()[0].content + (('외 ' + str(len(self.items.all()) - 1) + '개') if (len(self.items.all()) - 1) != 0 else '')

    @property
    def status_display(self) -> str:
        return {
            'WFP': '결제를 기다리고 있어요.',
            'DP': '결제가 완료되었어요.',
            'DS': '상품 발송을 완료했어요.',
            'C': '주문이 취소되었어요.'
        }[self.status]
    
    @property
    def payment(self) -> dict:
        toss = TossPayments()
        response = toss.inquiry(order_id=self.order_id)
        
        data = response.json()
        data['approvedAt'] = datetime.strptime(data['approvedAt'], '%Y-%m-%dT%H:%M:%S%z')

        return data

class Item(models.Model):
    order    = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    content  = models.CharField(max_length=99)
    price    = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()

    @property
    def total_price(self):
        return self.price * self.quantity