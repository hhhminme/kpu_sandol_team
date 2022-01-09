import json

type_check = lambda x, y: type(x) == y


def init_json():
    return {
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


def ParamOption(param_type, **kw):
    def button(**kwargs):
        data = {}
        params = ['label', 'action', 'webLinkUrl', 'messageText', 'phoneNumber', 'blockId']
        for item in kwargs.items():
            if item[0] not in params:
                data.clear()
                break
            data[item[0]] = item[1]

        return data

    def link(url):
        return {
            'web': url
        }

    def thumbnail(img_url, **kwargs):
        data = {'imageUrl': img_url}
        param = ['link']  # 'fixedRatio', 'width', 'height' 옵션은 제작하지 않음, 추후 필요한경우 제작하여 사용
        print(kwargs.keys())
        for key in kwargs.keys():
            if key in param:
                data[key] = kwargs[key]
        return data

    def profile(nickname, imageUrl=None):
        result = {
            'nickname': nickname,
        }
        if imageUrl is not None:
            result["imageUrl"] = imageUrl

        return result

    def detail_list(**kwargs):
        param = ['title', 'description', 'imageUrl']
        result = {}
        if 'link' in kwargs.keys():
            result['link'] = ParamOption('link', url=kwargs['link'])    # 링크가 있는 경우

        for key in kwargs.keys():   # 나머지 파라미터 적용
            if key in param:
                result[key] = kwargs[key]
        return result

    return locals()[param_type](**kw)


class ReturnType:  # 리턴 타입별 JSON 형식을 만드는 곳 입니다.
    def __init__(self, reply_json: dict = None):
        self.return_json = init_json()
        if reply_json is not None:
            self.return_json['template']['quickReplies'].append(reply_json)

    def set_text(self, text, is_init=True):  # 텍스트 형식
        if is_init:
            self.return_json = init_json()  # 이전에 들어간 텍스트가 유지될건지 여부
        basic_text = {
            "simpleText": {
                "text": str(text)
            }
        }
        self.return_json["template"]["outputs"].append(basic_text)
        return self.return_json

    def set_card(self, thumb_img, *is_buttons, is_title=None, is_description=None, is_carousel=False):  # 카드 형식
        init_json()
        basic_card = {
            "thumbnail": {
                "imageUrl": thumb_img
            }
        }

        try:
            if is_title is not None:
                basic_card["title"] = is_title  # 타이틀 입력

            if is_description is not None:
                basic_card["description"] = is_description  # 설명 입력

            if 0 < len(is_buttons) <= 3:
                basic_card.update({"buttons": list(is_buttons)})

            if is_carousel:  # flag 가 True이면 Card Json만 반환하지만, False이면 return 해야하는 기본 JSON도 포함이 된다.
                return basic_card

            else:
                self.return_json["template"]["outputs"].append({"basicCard": basic_card})  # 위 정보들을 return_json에 입력
                return self.return_json

        except Exception as e:  # 오류 발생시 오류 코드 리턴
            basic_card["description"] = "error :" + str(e)
            self.return_json["template"]["outputs"].append({"basicCard": basic_card})
            return self.return_json

    def set_image(self, src, text=None, is_init=True):  # 이미지 반환 형식
        if is_init:
            init_json()

        basic_image = {
            "simpleImage": {
                "imageUrl": src,
            }
        }

        if text is not None:
            basic_image["simpleImage"]["altText"] = text

        self.return_json["template"]["outputs"].append(basic_image)
        return self.return_json

    def set_commerce(self, thumbnail, description, price, *is_buttons, currency="won", is_discount=None,
                     is_discountRate=None, is_discountedPrice=None, profile=None, is_carousel=False):  # 커머스 반환 형식
        commerce_card = {
            "commerceCard": {
                "description": description,
                "price": price,
                "currecy": currency,
                "thumbnails": [

                ]
            }
        }
        commerce_card["commerceCard"]["thumbnails"].append(thumbnail)

        if 0 < len(is_buttons) <= 3:  # 버튼 관련 파라미터
            commerce_card["commerceCard"]["buttons"] = list(is_buttons)

        if is_discount is not None and \
                is_discountRate is not None and \
                is_discountedPrice is not None:  # 할인 관련 파라미터
            commerce_card["commerceCard"]["discount"] = is_discount
            commerce_card["commerceCard"]["discountRate"] = is_discountRate
            commerce_card["commerceCard"]["discountedPrice"] = is_discountedPrice

        if profile is not None:  # 프로필 관련 파라미터
            commerce_card["commerceCard"]["profile"] = profile

        if is_carousel:     # 리턴 형식 확인
            return commerce_card

        else:
            self.return_json["template"]["outputs"].append(commerce_card)
            return self.return_json

    def set_list(self, header_title, is_button: list, *data, is_carousel=False):
        basic_list = {
            "listCard": {
                "header": {
                    "title": header_title
                },
                "items": []
            }
        }
        if 0 < len(is_button) <= 2:  # 버튼은 최대 2개까지 설정 가능
            basic_list['listCard']['buttons'] = []
            for btn in is_button:
                basic_list['listCard']['buttons'].append(btn)

        for itm in data:    # 값 연결
            basic_list['listCard']['items'].append(itm)

        if is_carousel:     # 반환 형식 설정
            return basic_list

        else:
            self.return_json["template"]["outputs"].append(basic_list)
            return self.return_json

    def set_carousel(self, card_type, *items):  # 케로셀 반환 형식    #(link, Title, description)
        init_json()
        basic_carousel = {
            "carousel": {
                "type": card_type,
                "items": []
            }
        }

        for itm in list(items):
            basic_carousel['carousel']['items'].append(itm)

        self.return_json["template"]["outputs"].append(basic_carousel)
        return self.return_json

    def __str__(self):
        return str(self.return_json)


if __name__ == "__main__":
    Gen = ReturnType()
    buttons = [
        ParamOption('button', label='label1'),
        ParamOption('button', label='label2'),
        ParamOption('button', label='label3'),
        ParamOption('button', label='label4'),
    ]
    print(Gen.set_card("THUMB", *buttons, is_title="테스트!", is_description="산돌이 카드 테스트"))
