import boto3
import alphaSandol as settings
import datetime

settings.DEBUG = True


class AboutMeal:  # 학식 관련 클래스
    def __init__(self):
        self.DATE = 0
        self.LUNCH = 1
        self.DINNER = 2

        self.S3 = boto3.resource('s3')
        self.S3_client = boto3.client('s3')
        self.bucket = self.S3.Bucket(settings.BUCKET_NAME)
        self.data = ""
        self.URL_MENU = "https://ibook.kpu.ac.kr/Viewer/menu01"

    def read_meal(self, uid) -> dict:  # 학식 불러오기
        restaurant_position = {"messageText": "운영시간",
                               "action": "message",
                               "label": "운영시간 및 위치"
                               }  # quick reply 형식
        MEAL_GEN = settings.return_type(reply_json=restaurant_position)  # 따로 리턴타입을 불러옴, 이유는 발화안에 여러 응답을 줘야하기때문
        # 이전과 같은 id의 인스턴스로 사용하면 다른 발화에도 영향
        if not settings.DEBUG:  # 디버그 모드가 아닌 경우
            try:
                self.bucket.download_file(settings.RESTAURANT_MENU, settings.LOCAL_RESTAURANT_MENU)

            except Exception as e:
                return settings.GEN.set_text(
                    f"[File-Open-Error #131] 저장소에서 파일을 가져오는데 실패했습니다.{settings.IMOGE('emotion', 'sad')}\n{e}")
            # 버킷을 로컬 임시 폴더에 다운로드

        rst_name = list(settings.RESTAURANT_ACCESS_ID.values())  # 식당id만 뽑아낸 리스트
        if uid not in rst_name:
            try:
                weekday = ['월', '화', '수', '목', '금', '토', '일']
                file_dir = lambda \
                    is_debug: settings.LOCAL_RESTAURANT_MENU if is_debug is False else "../test_stored_data/restaurant_menu.txt"

                with open(file_dir(settings.DEBUG), "r", encoding='UTF-8') as f:
                    data = f.readlines()
                    ret = '[교외식당 메뉴입니다!]\n'
                    for restaurant in range(0, len(data) - 4, 2):  # 파일에서 식당 구분이 2칸 간격으로 되어있음 교외식당
                        menu_list = data[restaurant + 1].replace("\'", '').split(", ")
                        last_update_date = datetime.date.fromisoformat(menu_list[0])
                        form = data[restaurant].replace("\n", '').replace("🐾", settings.IMOGE('emotion', 'walk'))

                        ret += f"{form}[{str(last_update_date)} {weekday[last_update_date.weekday()]}요일]\n" \
                               f"{settings.IMOGE('emotion', 'paw')} 중식 : {menu_list[self.LUNCH].replace(' ', ', ')}\n" \
                               f"{settings.IMOGE('emotion', 'paw')} 석식 : {menu_list[self.DINNER].replace(' ', ', ')}\n"
                    ret = ret[:-2]
                    MEAL_GEN.set_text(ret, is_init=False)  # 교외식당 저장
                    ret = '[교내식당 메뉴입니다!]\n'
                    for school_restaurant in range(len(data) - 4, len(data) - 2, 2):
                        menu_list = data[school_restaurant + 1].replace("\'", '').split(", ")
                        last_update_date = datetime.date.fromisoformat(menu_list[0])
                        form = data[school_restaurant].replace("\n", '').replace("🐾",
                                                                                 settings.IMOGE('emotion', 'walk'))

                        ret += f"{form}[{str(last_update_date)} {weekday[last_update_date.weekday()]}요일]\n포장메뉴도 있어요\n" \
                               f"{settings.IMOGE('emotion', 'paw')} 중식 : {menu_list[self.LUNCH]}\n" \
                               f"{settings.IMOGE('emotion', 'paw')} 석식 : {menu_list[self.DINNER]}\n"
                    ret += "🐾웰스프레쉬(E동 교직원식당) [URL 참조]\nhttps://ibook.kpu.ac.kr/Viewer/menu01"

                return_string = MEAL_GEN.set_text(ret, is_init=False)  # 교외식당 저장
                return return_string

            except Exception as e:
                return settings.GEN.set_text(
                    "[File-Open-Error #132] 파일을 여는 중 오류가 발생했어요.." + settings.IMOGE('emotion', 'sad') + str(e))

        else:
            selected_restaurant = rst_name.index(uid) * 2  # 식당 이름 포인터
            try:
                weekday = ['월', '화', '수', '목', '금', '토', '일']
                file_dir = lambda \
                    is_debug: settings.LOCAL_RESTAURANT_MENU if is_debug is False else "../test_stored_data/restaurant_menu.txt"
                with open(file_dir(settings.DEBUG), "r", encoding='UTF-8') as f:
                    data = f.readlines()

                    menu_list = data[selected_restaurant + 1].replace("\'", '').split(", ")
                    last_update_date = datetime.date.fromisoformat(menu_list[0])
                    form = data[selected_restaurant].replace("\n", '').replace("🐾", settings.IMOGE('emotion', 'walk'))

                    if uid == settings.RESTAURANT_ACCESS_ID['푸드라운지']:
                        ret = f"{form}[{str(last_update_date)} {weekday[last_update_date.weekday()]}요일]\n포장메뉴도 있어요\n" \
                              f"{settings.IMOGE('emotion', 'paw')} 중식 : {menu_list[self.LUNCH].replace(' ', ', ')}\n" \
                              f"{settings.IMOGE('emotion', 'paw')} 석식 : {menu_list[self.DINNER].replace(' ', ', ')}\n"
                    else:
                        ret = f"{form}[{str(last_update_date)} {weekday[last_update_date.weekday()]}요일]\n" \
                              f"{settings.IMOGE('emotion', 'paw')} 중식 : {menu_list[self.LUNCH].replace(' ', ', ')}\n" \
                              f"{settings.IMOGE('emotion', 'paw')} 석식 : {menu_list[self.DINNER].replace(' ', ', ')}\n"
                    return_string = settings.GEN.set_text(ret)

                return return_string

            except Exception as e:
                return settings.GEN.set_text(
                    "[File-Open-Error #132] 파일을 여는 중 오류가 발생했어요.." + settings.IMOGE('emotion', 'sad') + str(e))

    def upload_meal(self, store_name, lunch_list: str, dinner_list: str, input_date, owner_id) -> dict:  # 학식 업로드
        if (owner_id != settings.RESTAURANT_ACCESS_ID[store_name]) and owner_id not in list(
                settings.SANDOL_ACCESS_ID.values()):
            return settings.GEN.set_text(
                f"[Permission-Error #121-1] 권한이 없습니다{owner_id}{settings.IMOGE('emotion', 'angry')}")
        # 권한 확인

        if store_name not in settings.RESTAURANT_ACCESS_ID.keys():
            return settings.GEN.set_text(f"[Not-Found-Error #121-2] 해당하는 식당이 없습니다.{settings.IMOGE('emotion', 'sad')}")
        # 식당 존재 여부 확인

        if not settings.DEBUG:
            try:
                self.S3.meta.client.download_file(settings.BUCKET_NAME, settings.RESTAURANT_MENU,
                                                  settings.LOCAL_RESTAURANT_MENU)

            except Exception as e:
                return settings.GEN.set_text(
                    f"[File-Open-Error #122] 저장소에서 파일을 찾을 수 없습니다.{settings.IMOGE('emotion', 'sad')}\n{e}")

        file_dir = lambda \
            is_debug: settings.LOCAL_RESTAURANT_MENU if is_debug is False else "../test_stored_data/restaurant_menu.txt"
        with open(file_dir(settings.DEBUG), "r", encoding='UTF-8') as f:
            try:
                data = f.readlines()
                menu_info = data[data.index("🐾" + store_name + "\n") + 1].replace('\'', '').replace("\n", "").split(
                    ", ")
                menu_info[self.DATE] = input_date

                menu_info[self.LUNCH] = lunch_list
                menu_info[self.DINNER] = dinner_list

                final_string = str(menu_info)[1:-1]

                data[data.index("🐾" + store_name + "\n") + 1] = final_string + "\n"  # 최종 문자열
                with open(file_dir(settings.DEBUG), "w", encoding='UTF-8') as rf:
                    rf.writelines(data)

            except Exception as e:
                return settings.GEN.set_text(
                    f"[File-Open-Error #123]파일을 수정하는 중 오류가 발생했습니다.{settings.IMOGE('emotion', 'sad')}\n{e}")

            if not settings.DEBUG:
                try:
                    s3 = boto3.client('s3')  # 이 부분 해당 버킷 생성 후 적절히 수정 예정
                    s3.upload_file(settings.LOCAL_RESTAURANT_MENU, 'sandol', settings.RESTAURANT_MENU)

                except Exception as e:
                    return settings.GEN.set_text(
                        f"[File-Open-Error #124]파일을 저장소에 업로드하는 중 오류가 발생했습니다.{settings.IMOGE('emotion', 'sad')}\n{e}")

        return settings.GEN.set_text(f"네! 학생들에게 잘 전달할게요! 감사합니다!{settings.IMOGE('emotion', 'walk')}")

    def reset_meal(self, bot_id, date) -> dict:  # 학식 초기화
        if bot_id not in list(settings.SANDOL_ACCESS_ID.values()):
            return settings.GEN.set_text(f"[Permission-Error #141] 권한이 없습니다{settings.IMOGE('emotion', 'angry')}")

        if not settings.DEBUG:
            try:
                self.S3.meta.client.download_file(settings.BUCKET_NAME, settings.RESTAURANT_MENU,
                                                  settings.LOCAL_RESTAURANT_MENU)

            except Exception as e:
                return settings.GEN.set_text(
                    f"[File-Open-Error #122] 저장소에서 파일을 찾을 수 없습니다.{settings.IMOGE('emotion', 'sad')}\n{e}")

        try:
            file_dir = lambda \
                is_debug: settings.LOCAL_RESTAURANT_MENU if is_debug is False else "../test_stored_data/restaurant_menu.txt"
            print(file_dir(settings.DEBUG))
            with open(file_dir(settings.DEBUG), "w", encoding='UTF-8') as f:
                rest_name = [f"{settings.IMOGE('emotion', 'paw')}미가식당\n",
                             f"{settings.IMOGE('emotion', 'paw')}세미콘식당\n",
                             f"{settings.IMOGE('emotion', 'paw')}푸드라운지\n",
                             f"{settings.IMOGE('emotion', 'paw')}웰스프레쉬\n"
                             ]

                return_string = ''
                for i in range(len(rest_name)):
                    return_string += rest_name[i] + "\'" + date + "\', \'업데이트되지않았습니다\', \'업데이트되지않았습니다\'\n"
                # 초기화 작업

                f.writelines(return_string)

        except Exception as e:
            return settings.GEN.set_text(
                f"[File-Open-Error #143]파일을 수정하는 중 오류가 발생했습니다.{settings.IMOGE('emotion', 'sad')}\n{e}")

        if not settings.DEBUG:
            try:
                s3 = boto3.client('s3')  # 이 부분 해당 버킷 생성 후 적절히 수정 예정
                s3.upload_file(settings.LOCAL_RESTAURANT_MENU, 'sandol', settings.RESTAURANT_MENU)

            except Exception as e:
                return settings.GEN.set_text(
                    f"[File-Open-Error #124]파일을 저장소에 업로드하는 중 오류가 발생했습니다.{settings.IMOGE('emotion', 'sad')}\n{e}")

        return settings.GEN.set_text(f"파일을 정상적으로 초기화했습니다")


