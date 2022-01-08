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
        data = {}
        param = ['link', 'fixedRatio', 'width', 'height']
        for key in kwargs.keys():
            if key in param:
                data[key] = kwargs[key]

        return data

    return locals()[param_type](**kw)


class ReturnType:  # 리턴 타입별 JSON 형식을 만드는 곳 입니다.
    def __init__(self, reply_json: dict = None):
        self.return_json = init_json()
        if reply_json is not None:
            self.return_json['template']['quickReplies'].append(reply_json)

    def set_text(self, text, is_init=True):  # 텍스트 형식
        if is_init:
            init_json()  # 이전에 들어간 텍스트가 유지될건지 여부
        basic_text = {
            "simpleText": {
                "text": str(text)
            }
        }
        self.return_json["template"]["outputs"].append(basic_text)
        return self.return_json

    def set_card(self, thumb_img, *is_buttons, is_title=None, is_description=None, flag=False):  # 카드 형식
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

            if is_buttons != ():
                if len(is_buttons) > 3:
                    pass

                else:
                    basic_card.update({"buttons": list(is_buttons)})

            if flag:  # flag 가 True이면 Card Json만 반환하지만, False이면 return해야하는 기본 JSON도 포함이 된다.
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

    def set_commerce(self, thumbnail, description, price, currency, is_discount=None, is_discountRate=None,
                     is_discountedPrice=None, profile=None, **kwargs):  # 커머스 반환 형식
        return_json = {
            "commerceCard": {
                "description": None,
                "discount": None,
                "currency": "won",
                "thumbnails": [

                ]
            }
        }

        return return_json

    def set_list(self, title, data, is_Button=None):  # [title, desc, url], 만약 없으면 None #data = list
        init_json()
        order = ['title', 'description', 'link']
        basic_list = {
            "listCard": {
                "header": {
                    "title": title
                },
                "items": []
            }
        }
        for column in data:
            item = {}
            for idx, dat in enumerate(column):
                if dat is not None:
                    if order[idx] == "link":
                        item[order[idx]] = self.common_params.link(dat)

                    else:
                        item[order[idx]] = dat

            basic_list['listCard']['items'].append(item)

            if is_Button is not None:
                basic_list['listCard']['buttons'] = list()
                basic_list['listCard']['buttons'].append(is_Button)

        self.return_json["template"]["outputs"].append(basic_list)
        return self.return_json

    def set_carousel(self, card_type, card_num, *params):  # 케로셀 반환 형식    #(link, Title, description)
        init_json()
        basic_carousel = {
            "carousel": {
                "type": card_type,
                "items": []
            }
        }
        if card_type == "basicCard":
            for param in range(card_num):  # thumb_img, *is_buttons, is_title = None, is_description = None
                basic_carousel['carousel']['items'].append(
                    self.set_card(thumb_img=params[param][0], is_title=params[param][1],
                                  is_description=params[param][2],
                                  flag=True))

        else:
            for param in range(card_num):  # thumb_img, *is_buttons, is_title = None, is_description = None
                basic_carousel['carousel']['items'].append(
                    self.set_card(thumb_img=params[param][0], is_title=params[param][1],
                                  is_description=params[param][2],
                                  flag=True))
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
