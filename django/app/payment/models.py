from django.db import models
from app.order.models import Order
from datetime import datetime

from utils.tosspayments import TossPayments

import base64, json

class Payment(models.Model):
    order = models.OneToOneField(Order, related_name='payment', on_delete=models.CASCADE)
    data  = models.TextField()

    def get_data(self) -> dict:
        return json.loads(base64.b64decode(self.data.encode('utf-8')).decode('utf-8'))
    
    def update_data(self) -> dict:
        tosspayments = TossPayments()
        self.data = base64.b64encode(json.dumps(tosspayments.inquiry(order_id=self.order.order_id).json()).encode('utf-8')).decode('utf-8')
        self.save()

    @property
    def status(self) -> str:
        return self.get_data()['status']
    
    @property
    def method(self) -> str:
        return self.get_data()['method']
    
    @property
    def virtual_account(self) -> str:
        return {
            '039': '경남은행',
            '034': '광주은행',
            '004': 'KB국민은행',
            '003': 'IBK기업은행',
            '011': 'NH농협은행',
            '031': 'DGB대구은행',
            '032': '부산은행',
            '045': '새마을금고',
            '007': 'Sh수협은행',
            '088': '신한은행',
            '020': '우리은행',
            '071': '우체국예금보험',
            '037': '전북은행',
            '081': '하나은행'
        }[self.get_data()['virtualAccount']['bankCode']] + ' ' + self.get_data()['virtualAccount']['accountNumber'][1:]
    
    @property
    def approved_at(self) -> datetime:
        return datetime.fromisoformat(self.get_data()['approvedAt'])
    
    @property
    def due_date(self) -> datetime:
        return datetime.fromisoformat(self.get_data()['virtualAccount']['dueDate'])
