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
from return_type_generator import return_type
from return_type_generator import common_params
import sandol_constant as Constant

GEN = return_type()  # kakao-i type json generator
GEN_OPTION = common_params()  # generator optional param


class AboutMeal:  # 학식 관련 클래스
    def __init__(self):
        self.DATE = 0
        self.LUNCH = 1
        self.DINNER = 2

        self.S3 = boto3.resource('s3')
        self.S3_client = boto3.client('s3')
        self.bucket = self.S3.Bucket(Constant.BUCKET_NAME)
        self.data = ""
        self.URL_MENU = "https://ibook.kpu.ac.kr/Viewer/menu01"

    def read_meal(self, uid) -> dict:     # 학식 불러오기
        MEAL_GEN = return_type()    # 따로 리턴타입을 불러옴, 이유는 발화안에 여러 응답을 줘야하기때문
                                    # 이전과 같은 id의 인스턴스로 사용하면 다른 발화에도 영향
        try:
            self.bucket.download_file(Constant.RESTAURANT_MENU, Constant.LOCAL_RESTAURANT_MENU)

        except Exception as e:
            return GEN.set_text(
                f"[File-Open-Error #131] 저장소에서 파일을 가져오는데 실패했습니다.{Constant.IMOGE['emotion']['sad']}\n{e}")
        # 버킷을 로컬 임시 폴더에 다운로드

        rst_name = list(Constant.RESTAURANT_ACCESS_ID.values())     # 식당이름만 뽑아낸 리스트
        if uid not in rst_name:
            try:
                weekday = ['월', '화', '수', '목', '금', '토', '일']
                with open(Constant.LOCAL_RESTAURANT_MENU, "r", encoding='UTF-8') as f:
                    data = f.readlines()
                    for restaurant in range(0, len(data), 2):  # 파일에서 식당 구분이 2칸 간격으로 되어있음
                        menu_list = data[restaurant + 1].replace("\'", '').split(", ")
                        last_update_date = datetime.date.fromisoformat(menu_list[0])
                        if restaurant == 2:  # 웰스프레쉬의 경우 건너뛴다 (링크로 대체)
                            continue

                        form = data[restaurant].replace("\n", '').replace("🐾", Constant.IMOGE['emotion']['walk'])
                        ret = f"{form}[{str(last_update_date)} {weekday[last_update_date.weekday()]}요일]\n" \
                              f"{Constant.IMOGE['emotion']['paw']} 중식 : {menu_list[self.LUNCH]}\n" \
                              f"{Constant.IMOGE['emotion']['paw']} 석식 : {menu_list[self.DINNER]}"
                        MEAL_GEN.set_text(ret, is_init=False)

                return_string = MEAL_GEN.set_text(f"{Constant.IMOGE['emotion']['paw']}웰스프레쉬 [URL 참조]\n{self.URL_MENU}",
                                                  is_init=False)
                return return_string

            except Exception as e:
                return GEN.set_text(
                    "[File-Open-Error #132] 파일을 여는 중 오류가 발생했어요.." + Constant.IMOGE['emotion']['sad'] + str(e))

        else:
            selected_restaurant = rst_name.index(uid) * 2  # 식당 이름
            try:
                weekday = ['월', '화', '수', '목', '금', '토', '일']
                with open(Constant.LOCAL_RESTAURANT_MENU, "r", encoding='UTF-8') as f:
                    data = f.readlines()

                    menu_list = data[selected_restaurant + 1].replace("\'", '').split(", ")
                    last_update_date = datetime.date.fromisoformat(menu_list[0])
                    form = data[selected_restaurant].replace("\n", '').replace("🐾", Constant.IMOGE['emotion']['walk'])
                    ret = f"{form}[{str(last_update_date)} {weekday[last_update_date.weekday()]}요일]\n" \
                          f"{Constant.IMOGE['emotion']['paw']} 중식 : {menu_list[self.LUNCH]}\n" \
                          f"{Constant.IMOGE['emotion']['paw']} 석식 : {menu_list[self.DINNER]}"
                    return_string = GEN.set_text(ret)

                return return_string

            except Exception as e:
                return GEN.set_text(
                    "[File-Open-Error #132] 파일을 여는 중 오류가 발생했어요.." + Constant.IMOGE['emotion']['sad'] + str(e))

    def upload_meal(self, store_name, lunch_list: list, dinner_list: list, input_date, owner_id) -> dict:  # 학식 업로드
        if (owner_id != Constant.RESTAURANT_ACCESS_ID[store_name]) and owner_id not in list(Constant.SANDOL_ACCESS_ID.values()):
            return GEN.set_text(f"[Permission-Error #121-1] 권한이 없습니다{owner_id}{Constant.IMOGE['emotion']['angry']}")
        # 권한 확인

        if store_name not in Constant.RESTAURANT_ACCESS_ID.keys():
            return GEN.set_text(f"[Not-Found-Error #121-2] 해당하는 식당이 없습니다.{Constant.IMOGE['emotion']['sad']}")
        # 식당 존재 여부 확인

        try:
            self.S3.meta.client.download_file(Constant.BUCKET_NAME, Constant.RESTAURANT_MENU,
                                              Constant.LOCAL_RESTAURANT_MENU)

        except Exception as e:
            return GEN.set_text(f"[File-Open-Error #122] 저장소에서 파일을 찾을 수 없습니다.{Constant.IMOGE['emotion']['sad']}\n{e}")

        with open(Constant.LOCAL_RESTAURANT_MENU, "r", encoding="UTF-8") as f:
            try:
                data = f.readlines()
                menu_info = data[data.index("🐾" + store_name + "\n") + 1].replace('\'', '').replace("\n", "").split(
                    ", ")
                menu_info[self.DATE] = input_date

                menu_info[self.LUNCH] = lunch_list.replace(", ", ",").replace(" ", ",")
                menu_info[self.DINNER] = dinner_list.replace(",", "").replace(" ", ",")

                menu_info[self.LUNCH] = lunch_list.replace(" ", ",")
                menu_info[self.DINNER] = dinner_list.replace(" ", ",")

                menu_info[self.LUNCH] = lunch_list.replace(" ", ",")
                menu_info[self.DINNER] = dinner_list.replace(" ", ",")

                data[data.index("🐾" + store_name + "\n") + 1] = str(menu_info)[1:-1] + "\n"  # 최종 문자열
                with open(Constant.LOCAL_RESTAURANT_MENU, "w", encoding='UTF-8') as rf:
                    rf.writelines(data)

            except Exception as e:
                return GEN.set_text(
                    f"[File-Open-Error #123]파일을 수정하는 중 오류가 발생했습니다.{Constant.IMOGE['emotion']['sad']}\n{e}")

            try:
                s3 = boto3.client('s3')  # 이 부분 해당 버킷 생성 후 적절히 수정 예정
                s3.upload_file(Constant.LOCAL_RESTAURANT_MENU, 'sandol', Constant.RESTAURANT_MENU)

            except Exception as e:
                return GEN.set_text(
                    f"[File-Open-Error #124]파일을 저장소에 업로드하는 중 오류가 발생했습니다.{Constant.IMOGE['emotion']['sad']}\n{e}")

        return GEN.set_text(f"네! 학생들에게 잘 전달할게요! 감사합니다!{Constant.IMOGE['emotion']['walk']}")

    def reset_meal(self, bot_id, date) -> dict:  # 학식 초기화
        if bot_id not in list(Constant.SANDOL_ACCESS_ID.values()):
            return GEN.set_text(f"[Permission-Error #141] 권한이 없습니다{Constant.IMOGE['emotion']['angry']}")

        try:
            self.S3.meta.client.download_file(Constant.BUCKET_NAME, Constant.RESTAURANT_MENU,
                                              Constant.LOCAL_RESTAURANT_MENU)

        except Exception as e:
            return GEN.set_text(f"[File-Open-Error #122] 저장소에서 파일을 찾을 수 없습니다.{Constant.IMOGE['emotion']['sad']}\n{e}")

        try:
            with open(Constant.LOCAL_RESTAURANT_MENU, "w", encoding="UTF-8") as f:
                rest_name = [f"{Constant.IMOGE['emotion']['paw']}미가식당\n",
                             f"{Constant.IMOGE['emotion']['paw']}웰스프레쉬\n",
                             f"{Constant.IMOGE['emotion']['paw']}세미콘식당\n"]

                return_string = ''
                for i in range(len(rest_name)):
                    return_string += rest_name[i] + "\'" + date + "\', \'업데이트되지않았습니다\', \'업데이트되지않았습니다\'\n"
                # 초기화 작업

                f.writelines(return_string)

        except Exception as e:
            return GEN.set_text(f"[File-Open-Error #143]파일을 수정하는 중 오류가 발생했습니다.{Constant.IMOGE['emotion']['sad']}\n{e}")

        try:
            s3 = boto3.client('s3')  # 이 부분 해당 버킷 생성 후 적절히 수정 예정
            s3.upload_file(Constant.LOCAL_RESTAURANT_MENU, 'sandol', Constant.RESTAURANT_MENU)

        except Exception as e:
            return GEN.set_text(
                f"[File-Open-Error #124]파일을 저장소에 업로드하는 중 오류가 발생했습니다.{Constant.IMOGE['emotion']['sad']}\n{e}")

        return GEN.set_text(f"파일을 정상적으로 초기화했습니다")


