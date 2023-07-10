from django.db import models
from app.order.models import Order
from datetime import datetime
import json, base64

class Payment(models.Model):
    order       = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='payment')
    data        = models.TextField(null=True, blank=True)

    def get_data(self):
        return json.loads(base64.b64decode(self.data.encode('utf-8')).decode('utf-8')) 
    
    def get_approved_at(self):
        return datetime.strptime(self.get_data()['approvedAt'], '%Y-%m-%dT%H:%M:%S%z')
    
    def format_approved_at(self):
        return self.get_approved_at().strftime('%Y년 %m월 %d일 %H시 %M분')  