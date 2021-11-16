from types import LambdaType
from typing import Generator
from bs4 import BeautifulSoup
import requests
import datetime
import json
import boto3
# boto3는 AWS 버킷에 접근하기 위해  import한 모듈로서, 로컬에서 테스트하기에는 어려움이 있음.
# 따라서 버킷에 접근하는 코드의 경우, 메인에 올려서 직접 실행해봐야함.
# 로컬에서 다른 코드 테스트시 오류 방지 하기 위함.
#
# from resource import Constant
from return_type_generator import ReturnType
from return_type_generator import ParamOptions
import sandol_constant as Constant

GEN = ReturnType()  # kakao-i type json generator
GEN_OPTION = ParamOptions()  # generator optional param










class Test:  # 테스트 블럭이 참조할 클래스 (직접 테스트해야하는경우에 해당 클래스에 작성 후 테스트 발화시 결과 나옴.)
    def __init__(self):
        pass

    def commerce_test(self):
        import random
        return_json = {
            "version": "2.0",
            "template": {
                "outputs": [
                ],
                "quickReplies": [
                    {
                        "messageText": "도움말",
                        "action": "message",
                        "label": "도움말"
                    }
                ]
            }
        }
        Commerce_test = lambda random_image: {
            "commerceCard": {
                "description": "산돌분식 방분하여 해당 광고를 보여주시면 해당 메뉴의 할인이 적용됩니다.",
                "price": 4000,
                "discount": 500,
                "currency": "won",
                "thumbnails": [
                    {
                        "imageUrl": random_image,
                        "link": {
                            "web": "http://naver.me/FMA7h2K7"
                        }
                    }
                ],
                "profile": {
                    "imageUrl": random_image,
                    "nickname": "산돌 분식"
                },
                "buttons": [
                    {
                        "label": "네이버 플레이스 연결",
                        "action": "webLink",
                        "webLinkUrl": "http://naver.me/FMA7h2K7 "
                    },
                    {
                        "label": "전화하기",
                        "action": "phone",
                        "phoneNumber": "010-4183-2998"
                    },
                    {
                        "label": "공유하기",
                        "action": "share"
                    }
                ]
            }
        }
        # 1~5 산돌 분식, 6 산돌 카페
        Commerce_image = [
            'https://raw.githubusercontent.com/hhhminme/kpu_sandol_team/main/commerce_img/commerce_test1.png',
            'https://raw.githubusercontent.com/hhhminme/kpu_sandol_team/main/commerce_img/commerce_test2.png',
            'https://raw.githubusercontent.com/hhhminme/kpu_sandol_team/main/commerce_img/commerce_test3.png',
            'https://raw.githubusercontent.com/hhhminme/kpu_sandol_team/main/commerce_img/commerce_test4.png',
            'https://raw.githubusercontent.com/hhhminme/kpu_sandol_team/main/commerce_img/commerce_test5.png',
            'https://raw.githubusercontent.com/hhhminme/kpu_sandol_team/main/commerce_img/commerce_test6.png'
        ]

        random_image = Commerce_image[random.randint(0, 5)]
        return_json['template']['outputs'].append(Commerce_test(random_image))
        return return_json


if __name__ == "__main__":
    print(GEN.set_card(Constant.SANDOL_LOGO1, GEN_OPTION.button(label="세미콘 식당", action="webLink",
                                                                webLinkUrl="https://qr.kakaopay.com/2810060111751110120069009c404611"), is_title="title", is_description="dsc", flag=False))