# 식당 운영시간 불러오기
def time_meal():
    MEAL_GEN = settings.return_type()
    MEAL_GEN.set_image(settings.SANDOL_RSTRNT_MAP, is_init=False)  # 식당 지도

    time_meal_string = f"교외식당 운영시간입니다! \n" \
                       f"{settings.IMOGE('emotion', 'walk')}미가식당  \n" \
                       f"{settings.IMOGE('emotion', 'paw')}운영시간 : 08:30 ~ 19:30  \n" \
                       f"{settings.IMOGE('emotion', 'paw')}운영시간동안 항시 식사 가능합니다.  \n\n" \
                       f"{settings.IMOGE('emotion', 'walk')}세미콘 식당  \n" \
                       f"{settings.IMOGE('emotion', 'paw')}중식 : 11:30 ~ 1:30\n" \
                       f"{settings.IMOGE('emotion', 'paw')}석식 : 5:00 ~ 6:30\n"
    MEAL_GEN.set_text(time_meal_string, is_init=False)

    time_meal_string = f"교내식당 운영시간입니다! \n" \
                       f"{settings.IMOGE('emotion', 'walk')}웰스 프레쉬(E동 교직원식당)  \n" \
                       f"{settings.IMOGE('emotion', 'paw')}중식 : 11:30 ~ 13:30 \n" \
                       f"{settings.IMOGE('emotion', 'paw')}석식 : 영업하지 않습니다. \n\n" \
                       f"{settings.IMOGE('emotion', 'walk')}푸드라운지 \n" \
                       f"{settings.IMOGE('emotion', 'paw')}천원의 아침 : 8시 30분 ~ 10시 \n" \
                       f"{settings.IMOGE('emotion', 'paw')}운영시간 : 11:00 ~ 20:00 \n" \
                       f"{settings.IMOGE('emotion', 'paw')}토,일,공유일 영업하지 않습니다. \n"

    return MEAL_GEN.set_text(time_meal_string, is_init=False)