class LastTraffic:  # 교통 관련 클래스
    def __init__(self):

        self.SUBWAY_URL = ["https://map.naver.com/v5/api/transit/subway/stations/455/schedule?lang=ko&stationID=455",
                           "https://map.naver.com/v5/api/transit/subway/stations/11120/schedule?lang=ko&stationID=11120"]

    def real_time_traffic(self):
        context = ''
        header = [f"{Constant.IMOGE['emotion']['walk']}4호선 막차시간입니다\n",
                  f"\n{Constant.IMOGE['emotion']['walk']}수인선 막차시간입니다\n"]
        try:
            for iteration in range(len(self.SUBWAY_URL)):
                context += ''.join(header[iteration])
                html = requests.get(self.SUBWAY_URL[iteration])
                soup = BeautifulSoup(html.text, 'html.parser')

                last_arrival_weekday = json.loads(soup.text)['weekdaySchedule']  # 평일 막차
                last_arrival_weekend = json.loads(soup.text)['sundaySchedule']  # 주말 막차
                if iteration == 0:
                    weekday_last = lambda sign: [last_arrival_weekday[sign][101 + i] for i in
                                                 range(len(last_arrival_weekday[sign]) - 101)][::-1]
                    weekend_last = lambda sign: [last_arrival_weekend[sign][85 + i] for i in
                                                 range(len(last_arrival_weekend[sign]) - 85)][::-1]

                else:
                    weekday_last = lambda sign: [last_arrival_weekday[sign][i] for i in
                                                 range(len(last_arrival_weekday[sign]))][::-1]
                    weekend_last = lambda sign: [last_arrival_weekend[sign][i] for i in
                                                 range(len(last_arrival_weekend[sign]))][::-1]
                # usage : weekend_last('up')
                # 마지막에 있는 열차 10개 정도를 가지고 와서 각 막차 시간 비교
                # 모두 불러오지 않는 이유는 속도 때문
                station = [i['headsign'] for i in weekday_last('up')]  # headsign이 가장 처음으로 나오는 경우의 인덱스를 반환하기 위한 리스트
                station_weekend = [i['headsign'] for i in
                                   weekend_last('up')]  # headsign이 가장 처음으로 나오는 경우의 인덱스를 반환하기 위한 리스트
                # 상행선에서의 막차별 역을 저장하는 리스트 (역 중복 가능)

                station2 = [i['headsign'] for i in weekday_last('down')]  # headsign이 가장 처음으로 나오는 경우의 인덱스를 반환하기 위한 리스트
                station_weekend2 = [i['headsign'] for i in
                                    weekend_last('down')]  # headsign이 가장 처음으로 나오는 경우의 인덱스를 반환하기 위한 리스트
                # 상행선에서의 막차별 역을 저장하는 리스트 (역 중복 가능)

                find_weekday = station.index
                find_weekend = station_weekend.index

                find_weekday2 = station2.index
                find_weekend2 = station_weekend2.index

                find_arrival_time_up = lambda a: weekday_last('up')[a]["departureTime"][:-3]  # 평일 상행선
                find_arrival_time_down = lambda a: weekday_last('down')[a]["departureTime"][:-3]  # 평일 하행선

                find_arrival_time_up2 = lambda a: weekend_last('up')[a]["departureTime"][:-3]  # 주말 상행선
                find_arrival_time_down2 = lambda a: weekend_last('down')[a]["departureTime"][:-3]  # 주말 하행선

                station_name_up: list = [["당고개", "안산", "노원", "금정", "한성대입구", "사당"], ["왕십리", "죽전", "고색"]]
                station_name_down: list = [["오이도"], ["오이도", "인천"]]

                for arv in (station_name_up[iteration]):
                    context += ''.join(f"{arv} - ")
                    try:
                        context += ''.join(f"(평일) {find_arrival_time_up(find_weekday(arv))}")
                    except Exception as e:
                        pass

                    try:
                        context += "".join(f"(휴일) {find_arrival_time_up2(find_weekend(arv))}\n")  # 휴일 시간이 있으면 시간 추가
                    except Exception as e:
                        context += "".join("\n")  # 휴일 시간 없으면 개행문자 넣고 pass

                for arv in (station_name_down[iteration]):
                    context += ''.join(f"{arv} - ")
                    try:
                        context += ''.join(f"(평일) {find_arrival_time_down(find_weekday2(arv))}")
                    except Exception:
                        pass

                    try:
                        context += "".join(f"(휴일) {find_arrival_time_down2(find_weekend2(arv))}\n")  # 휴일 시간이 있으면 시간 추가
                    except Exception:
                        context += "".join("\n")  # 휴일 시간 없으면 개행문자 넣고 pass
        except Exception as e:
            return GEN.set_text(str(e))
        return GEN.set_text(str(context[:-1]))


