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
        self.common_params = Common_params()

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

    def is_Text(self, text):  #텍스트 형식
        self.init_json()
        basic_text ={
                        "simpleText": {
                            "text": str(text)
                        }
                    }
        self.return_json["template"]["outputs"].append(basic_text)
        return self.return_json

    def is_Card(self,thumb_img, *is_buttons, is_title = None, is_description = None, flag = False):  #카드 형식
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

            if flag == True:    #flag 가 True이면 Card Json만 반환하지만, False이면 return해야하는 기본 JSON도 포함이 된다.
                return basic_card

            else:
                self.return_json["template"]["outputs"].append({"basicCard": basic_card})   # 위 정보들을 return_json에 입력
                return self.return_json

        except Exception as e:  #오류 발생시 오류 코드 리턴
            basic_card["description"] = "error :" + str(e)
            self.return_json["template"]["outputs"].append({"basicCard": basic_card})
            return self.return_json

    def is_Image(self, src, text = None): # 이미지 반환 형식
        self.init_json()
        basic_image ={
        "simpleImage": {
            "imageUrl": src,
            }
        }

        if text != None:
            basic_image["simpleImage"]["altText"] = text

        self.return_json["template"]["outputs"].append(basic_image)
        return self.return_json

    def is_commerce(self,thumbnail, description, price, currency, is_discount = None, is_discountRate = None, is_discountedPrice = None, profile = None, **kwargs):  # 커머스 반환 형식
        self.common_params.Button(**kwargs)
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


    def is_Carousel(self, card_type, card_num, *params):  #케로셀 반환 형식    #(link, Title, description)

        basic_carousel =  {
                        "carousel": {
                            "type": card_type,
                            "items": []
                        }
                    }
        if card_type == "basicCard":
            for param in range(card_num): # thumb_img, *is_buttons, is_title = None, is_description = None
                basic_carousel['carousel']['items'].append(self.is_Card(thumb_img = params[param][0], is_title = params[param][1], is_description = params[param][2], flag= True))

        else:
            for param in range(card_num): # thumb_img, *is_buttons, is_title = None, is_description = None
                basic_carousel['carousel']['items'].append(self.is_Card(thumb_img = params[param][0], is_title = params[param][1], is_description = params[param][2], flag= True))
        self.return_json["template"]["outputs"].append(basic_carousel)
        return self.return_json



class Common_params:

    #kwargs로 들어올 수 있는 값은 DOCS를 참조
    # label = string
    # action = string
    # webLinkUrl = string | action = webLink
    # messageText = string | action = message or block
    # phoneNumber = string | action = phone
    # blockId = string | action = block
    # extra ...
    def Button(self, **kwargs):
        data = {}
        params = ['label', 'action', 'webLinkUrl', 'messageText', 'phoneNumber', 'blockId']
        for item in kwargs.items():
            if item[0] not in params:
                data.clear()
                data["label"] = "error, Check Parameter"
                break
            data[item[0]] = item[1]

        return data

# a = Common_params()
# b = Return_Type()
# print(b.is_Card("asd",a.Button(label='true', action='false', ff="ff"), is_title="title", is_description="asdf"))
# print(a.Button(label="test", action="weblink", weblinkUrl="https://www.naver.com"))
#print(b.is_Carousel("basicCard",3,("http://k.kakaocdn.net/dn/83BvP/bl20duRC1Q1/lj3JUcmrzC53YIjNDkqbWK/i_6piz1p.jpg", "보물상자", "보물상자 안에는 뭐가 있을까"),("http://k.kakaocdn.net/dn/83BvP/bl20duRC1Q1/lj3JUcmrzC53YIjNDkqbWK/i_6piz1p.jpg", "보물상자2", "보물상자 안에는 뭐가 있을까"),("http://k.kakaocdn.net/dn/83BvP/bl20duRC1Q1/lj3JUcmrzC53YIjNDkqbWK/i_6piz1p.jpg", "보물상자3", "보물상자 안에는 뭐가 있을까")))