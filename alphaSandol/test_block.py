def commerce_test():
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
                        "web": "https://naver.me/FMA7h2K7"
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
                    "webLinkUrl": "https://naver.me/FMA7h2K7 "
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
    Commerce_image = [f'https://raw.githubusercontent.com/hhhminme/kpu_sandol_team/main/commerce_img/commerce_test{x}.png'
                      for x in range(1, 7)]

    random_image = Commerce_image[random.randint(0, 5)]
    return_json['template']['outputs'].append(Commerce_test(random_image))
    return return_json