class Feedback:
    def __init__(self):
        self.S3 = boto3.resource('s3')
        self.S3_client = boto3.client('s3')
        self.bucket = self.S3.Bucket(Constant.BUCKET_NAME)
        self.data = ""

    def upload_feedback(self, data):
        self.data = f"[{str(datetime.datetime.today())}] : {data}\n"

        try:
            self.bucket.download_file(Constant.FEEDBACK_FILE, Constant.LOCAL_FEEDBACK_FILE)

        except Exception as e:
            return GEN.set_text(
                f"[File-Open-Error #101] 서버에서 피드백 파일을 불러오는 중 오류가 발생했어요{Constant.IMOGE['emotion']['sad']}\n{e}")

        try:
            with open(Constant.LOCAL_FEEDBACK_FILE, "a", encoding="UTF-8") as f:
                f.writelines(self.data)

        except Exception as e:
            return GEN.set_text(f"[File-Open-Error #102] 파일을 저장 중 오류가 발생했습니다{Constant.IMOGE['emotion']['sad']}\n{e}")

        try:
            self.S3_client.upload_file(Constant.LOCAL_FEEDBACK_FILE, Constant.BUCKET_NAME, Constant.FEEDBACK_FILE)

        except Exception as e:
            return GEN.set_text(
                f"[File-Open-Error #103] 파일을 서버에 업로드 하는 중 오류가 발생했습니다{Constant.IMOGE['emotion']['sad']}\n{e}")

        return GEN.set_text(f"피드백 주셔서 감사해요! 빠른 시일내에 검토 후 적용해볼게요!{Constant.IMOGE['emotion']['love']}")


    def read_feedback(self, id):
        if id not in (Constant.SANDOL_ACCESS_ID.values()):
            return GEN.set_text("권한이 없습니다")
        try:
            self.bucket.download_file(Constant.FEEDBACK_FILE, Constant.LOCAL_FEEDBACK_FILE)

        except Exception as e:
            GEN.set_text(f"[File-Open-Error #111] 서버에서 피드백 파일을 불러오는 중 오류가 발생했어요\n{e}")

        try:
            with open(Constant.LOCAL_FEEDBACK_FILE, 'r', encoding='UTF-8')as f:
                txt = ''.join(f.readlines())

        except Exception as e:
            return GEN.set_text(f"[File-Open-Error #112] 파일을 읽는 중 오류가 발생했습니다\n{e}")

        return GEN.set_text(txt)

    def delete_feedback(self, id):
        if id not in (Constant.SANDOL_ACCESS_ID.values()):
            return GEN.set_text("권한이 없습니다")

        basic_text = "#feedbacks\n"
        try:
            self.bucket.download_file(Constant.FEEDBACK_FILE, Constant.LOCAL_FEEDBACK_FILE)
        except Exception as e:
            return GEN.set_text(f"[File-Open-Error #113] 서버에서 피드백 파일을 불러오는 중 오류가 발생했어요\n{e}")

        try:
            with open(Constant.LOCAL_FEEDBACK_FILE, 'w', encoding="UTF-8") as f:
                f.writelines(basic_text)

        except Exception as e:
            return GEN.set_text(f"[File-Open-Error #114] 파일 데이터를 삭제 중 오류가 발생했습니다{e}")

        try:
            s3 = boto3.client('s3')
            s3.upload_file(Constant.LOCAL_FEEDBACK_FILE, Constant.BUCKET_NAME, Constant.FEEDBACK_FILE)

        except Exception as e:
            return GEN.set_text(f"[File-Open-Error #115] 파일을 서버에 업로드 하는 중 오류가 발생했습니다{e}")

        return GEN.set_text("성공적으로 파일 내용을 삭제했습니다")


