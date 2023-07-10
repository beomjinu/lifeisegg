import platform, os, requests, time, datetime, uuid, hmac, hashlib, json
from django.conf import settings

class Message:
    def __init__(self):
        self.default_agent = {
            'sdkVersion': 'python/4.2.0',
            'osPlatform': platform.platform() + " | " + platform.python_version()
        }

        self.url       = "https://api.solapi.com/messages/v4/send"
        self.date      = self.get_iso_datetime()
        self.salt      = str(uuid.uuid1().hex)

        self.headers = {
            'Authorization': 'HMAC-SHA256 ApiKey=' + settings.SOLAPI_CK + ', Date=' + self.date + ', salt=' + self.salt + ', signature=' + (hmac.new((settings.SOLAPI_SK).encode(), (self.date + self.salt).encode(), hashlib.sha256).hexdigest()),
            'Content-Type': 'application/json; charset=utf-8'
        }

        self.templates = {
            '주문접수': 'KA01TP230701162116367VjEPEehkl6I',
            '발송완료': 'KA01TP230708122917670lqAsmIPnu7C'
        }        
    
    def get_iso_datetime(self):
        utc_offset_sec = time.altzone if time.localtime().tm_isdst else time.timezone
        utc_offset = datetime.timedelta(seconds=-utc_offset_sec)

        return datetime.datetime.now().replace(tzinfo=datetime.timezone(offset=utc_offset)).isoformat()    

    def create_send_data(self, data):
        self.send_data = {
            "agent": self.default_agent,

            'message': {
                'to': data["to"],
                'from': settings.ALIMTALK_FROM_NUMBER,
                
                'kakaoOptions': {
                    'pfId': settings.SOLAPI_PFID,
                    'templateId': self.templates[data["template"]],
                    'variables': data["var"]
                }
            }
        }
    
    def send(self):
        return requests.post(self.url, headers=self.headers, json=self.send_data)