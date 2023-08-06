import requests
import time
import uuid


class ClovaOCR:
    def __init__(self):
        self.headers = {
            'Accept' : 'application/json, text/plain, */*'
        }
        self.ocr_modes = {
            # API                   # 기능              # 지원 언어
            'general',              # 일반              ko, ja, en
            'receipt',              # 영수증            ko, ja, en
            'credit-card',          # 신용카드          ko, ja, en
            'business-license',     # 사업자 등록증     ko
            'giro',                 # 고지서            ko
            'name-card',            # 명함              ko, ja, en
            'id-card',              # 신분증            ko, ja
            'invoice',              # 청구서            ja
        }


    def run_ocr(self, image_path, language_code, ocr_mode='general'):
        timestamp = int(time.time() *1000)
        uuid4 = uuid.uuid4()
        guid = uuid4.hex

        upload = {
            'image': open(image_path, 'rb')
        }

        r = requests.post(
            url = f"https://clova.ai/ocr/api/{ocr_mode}/{language_code}/recognition?ts={timestamp}&s={guid}",
            headers = self.headers,
            files = upload
        )
        return r.json()['raw']
