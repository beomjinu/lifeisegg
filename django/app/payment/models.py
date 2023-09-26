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
            "88": "신한은행",
            "06": "국민은행",
            "45": "새마을금고",
            "34": "광주은행",
            "11": "농협은행",
            "03": "기업은행",
            "20": "우리은행",
            "07": "수협은행",
            "37": "전북은행",
            "89": "케이뱅크"
        }[self.get_data()['virtualAccount']['bankCode']] + ' ' + self.get_data()['virtualAccount']['accountNumber'][1:]
    
    @property
    def approved_at(self) -> datetime:
        return datetime.fromisoformat(self.get_data()['approvedAt'])
    
    @property
    def due_date(self) -> datetime:
        return datetime.fromisoformat(self.get_data()['virtualAccount']['dueDate'])
