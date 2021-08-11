from return_type_generator import *

class Constant:

    ####################################################################################################################
    IMOGE: dict = {
        'emotion': {
            'paw': '🐾',
            'smile': '😺',
            'happy': '😸',
            'sad': '😹',
            'love': '😻',
            'confident': '😼',
            'angry': '😾',
            'surprise': '🙀',
            'walk': '🐈',
            'nexpression': '🐱'

        },
        'weather': {
            '흐림': '☁',
            '구름많음': '⛅',
            'hvy_rain': '⛈',
            '비': '☔',
            '약간흐림': '🌤',
            '맑음': '☀',
            'sun_wth_rain': '🌦',
            'thunder': '🌩',
            '바람': '🌪',
            '안개': '🌫'
        }
    }  # 이모지 매핑

    ####################################################################################################################
    BUCKET_NAME: str = 'sandol'

    RESTAURANT_MENU: str = "restaurant_menu.txt"  # 학식이 저장된 파일 이름 (Bucket)
    LOCAL_RESTAURANT_MENU: str = "/tmp/" + RESTAURANT_MENU  # 람다 서버의 해당 디렉토리에 불러옴

    FEEDBACK_FILE: str = "feedback.txt"  # 피드백이 저장된 파일 이름
    LOCAL_FEEDBACK_FILE: str = "/tmp/"+FEEDBACK_FILE  # 람다 서버 tmp 디렉토리에 불러와 실행

    ####################################################################################################################
    SANDOL_ACCESS_ID:dict = {'MANAGER': "d367f2ec55f41b4207156f4b8fce5ce885b05d8c3b238cf8861c55a9012f6f5895",
                             'CONT1': "339b0444bfabbffa0f13508ea7c45b61675b5720234cca8f73cd7421c22de9e546",
                             'CONT2': "04eabc8b965bf5ae6cccb122a18521969cc391162e3fd5f61b85efe8bb12e5e98a",
                             'CONT3': "def99464e022b38389697fe68d54bbba723d1da291094c19bbf5eaace7b059a997"}
    # 산돌팀만 접근할 수 있는 컨텐츠에 인증 수단으로 사용 (현재 아이디의 정확한 위치가 기억이 나지 않아.. KEY를 메니저와, CONTRIBUTOR로 명명함.)
    RESTAURANT_ACCESS_ID: dict = {'미가식당': "32d8a05a91242ffb4c64b5630ec55953121dffd83a121d985e26e06e2c457197e6",
                                  '웰스프레쉬': "d367f2ec55f41b4207156f4b8fce5ce885b05d8c3b238cf8861c55a9012f6f5895",
                                  '푸드라운지': "46f338132e6af63c32c07220c318f0e7c570e8eb6f375c9e8bb59ce33776f27c4c"}
    # 레스토랑에서 접근 허용해주는 ID

    ####################################################################################################################
    SANDOL_CATEGORY_1: str = "https://github.com/hhhminme/kpu_sandol_team/blob/06916e07fe02d36d3384dfe96c8d2dc4cb300aa7/img/card1.png"  # 인기 메뉴
    SANDOL_CATEGORY_2: str = "https://github.com/hhhminme/kpu_sandol_team/blob/06916e07fe02d36d3384dfe96c8d2dc4cb300aa7/img/card2.png"  # 놀거리
    SANDOL_CATEGORY_3: str = "https://github.com/hhhminme/kpu_sandol_team/blob/06916e07fe02d36d3384dfe96c8d2dc4cb300aa7/img/card3.png"  # 교내 정보
    SANDOL_CATEGORY_4: str = "https://github.com/hhhminme/kpu_sandol_team/blob/main/img/card_other.png"  # 기타 기능
    SANDOL_COVID_IMG: str = "https://raw.githubusercontent.com/hhhminme/kpu_sandol_team/main/img/card_covid.png"  # 코로나
    SANDOL_RSTRNT_FOOD_IMG: str = "https://github.com/hhhminme/kpu_sandol_team/blob/main/img/card_food.png"  # 푸드라운지
    SANDOL_RSTRNT_MIGA_IMG: str = "https://github.com/hhhminme/kpu_sandol_team/blob/main/img/card_miga.png"  # 미가식당
    SANDOL_LOGO1: str = "https://github.com/hhhminme/kpu_sandol_team/blob/main/img/logo1.png"  # 산돌이 로고 (필요시 사용)
    SANDOL_PROFILE1: str = "https://github.com/hhhminme/kpu_sandol_team/blob/main/img/logo_profile1.png"  # 산돌이 프로필 (필요시 사용)

    ####################################################################################################################

    def Return_A(self)-> str:
        return "A"