# 식당 계좌이체 결제
def payment_meal():
    btn_list = [{
        "label": "세미콘 식당",
        "action": "webLink",
        "webLinkUrl": "https://qr.kakaopay.com/2810060111751110120069009c404611"
    },
        {
            "label": "민이 식당",
            "action": "webLink",
            "webLinkUrl": "https://qr.kakaopay.com/2810060110000075262686359c406394"
        }]
    title = "hello"
    dsc = "dsc"
    params = ['label', 'action', 'webLinkUrl', 'messageText', 'phoneNumber', 'blockId']
    return settings.GEN.set_card(settings.SANDOL_LOGO1, settings.GEN_OPTION.Button(label="세미콘 식당", action="webLink",
                                                                                   webLinkUrl="https://qr.kakaopay.com/2810060111751110120069009c404611"),
                                 is_title=title, is_description=dsc, flag=False)


if __name__ == "__main__":
    # print(AboutMeal().read_meal(uid="d367f2ec55f41b4207156f4b8fce5ce885b05d8c3b238cf8861c55a9012f6f5895"))  # read meal (산돌팀 (학생)) 기준
    # print(AboutMeal().read_meal(uid="32d8a05a91242ffb4c64b5630ec55953121dffd83a121d985e26e06e2c457197e6"))  # read meal (미가식당 (업주)) 기준
    # print(AboutMeal().reset_meal(bot_id="d367f2ec55f41b4207156f4b8fce5ce885b05d8c3b238cf8861c55a9012f6f5895", date="2001-09-03"))  # reset meal 테스트 데이터 형식
    # print(AboutMeal().upload_meal(store_name="미가식당", lunch_list="ㅁ ㅁ ㅁ ㅁ", dinner_list="ㄹ ㄹ ㄹ ㄹ", input_date="2001-09-03",owner_id="d367f2ec55f41b4207156f4b8fce5ce885b05d8c3b238cf8861c55a9012f6f5895"))  # read meal (미가식당 (업주)) 기준
    # print(time_meal())  # time meal
    print(payment_meal())
