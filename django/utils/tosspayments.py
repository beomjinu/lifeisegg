from django.conf import settings
import requests, base64

class TossPayments:
    def __init__(self):
        self.secret_key = settings.ENV_DATA['TOSS_SK']
        self.base_url = 'https://api.tosspayments.com'

        self.headers = {
            'Authorization': "Basic " + base64.b64encode((self.secret_key + ":").encode("utf-8")).decode("utf-8"),
            'Content-Type': "application/json"
        }

    def inquiry(self, order_id: str):
        url = f'{self.base_url}/v1/payments/orders/{order_id}'
        
        return requests.get(url, headers=self.headers)

    def success(self, payload: dict):
        url = f'{self.base_url}/v1/payments/confirm'

        return requests.post(url, json=payload, headers=self.headers)

    def cancel(self, order_id: str, payload: dict={'cancelReason': 'Cancel'}):
        payment_key = self.inquiry(order_id=order_id).json()['paymentKey']
        url = f'{self.base_url}/v1/payments/{payment_key}/cancel'

        return requests.post(url, json=payload, headers=self.headers)