class Return_Type:  # 리턴 타입별 JSON 형식을 만드는 곳 입니다.
    def __init__(self):
        self.return_json = {
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
    def init_json(self):
        self.return_json = {
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
    #Return Type 이 1이면 텍스트, 2면 카드, 3이면

    def is_Text(self, text):  #텍스트 형식
        self.init_json()
        basic_text ={
                        "simpleText": {
                            "text": str(text)
                        }
                    }
        self.return_json["template"]["outputs"].append(basic_text)
        return self.return_json

    def is_Card(self,thumb_img, *is_buttons, is_title = None, is_description = None):  #카드 형식
        self.init_json()
        basic_card = {
            "thumbnail": {
                "imageUrl": thumb_img
            }
        }

        try:
            if is_title != None:
                basic_card["title"] = is_title  #타이틀 입력

            if is_description != None:
                basic_card["description"] = is_description  # 설명 입력

            if is_buttons != ():
                if len(is_buttons) > 3:
                    raise Exception("Buttons are must less then 3") # 버튼이 3개 이상이라면 오류 발생
                else:
                    basic_card.update({"buttons": list(is_buttons)})

            self.return_json["template"]["outputs"].append({"basicCard": basic_card})   # 위 정보들을 return_json에 입력
            return self.return_json

        except Exception as e:  #오류 발생시 오류 코드 리턴
            basic_card["description"] = "error :" + str(e)
            self.return_json["template"]["outputs"].append({"basicCard": basic_card})
            return self.return_json

    def is_Image(self): # 이미지 반환 형식
        return_json = {
                        "version": "2.0",
                        "template": {
                            "outputs": [
                                {
                                    "simpleImage": {
                                        "imageUrl": "http://k.kakaocdn.net/dn/83BvP/bl20duRC1Q1/lj3JUcmrzC53YIjNDkqbWK/i_6piz1p.jpg",
                                        "altText": "보물상자입니다"
                                    }
                                }
                            ]
                        }
                    }
        return return_json

    def is_commerce(self):  # 커머스 반환 형식
        return_json = {
                          "version": "2.0",
                          "template": {
                            "outputs": [
                              {
                                "commerceCard": {
                                  "description": "따끈따끈한 보물 상자 팝니다",
                                  "price": 10000,
                                  "discount": 1000,
                                  "currency": "won",
                                  "thumbnails": [
                                    {
                                      "imageUrl": "http://k.kakaocdn.net/dn/83BvP/bl20duRC1Q1/lj3JUcmrzC53YIjNDkqbWK/i_6piz1p.jpg",
                                      "link": {
                                        "web": "https://store.kakaofriends.com/kr/products/1542"
                                      }
                                    }
                                  ],
                                  "profile": {
                                    "imageUrl": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT4BJ9LU4Ikr_EvZLmijfcjzQKMRCJ2bO3A8SVKNuQ78zu2KOqM",
                                    "nickname": "보물상자 팝니다"
                                  },
                                  "buttons": [
                                    {
                                      "label": "구매하기",
                                      "action": "webLink",
                                      "webLinkUrl": "https://store.kakaofriends.com/kr/products/1542"
                                    },
                                    {
                                      "label": "전화하기",
                                      "action": "phone",
                                      "phoneNumber": "354-86-00070"
                                    },
                                    {
                                      "label": "공유하기",
                                      "action": "share"
                                    }
                                  ]
                                }
                              }
                            ]
                          }
                        }
        return return_json


    def is_Carousel(self):  #케로셀 반환 형식
       return_json =  {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "carousel": {
                            "type": "basicCard",
                            "items": [
                                {
                                    "title": "보물상자",
                                    "description": "보물상자 안에는 뭐가 있을까",
                                    "thumbnail": {
                                        "imageUrl": "http://k.kakaocdn.net/dn/83BvP/bl20duRC1Q1/lj3JUcmrzC53YIjNDkqbWK/i_6piz1p.jpg"
                                    },
                                    "buttons": [
                                        {
                                            "action": "message",
                                            "label": "열어보기",
                                            "messageText": "짜잔! 우리가 찾던 보물입니다"
                                        },
                                        {
                                            "action": "webLink",
                                            "label": "구경하기",
                                            "webLinkUrl": "https://e.kakao.com/t/hello-ryan"
                                        }
                                    ]
                                },
                                {
                                    "title": "보물상자2",
                                    "description": "보물상자2 안에는 뭐가 있을까",
                                    "thumbnail": {
                                        "imageUrl": "http://k.kakaocdn.net/dn/83BvP/bl20duRC1Q1/lj3JUcmrzC53YIjNDkqbWK/i_6piz1p.jpg"
                                    },
                                    "buttons": [
                                        {
                                            "action": "message",
                                            "label": "열어보기",
                                            "messageText": "짜잔! 우리가 찾던 보물입니다"
                                        },
                                        {
                                            "action": "webLink",
                                            "label": "구경하기",
                                            "webLinkUrl": "https://e.kakao.com/t/hello-ryan"
                                        }
                                    ]
                                },
                                {
                                    "title": "보물상자3",
                                    "description": "보물상자3 안에는 뭐가 있을까",
                                    "thumbnail": {
                                        "imageUrl": "http://k.kakaocdn.net/dn/83BvP/bl20duRC1Q1/lj3JUcmrzC53YIjNDkqbWK/i_6piz1p.jpg"
                                    },
                                    "buttons": [
                                        {
                                            "action": "message",
                                            "label": "열어보기",
                                            "messageText": "짜잔! 우리가 찾던 보물입니다"
                                        },
                                        {
                                            "action": "webLink",
                                            "label": "구경하기",
                                            "webLinkUrl": "https://e.kakao.com/t/hello-ryan"
                                        }
                                    ]
                                }
                            ]
                        }
                    }
                ]
            }
        }
       return return_json

import json
rt = Return_Type()
print(rt.is_Card("None"))

result = {
        'statusCode': 200,
        'body': json.dumps(rt.is_Text("간단한 텍스트 요소입니다.")),
        'headers': {
            'Access-Control-Allow-Origin': '*',
        }
    }

