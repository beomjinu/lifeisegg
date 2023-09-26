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
        ('WAITING_FOR_PAYMENT', 'WAITING_FOR_PAYMENT'),  # 결제 대기중
        ('WAITING_FOR_DEPOSIT', 'WAITING_FOR_DEPOSIT'),  # 입금 대기중
        ('DONE_PAYMENT', 'DONE_PAYMENT'),  # 결제 완료
        ('DONE_SEND', 'DONE_SEND'),  # 발송 완료
        ('CANCELED', 'CANCELED'),  # 주문 취소 (환불)
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
            'WAITING_FOR_PAYMENT': '결제를 기다리고 있어요.',
            'WAITING_FOR_DEPOSIT': '입금을 완료해주세요.',
            'DONE_PAYMENT': '결제가 완료되었어요.',
            'DONE_SEND': '상품 발송을 완료했어요.',
            'CANCELED': '주문이 취소되었어요.',
        }[self.status]

class Item(models.Model):
    order    = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    content  = models.CharField(max_length=99)
    price    = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()

    @property
    def total_price(self):
        return self.price * self.quantity