class Covid:
    def __init__(self):
        self.return_string = ""

    def today_covid(self) -> dict:
        try:
            url = 'https://m.search.naver.com/p/csearch/content/nqapirender.nhn?where=nexearch&pkid=9005&key=diffV2API'
            html = requests.get(url).text
            data = json.loads(html)
            result = f"{data['result']['list'][-1]['date']}일까지 코로나 발생현황이에요 {Constant.IMOGE['emotion']['walk']}\n" \
                     f"{Constant.IMOGE['emotion']['paw']}지역발생 : {data['result']['list'][-1]['local']}명\n" \
                     f"{Constant.IMOGE['emotion']['paw']}해외발생 : {data['result']['list'][-1]['oversea']}명 입니다!\n " \
                     f"코로나 조심하세요!{Constant.IMOGE['emotion']['nexpression']}"
            # 결과 컨텍스트

            self.return_string = GEN.set_card(Constant.SANDOL_COVID_IMG, is_title="코로나 확진자 수",
                                              is_description=result)

        except Exception as e:
            description = f"코로나 확진자 정보를 불러오는데 실패했어요{Constant.IMOGE['emotion']['sad']}\n"
            self.return_string = GEN.set_card(Constant.SANDOL_COVID_IMG, is_title=f"{e}", is_description=description)

        finally:
            return self.return_string


