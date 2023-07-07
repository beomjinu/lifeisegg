from django.db import models

class Order(models.Model):
    order_id         = models.CharField(max_length=99, null=True, blank=True)
    orderer_name     = models.CharField(max_length=99)
    orderer_number   = models.CharField(max_length=99)
    orderer_email    = models.EmailField(max_length=99)
    recipient_name   = models.CharField(max_length=99)
    recipient_number = models.CharField(max_length=99)
    address          = models.CharField(max_length=99)
    request          = models.CharField(max_length=99, null=True, blank=True)
    created_at       = models.DateTimeField(auto_now_add=True)
    delivery         = models.CharField(max_length=99, null=True, blank=True)
    
    status_choices   = (
        ('WFP', 'WAITING_FOR_PAYMENT'),
        ('DP', 'DONE_PAYMENT'),
        ('IPD', 'IN_PROGRESS_DELIVERY'),
        ('DD', 'DONE_DELIVERY'),
        ('C', 'CANCLED'),
    )

    status           = models.CharField(max_length=99, choices=status_choices)

    def korean_created_at(self):
        return self.created_at.strftime("%Y년 %m월 %d일 %H시 %M분")
    
    def simple_created_at(self):
        return self.created_at.strftime("%y.%m.%d %H:%M")
    
    def simple_items(self):
        return self.items.all()[0].content + (('외 ' + str(len(self.items.all()) - 1) + '개') if (len(self.items.all()) - 1) != 0 else '')

    def display_status(self):
        return {
            'WFP': '결제를 기다리고 있습니다.',
            'DP': '결제가 완료되었습니다.',
            'IPD': '배송 중인 주문입니다.',
            'DD': '배송이 완료되었습니다.',
            'C': '취소된 주문입니다.'
        }[self.status]
    
    def simple_display_status(self):
        return {
            'WFP': '결제 대기',
            'DP': '결제 완료',
            'IPD': '배송 중',
            'DD': '배송 완료',
            'C': '취소'
        }[self.status]
    
    def amount(self):
        return sum([item.total_price() for item in self.items.all()])

    def format_amount(self):
        return format(self.amount(), ',')

class Item(models.Model):
    order    = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    content  = models.CharField(max_length=99)
    price    = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()

    def format_price(self):
        return format(self.price, ',')

    def total_price(self):
        return self.price * self.quantity

    def format_total_price(self):
        return format(self.total_price(), ',')