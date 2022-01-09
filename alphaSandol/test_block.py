from return_type_generator import (ReturnType, ParamOption)


def text_test():  # set_text 예시
    Gen = ReturnType()
    text_list = ["안녕!", "내 이름은 산돌이!", "만나서 반가워"]
    for txt in text_list:
        Gen.set_text(txt, is_init=True)
    return Gen


def commerce_test():  # set_commerce 예시
    import random
    # 1~5 산돌 분식, 6 산돌 카페
    commerce_image = [
        f'https://raw.githubusercontent.com/hhhminme/kpu_sandol_team/main/commerce_img/commerce_test{x}.png'
        for x in range(1, 7)]
    choice = random.choice(commerce_image)

    Gen = ReturnType()

    return Gen.set_commerce(
        ParamOption('thumbnail', img_url=choice, link=ParamOption("link", url="https://naver.me/FMA7h2K7")),
        # thumbnail
        "산돌분식을 방문하여 해당 광고를 보여주시면 해당 메뉴의 할인이 적용됩니다.",  # description
        4000,  # price
        ParamOption('button', label="네이버 플레이스 연결", action="webLink", webLinkUrl="https://naver.me/FMA7h2K7"),
        ParamOption('button', label="네이버 플레이스 연결", action="webLink", webLinkUrl="https://naver.me/FMA7h2K7"),
        ParamOption('button', label="전화하기", action="phone", webLinkUrl="010-4183-2998"),
        ParamOption('button', label="공유하기", action="share"),  # buttons
        is_discount=500,  # discount
        profile=ParamOption('profile', imageUrl=choice, nickname="산돌분식"),  # profile
    )


def card_test():  # set_card
    Gen = ReturnType()
    THUMBNAIL = r"https://github.com/teamSANDOL/kpu_sandol_team/blob/main/return_type_img/Basic%20Card%20Test.JPG?raw=true"
    buttons = [
        ParamOption('button', label='label1'),
        ParamOption('button', label='label2'),
        ParamOption('button', label='label3'),
    ]
    return Gen.set_card(THUMBNAIL, *buttons, is_title="테스트!", is_description="산돌이 카드 테스트")


def image_test():  # set_image
    Gen = ReturnType()
    URL = r"https://github.com/hhhminme/kpu_sandol_team/blob/main/img/logo1.png?raw=true"
    return Gen.set_image(URL, text="산돌이 로고 이미지입니다!")


def carousel_test():
    Gen = ReturnType()
    return Gen.set_carousel("basicCard",
                            Gen.set_card("THUMB1", "THUMB_IMG",
                                         ParamOption('button', label="button1", action="messageText"),
                                         ParamOption('button', label="button2", action="messageText"),
                                         ParamOption('button', label="button3", action="messageText"),
                                         is_carousel=True
                                         ),
                            Gen.set_card("THUMB2", "THUMB_IMG",
                                         ParamOption('button', label="button1", action="messageText"),
                                         ParamOption('button', label="button2", action="messageText"),
                                         ParamOption('button', label="button3", action="messageText"),
                                         is_carousel=True
                                         ),
                            Gen.set_card("THUMB3", "THUMB_IMG",
                                         ParamOption('button', label="button1", action="messageText"),
                                         ParamOption('button', label="button2", action="messageText"),
                                         ParamOption('button', label="button3", action="messageText"),
                                         is_carousel=True
                                         )
                            )


def list_test():
    Gen = ReturnType()
    buttons = [
        ParamOption('button', label='button1', webLinkUrl='https://www.naver.com')
    ]
    return Gen.set_list("Header Title",
                        buttons,
                        ParamOption('detail_list', title='item title1', description='item description1',
                                    imageUrl='test.jpg'),
                        ParamOption('detail_list', title='item title2', description='item description2',
                                    imageUrl='test.jpg'),
                        ParamOption('detail_list', title='item title3', description='item description3',
                                    imageUrl='test.jpg'),
                        ParamOption('detail_list', title='item title4', description='item description4',
                                    imageUrl='test.jpg'),
                        ParamOption('detail_list', title='item title5', description='item description5',
                                    imageUrl='test.jpg'),
                        )


if __name__ == "__main__":
    import pprint

    print(list_test())