class Weather:
    def __init__(self):
        self.URL = 'https://search.naver.com/search.naver?query='
        self.return_string = ''

    def weather(self, location: str = "정왕") -> dict:
        url = self.URL + (location + "날씨")
        html = requests.get(url).text
        soup = BeautifulSoup(html, 'html.parser')
        weather_box = soup.find('section', {'class': 'sc_new cs_weather_new _cs_weather'})
        info = weather_box.find('div', {'class': 'weather_graphic'})
        weather_info = info.find("div", {"class": "weather_main"}).get_text()
        temp = info.find("div", {"class": "temperature_text"}).get_text()
        temp = temp[temp.find("도") + 1:]

        temp_summary = weather_box.find("div", {"class": "temperature_info"})
        compare_yesterday = temp_summary.find("p").get_text().split('  ')[0]

        chart_list = weather_box.find("div", {"class": "report_card_wrap"})
        chart = []  # 미세먼지, 초미세먼지, 자외선, 일몰 순서
        for i in chart_list.find_all("li"):
            chart.append(i.get_text().strip().split(" ")[1])

        result = f"오늘 {location}의 날씨는 {Constant.IMOGE['weather'][weather_info.strip()]}{weather_info}이고, " \
                 f"기온은 {temp}C 으로 {compare_yesterday}\n"\
                 f"미세먼지는 {chart[0]}, 초미세먼지는 {chart[1]}이며, 자외선은 {chart[2]} 입니다!\n"
        return GEN.set_text(result)


class Announcement:
    def __init__(self):
        self.URL = "http://www.kpu.ac.kr/front/boardlist.do?bbsConfigFK=1&siteGubun=14&menuGubun=1"
        self.ORIGIN = "http://www.kpu.ac.kr"
        self.TITLE = "교내 최신 학사공지 내역입니다"
        self.MAX_ANNOUNCEMENT_CNT = 5  # 최대 가져올 공지 수
        self.webLinkUrl = "http://www.kpu.ac.kr/contents/main/cor/noticehaksa.html"

    def announce(self) -> dict:
        try:
            req = requests.get(self.URL)
            soup = BeautifulSoup(req.text, 'html.parser')
            announce_list = soup.find('table').find('tbody').find_all('tr')
            result = []  # title, date, URl

            for i in range(self.MAX_ANNOUNCEMENT_CNT):
                result.append([announce_list[i].find_all("td")[1].find('a').text.strip(),
                               announce_list[i].find_all("td")[4].text.strip(),
                               self.ORIGIN + announce_list[i].find_all("td")[1].find("a")['href']])

            return GEN.set_list(self.TITLE, result,
                                is_Button=GEN_OPTION.Button(label="바로가기", action="webLink", webLinkUrl=self.webLinkUrl))

        except Exception as e:
            return GEN.set_text(f"{e}")


