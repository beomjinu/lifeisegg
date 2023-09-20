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
        ('WFP', 'WAITING_FOR_PAYMENT'), # 결제 대기중
        ('WFD', 'WAITING_FOR_DEPOSIT'), # 입금 대기중
        ('DP', 'DONE_PAYMENT'), # 결제 완료
        ('DS', 'DONE_SEND'), # 발송 완료
        ('C', 'CANCLED'), # 결제 취소 (환불)
        ('A', 'ABORTED'), # 결제 실패
        ('E', 'EXPIRED') # 
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
            'WFD': '입금을 완료해주세요.',
            'DP': '결제가 완료되었어요.',
            'DS': '상품 발송을 완료했어요.',
            'C': '주문이 취소되었어요.',
            'A': '결제를 실패했어요.',
        }[self.status]
    
    @property
    def payment(self) -> dict:
        toss = TossPayments()
        response = toss.inquiry(order_id=self.order_id)
        
        data = response.json()

        if data['method'] == '가상계좌' and data['status'] == 'WAITING_FOR_DEPOSIT':
            data['virtualAccount']['bank'] = {
                '32': '부산',
                '37': '전북',
                '07': '수협',
                '20': '우리',
                '88': '신한',
                '71': '우체국',
                '03': '기업',
                '31': '대구',
                '11': '농협',
                '45': '새마을',
                '39': '경남',
                '34': '광주',
                '04': '국민',
                '81': '하나',
                '89': '케이',
            }[data['virtualAccount']['bankCode']]

            data['virtualAccount']['accountNumber'] = data['virtualAccount']['accountNumber'][1:]
        else:
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