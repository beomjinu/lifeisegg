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
        ('DS', 'DONE_SEND'),
        ('C', 'CANCLED'),
    )

    status           = models.CharField(max_length=99, choices=status_choices)

    def get_kr_created_at(self):
        return self.created_at.strftime("%Y년 %m월 %d일 %H시 %M분")
    
    def get_simple_items(self):
        return self.items.all()[0].content + (('외 ' + str(len(self.items.all()) - 1) + '개') if (len(self.items.all()) - 1) != 0 else '')

    def get_display_status(self):
        return {
            'WFP': '결제를 기다리고 있습니다.',
            'DP': '결제가 완료되었습니다.',
            'DS': '상품을 발송 완료하였습니다.',
            'C': '취소된 주문입니다.'
        }[self.status]
    
    def get_amount(self):
        return sum([item.get_total_price() for item in self.items.all()])

    def get_format_amount(self):
        return format(self.get_amount(), ',')

class Item(models.Model):
    order    = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    content  = models.CharField(max_length=99)
    price    = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()

    def format_price(self):
        return format(self.price, ',')

    def get_total_price(self):
        return self.price * self.quantity

    def format_total_price(self):
        return format(self.get_total_price(), ',')