class LiveSubwayTraffic:
    def __init__(self, station_no = ["455", "11120"]) -> None:
        self.URL = "https://map.naver.com/v5/api/transit/subway/stations/"
        self.time = None
        self.station_name: str
        self.return_data = ''
        self.station_no = station_no

    def get_data(self) -> dict:
        URL = self.URL + self.station_no + "/schedule?lang=ko&stationID=" + self.station_no
        html = requests.get(URL).text
        soup = BeautifulSoup(html, 'html.parser')

        json_data = json.loads(soup.text)
        # print(json_data)
        return json_data

    def arrival_time(self):
        try:
            if self.data['todayServiceDay']['name'] == '평일':  # 평일 시간표
                schedule_data_up = self.data['weekdaySchedule']['up']
                schedule_data_down = self.data['weekdaySchedule']['down']

                it = schedule_data_up.__iter__()  # 상행선
                flag = False
                for i in schedule_data_up:
                    it.__next__()
                    if datetime.datetime.strptime(i['departureTime'], '%H:%M:%S') > self.time:
                        self.return_data += i['headsign'] + " 방면 " + i['departureTime'] + ", "\
                                            + it.__next__()['departureTime'] + "\n"
                        flag = True
                        break
                    else:
                        continue

                if flag == False:
                    self.return_data += schedule_data_up[-1]['headsign'] + schedule_data_up[-1]['departureTime'] + " 막차입니다"

                self.return_data += "\n\n"

                flag = False
                it = schedule_data_down.__iter__()  # 하행선
                for i in schedule_data_down:
                    it.__next__()
                    if datetime.datetime.strptime(i['departureTime'], '%H:%M:%S') > self.time:
                        self.return_data += i['headsign'] + "방면 " + i['departureTime'] + ", " \
                                            + it.__next__()['departureTime'] + "\n"
                        flag = True
                        # print(i['departureTime'], end=' ')
                        # print(it.__next__()['departureTime'], end=' ')
                        break

                    else:
                        continue

                if flag == False:
                    self.return_data += schedule_data_down[-1]['headsign'] + schedule_data_down[-1][
                        'departureTime'] + " 막차입니다"

            else:  # 주말 시간표
                schedule_data_up = self.data['sundaySchedule']['up']
                schedule_data_down = self.data['sundaySchedule']['down']

                flag = False

                it = schedule_data_up.__iter__()
                for i in schedule_data_up:
                    it.__next__()
                    if datetime.datetime.strptime(i['departureTime'], '%H:%M:%S') > self.time:
                        self.return_data += i['headsign'] + "방면 " + i['departureTime'] + ", " \
                                            + it.__next__()['departureTime'] + "\n"
                        flag = True
                        # print(i['departureTime'], end=' ')
                        # print(it.__next__()['departureTime'])
                        break

                    else:
                        continue

                if flag == False:
                    self.return_data += schedule_data_up[-1]['headsign'] + schedule_data_up[-1]['departureTime'] + " 막차입니다"

                flag = False
                it = schedule_data_down.__iter__()
                for i in schedule_data_down:
                    it.__next__()
                    if datetime.datetime.strptime(i['departureTime'], '%H:%M:%S') > self.time:
                        self.return_data += i['headsign'] + "방면 " + i['departureTime'] + ", " \
                                            + it.__next__()['departureTime'] + "\n"
                        flag = True
                        # print(i['departureTime'], end=' ')
                        # print(it.__next__()['departureTime'])
                        break

                    else:
                        continue

                if flag == False:
                    self.return_data += schedule_data_down[-1]['headsign'] + schedule_data_down[-1][
                        'departureTime'] + " 막차입니다"

        except Exception as e:
            return str(e)


    def get_time(self) -> dict:
        return gen.set_text(self.time)

    def get_string(self, time):
        self.time = datetime.datetime.strptime(time, '%H:%M:%S')  # time 모듈로 변환
        for subway in self.station_no:
            self.station_no = subway
            self.data = self.get_data()
            self.arrival_time()
        return GEN.set_text(self.return_data)


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
        #1~5 산돌 분식, 6 산돌 카페
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
    print(Weather().weather())