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
            '39': '경남은행',
            '34': '광주은행',
            '04': 'KB국민은행',
            '03': 'IBK기업은행',
            '11': 'NH농협은행',
            '31': 'DGB대구은행',
            '32': '부산은행',
            '45': '새마을금고',
            '07': 'Sh수협은행',
            '88': '신한은행',
            '20': '우리은행',
            '71': '우체국예금보험',
            '37': '전북은행',
            '81': '하나은행'
        }[self.get_data()['virtualAccount']['bankCode']] + ' ' + self.get_data()['virtualAccount']['accountNumber']
    
    @property
    def approved_at(self) -> datetime:
        return datetime.fromisoformat(self.get_data()['approvedAt'])
    
    @property
    def due_date(self) -> datetime:
        return datetime.fromisoformat(self.get_data()['virtualAccount']['dueDate'])
