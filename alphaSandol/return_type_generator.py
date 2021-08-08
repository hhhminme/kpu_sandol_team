class Return_Type:  # 리턴 타입별 JSON 형식을 만드는 곳 입니다.
    def __init__(self)->None:
        self.return_json:dict = {
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
        self.common_params = Common_Params()

    def init_json(self)->None:
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

    def is_Text(self, text: str, is_init = True)->dict:  #텍스트 형식
        if (is_init == True):
            self.init_json()
        basic_text ={
                        "simpleText": {
                            "text": str(text)
                        }
                    }
        self.return_json["template"]["outputs"].append(basic_text)
        return self.return_json

    def is_Card(self,thumb_img, *is_buttons, is_title: str = None, is_description = None, flag = False)->dict:  #카드 형식
        self.init_json()
        basic_card: dict = {
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

    def is_Image(self, src, text = None)->dict: # 이미지 반환 형식
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

    def is_Carousel(self, card_type, card_num, *params)->dict:  #케로셀 반환 형식    #(link, Title, description)
        self.init_json()
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

    def is_List(self, title: str, data: list, is_Button = None)->dict:     # [title, desc, url], 만약 없으면 None #data = list
        self.init_json()
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
                        item[order[idx]] = self.common_params.Link(dat)

                    else:
                        item[order[idx]] = dat

            basic_list['listCard']['items'].append(item)
            if is_Button != None:
                basic_list['listCard']['buttons'] = list()
                basic_list['listCard']['buttons'].append(is_Button)

        self.return_json["template"]["outputs"].append(basic_list)
        return self.return_json


class Common_Params:

    #kwargs로 들어올 수 있는 값은 DOCS를 참조
    # label = string
    # action = string
    # webLinkUrl = string | action = webLink
    # messageText = string | action = message or block
    # phoneNumber = string | action = phone
    # blockId = string | action = block
    # extra ...
    def Button(self, **kwargs)->dict:
        data = {}
        params = ['label', 'action', 'webLinkUrl', 'messageText', 'phoneNumber', 'blockId']
        for item in kwargs.items():
            if item[0] not in params:
                data.clear()
                data["label"] = "error, Check Parameter"
                data["action"] = "message"
                break
            data[item[0]] = item[1]

        return data

    def Link(self, url)->dict:
        return {
            'web' : url
        }