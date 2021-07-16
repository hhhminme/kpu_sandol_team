from bs4 import BeautifulSoup
import requests
import boto3
import random
import datetime
import json
import time
import return_type_generator as Generator

imoge_mapping = {
    'emotion':{
        'paw' : '🐾',
        'smile' : '😺',
        'happy' : '😸',
        'sad' : '😹',
        'love' : '😻',
        'confident' : '😼',
        'angry' : '😾',
        'surprise' : '🙀',
        'walk' : '🐈',
        'nexpression' : '🐱'

    },
    'weather':{
        '흐림' : '☁',
        '구름많음' : '⛅',
        'hvy_rain' : '⛈',
        '비' : '☔',
        '약간흐림' : '🌤',
        '맑음' : '☀',
        'sun_wth_rain' : '🌦',
        'thunder' : '🌩',
        '바람' : '🌪',
        '안개' : '🌫'
    }
}
gen = Generator.Return_Type()
opt = Generator.Common_params()
class CrawlingFunction():
    def subway(self, station='정왕'):
        try:
            header = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36"}
            arrival_subway_api_url = "http://swopenapi.seoul.go.kr/api/subway/49664c636d6a68303634704d4f7649/json/realtimeStationArrival/0/5/" + station
            soup = requests.get(arrival_subway_api_url, headers=header)  # 여기까지 기본 크롤링 준비

            if soup.status_code != 200:
                raise Exception('[Crawling-Error #001] API 서버에 연결을 실패했습니다 잠시후 다시 시도해주세요'+ imoge_mapping['emotion']['sad'])

            receptdata = soup.json()
            reprocess = {'subwayStatus': [],  # arivlCd
                         'subwayPos': [],  # arivlMsg2
                         'reqDate': None,  # recptnDt
                         'heading': [],  # trainLineNm
                         'arivlTime': []  # barvlDt
                         }

            reprocess['reqDate'] = receptdata['realtimeArrivalList'][0]['recptnDt']
            for i in range(len(receptdata['realtimeArrivalList'])):
                reprocess['subwayStatus'].append(receptdata['realtimeArrivalList'][i]['arvlCd'])
                reprocess['subwayPos'].append(receptdata['realtimeArrivalList'][i]['arvlMsg2'])
                reprocess['heading'].append(receptdata['realtimeArrivalList'][i]['trainLineNm'])
                reprocess['arivlTime'].append(
                    receptdata['realtimeArrivalList'][i]['barvlDt'])  # 여기까지 크롤링 한 내용들 기준으로 업데이트

            retn_str = reprocess['reqDate'] + "기준 " + station + " 도착정보입니다"+ imoge_mapping['emotion']['walk']+"\n"
            for i in range(len(reprocess['arivlTime'])):
                rept_str = str(i + 1) + ".\n[" + reprocess['heading'][i] + "] - " + "\n" + reprocess['subwayPos'][i] + "\n\n"
                retn_str += rept_str

            retn_str += imoge_mapping['emotion']['paw']+"실제 열차 도착 시간과 상이할 수 있습니다.\n"

            return gen.is_Text(retn_str)


        except Exception as e:
            return gen.is_Text("[Crawling_Error #002] 현재 열차 운행 시간이 아니거나, API 서버와의 통신에 실패하였습니다"+ imoge_mapping['emotion']['sad'])
    def last_subway(self):
        def station_no4():
            target_url = "https://map.naver.com/v5/api/transit/subway/stations/455/schedule?lang=ko&stationID=455"
            html = requests.get(target_url)
            soup = BeautifulSoup(html.text, 'html.parser')

            last_arrival_weekday = json.loads(soup.text)["weekdaySchedule"]  # 평일
            last_arrival_weekend = json.loads(soup.text)["sundaySchedule"]  # 주말

            weekday_last = [last_arrival_weekday['up'][101 + i] for i in range(len(last_arrival_weekday['up']) - 101)][
                           ::-1]  # 역순으로 변경
            weekend_last = [last_arrival_weekend['up'][85 + i] for i in range(len(last_arrival_weekend['up']) - 85)][
                           ::-1]  # 역순으로 변경
            station = [i['headsign'] for i in weekday_last]  # headsign이 가장 처음으로 나오는 경우의 인덱스를 반환하기 위한 리스트
            station2 = [i['headsign'] for i in weekend_last]  # headsign이 가장 처음으로 나오는 경우의 인덱스를 반환하기 위한 리스트
            find_station_idx = station.index  # 가독성 up
            find_station2_idx = station2.index  # 가독성 up

            return "당고개 - (평일) ", weekday_last[find_station_idx("당고개")]['departureTime'][:-3], " (휴일) ", \
                   weekend_last[find_station2_idx("당고개")]['departureTime'][:-3] \
                   + "\n안산 - (평일) ", weekday_last[find_station_idx("안산")]['departureTime'][:-3] \
                   + "\n노원 - (평일) ", weekday_last[find_station_idx("노원")]['departureTime'][:-3], " (휴일) ", \
                   weekend_last[find_station2_idx("노원")]['departureTime'][:-3] \
                   + "\n금정 - (평일) ", weekday_last[find_station_idx("금정")]['departureTime'][:-3], " (휴일) ", \
                   weekend_last[find_station2_idx("금정")]['departureTime'][:-3] \
                   + "\n한성대입구 - (휴일) ", weekend_last[find_station2_idx("한성대입구")]['departureTime'][:-3] \
                   + "\n사당 - (휴일) ", weekend_last[find_station2_idx("사당")]['departureTime'][:-3] \
                   + "\n오이도 - (평일) ", last_arrival_weekday['down'][-1]['departureTime'][:-3], " (휴일) ", \
                   last_arrival_weekend['down'][-1]['departureTime'][:-3]

        def station_suin():
            target_url = "https://map.naver.com/v5/api/transit/subway/stations/11120/schedule?lang=ko&stationID=11120"
            html = requests.get(target_url)
            soup = BeautifulSoup(html.text, 'html.parser')

            last_arrival_weekday = json.loads(soup.text)["weekdaySchedule"]  # 평일
            last_arrival_weekend = json.loads(soup.text)["sundaySchedule"]  # 주말
            weekday_last = [last_arrival_weekday['up'][i] for i in range(len(last_arrival_weekday['up']))][
                           ::-1]  # 역순으로 변경 (상행)
            weekend_last = [last_arrival_weekend['up'][i] for i in range(len(last_arrival_weekend['up']))][
                           ::-1]  # 역순으로 변경

            weekday_last2 = [last_arrival_weekday['down'][i] for i in range(len(last_arrival_weekday['down']))][
                            ::-1]  # 역순으로 변경 (하행)
            weekend_last2 = [last_arrival_weekend['down'][i] for i in range(len(last_arrival_weekend['down']))][
                            ::-1]  # 역순으로 변경

            station = [i['headsign'] for i in weekday_last]  # headsign이 가장 처음으로 나오는 경우의 인덱스를 반환하기 위한 리스트 (상행)
            station2 = [i['headsign'] for i in weekend_last]  # headsign이 가장 처음으로 나오는 경우의 인덱스를 반환하기 위한 리스트

            station_down = [i['headsign'] for i in weekday_last2]  # headsign이 가장 처음으로 나오는 경우의 인덱스를 반환하기 위한 리스트 (하행)
            station_down2 = [i['headsign'] for i in weekend_last2]  # headsign이 가장 처음으로 나오는 경우의 인덱스를 반환하기 위한 리스트

            find_station_idx = station.index  # 가독성 up  (상행)
            find_station2_idx = station2.index  # 가독성 up

            find_station_down_idx = station_down.index  # 가독성 up (하행)
            find_station_down_idx2 = station_down2.index  # 가독성 up
            return "왕십리 - (평일) ", weekday_last[find_station_idx("왕십리")]['departureTime'][:-3], " (휴일) ", \
                   weekend_last[find_station2_idx("왕십리")]['departureTime'][:-3] \
                   + "\n죽전 - (평일) ", weekday_last[find_station_idx("죽전")]['departureTime'][:-3], " (휴일) ", \
                   weekend_last[find_station2_idx("죽전")]['departureTime'][:-3] \
                   + "\n고색 - (평일) ", weekday_last[find_station_idx("고색")]['departureTime'][:-3], " (휴일) ", \
                   weekend_last[find_station2_idx("고색")]['departureTime'][:-3] \
                   + "\n오이도 - (평일) ", weekday_last2[find_station_down_idx("오이도")]['departureTime'][:-3], " (휴일) ", \
                   weekend_last2[find_station_down_idx2("오이도")]['departureTime'][:-3] \
                   + "\n인천 - (평일) ", weekday_last2[find_station_down_idx("인천")]['departureTime'][:-3], " (휴일) ", \
                   weekend_last2[find_station_down_idx2("인천")]['departureTime'][:-3]

        # station_suin()
        return_str = imoge_mapping['emotion']['walk'] + '4호선 막차 시간입니다\n'
        return_str += ''.join(station_no4())
        return_str += '\n\n' + imoge_mapping['emotion']['walk'] + '수인선 막차 시간입니다\n'
        return_str += ''.join(station_suin())
        return gen.is_Text(return_str)
        # boto3 주석 해제하기
    # def random_meal(self):
    #     s3 = boto3.resource('s3')
    #     bucket = s3.Bucket("sandol")
    #     try:
    #         local_file = "/tmp/" + "test.txt"
    #         bucket.download_file("tmp/test.txt", local_file)  # s3에서 파일을 다운로드 후 /tmp에 저장
    #
    #     except Exception as e:
    #         return str(e)
    #
    #     with open("/tmp/test.txt", "r", encoding='UTF-8') as rf:
    #         data = rf.readlines()  # 파일을 전부 읽어서 list로 변환
    #
    #     idx = random.randint(0, 100)
    #     result_string = data[idx]
    #     return "☆빠밤★\n" + result_string.split("->")[0] + " 에서, " + result_string.split("->")[1].replace("\n",
    #                                                                                                    '') + " 어떠세요?"

    def today_covid(self):
        try:
            url = 'https://m.search.naver.com/p/csearch/content/nqapirender.nhn?where=nexearch&pkid=9005&key=diffV2API'
            html = requests.get(url).text
            data = json.loads(html)
            result = data['result']['list'][-1]['date'] +"일까지 코로나 발생 현황이에요"+imoge_mapping['emotion']['walk']+"\n"+imoge_mapping['emotion']['paw']+"지역발생 : " + data['result']['list'][-1]['local'] +"명\n" + imoge_mapping['emotion']['paw'] + "해외유입 : "+data['result']['list'][-1]['oversea']+"명 입니다!\n코로나 조심하세요"+imoge_mapping['emotion']['nexpression']
            return gen.is_Card("https://raw.githubusercontent.com/hhhminme/kpu_sandol_team/main/img/card_covid.png", is_title="코로나 확진자 수", is_description= result)

        except Exception as e:
            return gen.is_Text("코로나 확진자 정보를 불러오는데 실패했어요" + imoge_mapping['emotion']['sad'])

    def weather(self, location):

        url = 'https://search.naver.com/search.naver?query=' + location + "날씨"
        html = requests.get(url).text
        soup = BeautifulSoup(html, 'html.parser')
        form = soup.find("div", {'class': 'api_subject_bx'}).find("div", {'class': 'main_info'}).find("div", {
            'class': 'info_data'})
        sub_form = soup.find("div", {'class': 'api_subject_bx'}).find("div", {'class': 'sub_info'}).find("div", {
            'class': 'detail_box'})
        today_temp = form.find("span", {'class': 'todaytemp'}).text

        try:
            today_temp_min = form.find("span", {'class': 'min'}).text
        except:
            today_temp_min = "-"

        try:
            today_temp_max = form.find("span", {'class': 'max'}).text
        except:
            today_temp_max = "-"

        try:
            today_temp_ray = form.find("span", {'class': 'indicator'}).find("span").text
        except:
            today_temp_ray = "-"
        update_date = soup.find("div", {'class': 'guide_bx _guideBox'}).find("span", {'class': 'guide_txt'}).find(
            'span', {'class': 'update'}).text

        today_weather = form.find("ul").find("li").text.strip()
        today_dust_list = sub_form.find_all("dd")
        today_dust10 = today_dust_list[0].text
        today_dust25 = today_dust_list[1].text

        try:
            weather_icon = imoge_mapping['weather'][today_weather.split(', ')[0]]

        except:
            weather_icon = ''

        result = imoge_mapping['emotion']['walk']+ location + "의  기상정보입니다" \
            "\n\n기온 : " + today_temp + "°C (" + today_temp_min + "C / " + today_temp_max + "C)\n" + weather_icon + today_weather + \
                 "\n\n미세먼지 : " + today_dust10.replace("㎥", "㎥, ") + "\n초미세먼지 : " + today_dust25.replace("㎥", "㎥, ") + \
                 "\n자외선 : " + today_temp_ray + "이에요!\n\n" + update_date + "시에 업데이트 된 네이버 날씨 정보입니다!"

        return gen.is_Text(result)

    def announcement(self):
        URL = "http://www.kpu.ac.kr/front/boardlist.do?bbsConfigFK=1&siteGubun=14&menuGubun=1"
        ORIGIN = "http://www.kpu.ac.kr"
        req = requests.get(URL)
        soup = BeautifulSoup(req.text, 'html.parser')
        announce_list = soup.find('table').find('tbody').find_all('tr')
        result = [] # title, date, URl

        for i in range (5):
            result.append([announce_list[i].find_all("td")[1].find('a').text.strip(), announce_list[i].find_all("td")[4].text.strip(), ORIGIN+announce_list[i].find_all("td")[1].find("a")['href']])
        return gen.is_List("교내 최신 학사공지 내역입니다", result, is_Button= opt.Button(label="바로가기", action="webLink", webLinkUrl = "http://www.kpu.ac.kr/contents/main/cor/noticehaksa.html"))

class s3IOEvent():
    def upload_feedback(self, params):  # 피드백 업로드 기능
        s3 = boto3.resource('s3')
        bucket = s3.Bucket('sandol')  # 이 부분 해당 버킷 생성 후 적절히 수정 예정
        params = "[" + str(datetime.datetime.today()) + "] :" + params + "\n"
        try:
            local_file = "/tmp/" + "feedback.txt"
            bucket.download_file("feedback.txt", local_file)
        except Exception as e:
            return gen.is_Text("[File-Open-Error #101] 서버에서 피드백 파일을 불러오는 중 오류가 발생했어요"+ imoge_mapping['emotion']['sad'])

        try:
            with open("/tmp/feedback.txt", "a", encoding="UTF-8") as f:
                f.writelines(params)
        except Exception as e:
            return gen.is_Text("[File-Open-Error #102] 파일을 저장 중 오류가 발생했습니다" + imoge_mapping['emotion']['sad'])

        try:
            s3 = boto3.client('s3')  # 이 부분 해당 버킷 생성 후 적절히 수정 예정
            s3.upload_file("/tmp/feedback.txt", 'sandol', 'feedback.txt')

        except Exception as e:
            return gen.is_Text("[File-Open-Error #103] 파일을 서버에 업로드 하는 중 오류가 발생했습니다" + imoge_mapping['emotion']['sad'])

        return gen.is_Text("피드백 주셔서 감사해요! 빠른 시일내에 검토 후 적용해볼게요!" + imoge_mapping['emotion']['love'])

    def read_feedback(self, params, bot_id):  # 피드백 읽기 기능 (관리자 전용)
        sandol_team = ['d367f2ec55f41b4207156f4b8fce5ce885b05d8c3b238cf8861c55a9012f6f5895',
                       '339b0444bfabbffa0f13508ea7c45b61675b5720234cca8f73cd7421c22de9e546',
                       '04eabc8b965bf5ae6cccb122a18521969cc391162e3fd5f61b85efe8bb12e5e98a',
                       'def99464e022b38389697fe68d54bbba723d1da291094c19bbf5eaace7b059a997']

        if bot_id not in sandol_team:
            return gen.is_Text("권한이 없습니다")

        if params == '1':  # 읽기
            s3 = boto3.resource('s3')
            bucket = s3.Bucket("sandol")

            try:
                local_file = "/tmp/" + "feedback.txt"
                bucket.download_file("feedback.txt", local_file)
            except Exception as e:
                return gen.is_Text("[File-Open-Error #111] 서버에서 피드백 파일을 불러오는 중 오류가 발생했어요 ")

            try:
                with open("/tmp/feedback.txt", "r", encoding="UTF-8") as f:  # 이 부분 해당 버킷 생성 후 적절히 수정 예정
                    txt = ''.join(f.readlines())
                    return gen.is_Text(txt)

            except Exception as e:
                return gen.is_Text("[File-Open-Error #112] 파일을 읽는 중 오류가 발생했습니다")

        elif params == '2':  # 지우기
            s3 = boto3.resource('s3')
            bucket = s3.Bucket('sandol')  # 이 부분 해당 버킷 생성 후 적절히 수정 예정
            params = "#feedbacks\n"
            try:
                local_file = "/tmp/" + "feedback.txt"
                bucket.download_file("feedback.txt", local_file)
            except Exception as e:
                return gen.is_Text("[File-Open-Error #113] 서버에서 피드백 파일을 불러오는 중 오류가 발생했어요")

            try:
                with open("/tmp/feedback.txt", "w", encoding="UTF-8") as f:  # 이 부분 해당 버킷 생성 후 적절히 수정 예정
                    f.writelines(params)
            except Exception as e:
                return gen.is_Text("[File-Open-Error #114] 파일을 삭제 중 오류가 발생했습니다")

            try:
                s3 = boto3.client('s3')
                s3.upload_file("/tmp/feedback.txt", 'sandol', 'feedback.txt')

            except Exception as e:
                return gen.is_Text("[File-Open-Error #115] 파일을 서버에 업로드 하는 중 오류가 발생했습니다")
            return gen.is_Text("성공적으로 파일 내용을 삭제했습니다")


        else:  # param error
            return gen.is_Text('[Param-Error #116] 잘못된 파라미터')

    def upload_meal(self, store_name, lunch_list, dinner_list,input_date, owner_id):  # 식사 업로드 기능
        owner_id_dec = {'미가식당': "32d8a05a91242ffb4c64b5630ec55953121dffd83a121d985e26e06e2c457197e6",
                        '웰스프레쉬': "d367f2ec55f41b4207156f4b8fce5ce885b05d8c3b238cf8861c55a9012f6f5895",
                        '푸드라운지': "46f338132e6af63c32c07220c318f0e7c570e8eb6f375c9e8bb59ce33776f27c4c"
                        }
        sandol_team = ['d367f2ec55f41b4207156f4b8fce5ce885b05d8c3b238cf8861c55a9012f6f5895',
                       '339b0444bfabbffa0f13508ea7c45b61675b5720234cca8f73cd7421c22de9e546',
                       '04eabc8b965bf5ae6cccb122a18521969cc391162e3fd5f61b85efe8bb12e5e98a',
                       'def99464e022b38389697fe68d54bbba723d1da291094c19bbf5eaace7b059a997']

        if (owner_id_dec[store_name] != owner_id) and owner_id not in sandol_team:
            return gen.is_Text("[Permission-Error #121-1] 권한이 없습니다" + imoge_mapping['emotion']['angry'])

        if store_name not in owner_id_dec.keys():
            return gen.is_Text("[Not-Found-Error #121-2] 해당하는 식당이 없습니다."+ imoge_mapping['emotion']['sad'])

        else:
            store_file = "restaurant_menu.txt"
            s3 = boto3.resource('s3')
            bucket = s3.Bucket("sandol")
            local_file = "/tmp/" + store_file

            try:
                # local_file = "./restaurant_menu/" + store_file
                s3.meta.client.download_file("sandol", "restaurant_menu.txt", '/tmp/restaurant_menu.txt')

            except Exception as e:
                return gen.is_Text("[File-Open-Error #122] 저장소에서 파일을 찾을 수 없습니다."+ imoge_mapping['emotion']['sad'])

            with open(local_file, "r", encoding="UTF-8") as f:
                try:
                    data = f.readlines()
                    print(data)
                    menu_info = data[data.index("🐾"+store_name+"\n") + 1].replace('\'','').replace("\n","").split(", ") #내부 데이터 처리
                    menu_info[0] = input_date

                    menu_info[1] = lunch_list.replace(", ",",").replace(" ",",")
                    menu_info[2] = dinner_list.replace(",","").replace(" ",",") #메뉴 수정

                    menu_info[1] = lunch_list.replace(" ",",")
                    menu_info[2] = dinner_list.replace(" ",",") #메뉴 수정

                    menu_info[1] = lunch_list.replace(" ",",")
                    menu_info[2] = dinner_list.replace(" ",",") #메뉴 수정

                    data[data.index("🐾"+store_name+"\n") + 1] = str(menu_info)[1:-1] + "\n" #최종 문자열
                    with open(local_file, "w", encoding='UTF-8') as rf:
                        rf.writelines(data)


                except Exception as e:
                    return gen.is_Text("[File-Open-Error #123]파일을 수정하는 중 오류가 발생했습니다."+ imoge_mapping['emotion']['sad'])
            try:
                s3 = boto3.client('s3')  # 이 부분 해당 버킷 생성 후 적절히 수정 예정
                s3.upload_file(local_file, 'sandol', store_file)

            except Exception:
                return gen.is_Text("[File-Open-Error #124]파일을 저장소에 업로드하는 중 오류가 발생했습니다."+ imoge_mapping['emotion']['sad'])


        return gen.is_Text("네! 학생들에게 잘 전달할게요! 감사합니다!"+ imoge_mapping['emotion']['walk'])


    def read_meal(self):
        store_file = "restaurant_menu.txt"
        s3 = boto3.resource('s3')  # 이 부분 해당 버킷 생성 후 적절히 수정 예정
        bucket = s3.Bucket("sandol")
        try:
            local_file = "/tmp/" + store_file
            # local_file = "./restaurant_menu/" + store_file  #이 부분 해당 버킷 생성 후 적절히 수정 예정
            bucket.download_file(store_file, local_file)

        except Exception:
            return gen.is_Text(
                "[File-Open-Error #131] 저장소에서 파일을 가져오는데 실패했습니다" + imoge_mapping['emotion']['sad'])  # 파일을 /tmp/에 복사하여 다운로드

        try:
            t = ['월', '화', '수', '목', '금', '토', '일']
            return_string = ''
            with open(local_file, "r", encoding='UTF-8') as f:
                data = f.readlines()
                for restaurant in range(0, len(data), 2):
                    menu_list = data[restaurant + 1].replace("\'", '').split(", ")
                    last_update_date = datetime.date.fromisoformat(menu_list[0])
                    if restaurant == 2:
                        return_string += "웰스프레쉬\nhttps://ibook.kpu.ac.kr/Viewer/menu01\n\n"

                    # else:
                    #     return_string += data[restaurant].replace("\n", '').replace("🐾",imoge_mapping['emotion']['walk']) + " [" + str(last_update_date) + " " + t[last_update_date.weekday()] + "요일]",imoge_mapping['emotion']['paw'] + "중식 : " + menu_list[1] + "\n" + imoge_mapping['emotion']['paw'] + "석식 : " + menu_list[2] + "\n"

                    # if restaurant == 2: # 웰스프레시는 링크로 대체~
                    #     return_string.append(["https://raw.githubusercontent.com/hhhminme/kpu_sandol_team/main/img/logo1.png", data[restaurant].replace("\n", '').replace("🐾",imoge_mapping['emotion']['walk']), "https://ibook.kpu.ac.kr/Viewer/menu01"])
                    # else :
                    #      return_string.append(["https://raw.githubusercontent.com/hhhminme/kpu_sandol_team/main/img/logo1.png", data[restaurant].replace("\n", '').replace("🐾",imoge_mapping['emotion']['walk']) + " [" + str(last_update_date) + " " + t[last_update_date.weekday()] + "요일]",imoge_mapping['emotion']['paw']+"중식 : " + menu_list[1] + "\n"+ imoge_mapping['emotion']['paw']+"석식 : " + menu_list[2] + "\n"])

            # additional_info = "\n"+imoge_mapping['emotion']['paw']+"부득이하게 메뉴가 변동될 수 있어요!"\
            #                   +"\n"+imoge_mapping['emotion']['paw']+"주말엔 학식기능이 작동하지 않아요!"\
            #                   +"\n"+imoge_mapping['emotion']['paw']+"세미콘 식당은 업주님의 사정으로 업데이트하지 못하고 있어요"+imoge_mapping['emotion']['sad']
            # return_string += additional_info

            return gen.is_Text("학식 정보입니다\n" + return_string)

        except Exception as e:
            return gen.is_Text("[File-Open-Error #132] 파일을 여는 중 오류가 발생했어요.." + imoge_mapping['emotion']['sad'] + str(e))

    def reset_meal(self, bot_id, date):
        sandol_team = ['d367f2ec55f41b4207156f4b8fce5ce885b05d8c3b238cf8861c55a9012f6f5895',
                       '339b0444bfabbffa0f13508ea7c45b61675b5720234cca8f73cd7421c22de9e546',
                       '04eabc8b965bf5ae6cccb122a18521969cc391162e3fd5f61b85efe8bb12e5e98a',
                       'def99464e022b38389697fe68d54bbba723d1da291094c19bbf5eaace7b059a997']
        if bot_id not in sandol_team:
            return gen.is_Text("[Permission-Error #141] 권한이 없습니다" + imoge_mapping['emotion']['angry'])

        store_file = "restaurant_menu.txt"
        s3 = boto3.resource('s3')
        bucket = s3.Bucket("sandol")
        local_file = "/tmp/" + store_file

        try:
            # local_file = "./restaurant_menu/" + store_file
            s3.meta.client.download_file("sandol", "restaurant_menu.txt", '/t`1mp/restaurant_menu.txt')

        except Exception as e:
            return gen.is_Text("[File-Open-Error #142] 저장소에서 파일을 찾을 수 없습니다." + imoge_mapping['emotion']['sad'])
        try:
            with open(local_file, "w", encoding="UTF-8") as f:
                rest_name = [imoge_mapping['emotion']['paw'] + "미가식당\n", imoge_mapping['emotion']['paw'] + "웰스프레쉬\n",
                             imoge_mapping['emotion']['paw'] + "푸드라운지\n"]

                return_string = ''
                for i in range(len(rest_name)):
                    return_string += rest_name[i] + "\'" + date + "\', \'업데이트되지않았습니다\', \'업데이트되지않았습니다\'\n"
                f.writelines(return_string)

        except Exception as e:
            return gen.is_Text("[File-Open-Error #143]파일을 수정하는 중 오류가 발생했습니다." + imoge_mapping['emotion']['sad'])

        try:
            s3 = boto3.client('s3')  # 이 부분 해당 버킷 생성 후 적절히 수정 예정
            s3.upload_file(local_file, 'sandol', store_file)

        except Exception:
            return gen.is_Text("[File-Open-Error #144]파일을 저장소에 업로드하는 중 오류가 발생했습니다." + imoge_mapping['emotion']['sad'])
        return gen.is_Text("파일을 정상적으로 초기화했습니다" + imoge_mapping['emotion']['happy'])

class Test():
    def __init__(self, time: str = "00:00:00", station_no: str = "455") ->None:
        self.time = datetime.datetime.strptime(time, '%H:%M:%S')    #time 모듈로 변환
        self.station_no = station_no
        self.rail: str
        self.station_name: str
        self.data = self.get_data()

    def get_data(self) -> dict:
        URL = "https://map.naver.com/v5/api/transit/subway/stations/"+self.station_no+"/schedule?lang=ko&stationID="+self.station_no
        html = requests.get(URL).text
        soup = BeautifulSoup(html, 'html.parser')

        json_data = json.loads(soup.text)
        # print(json_data)
        return json_data

    def arrival_time(self) -> str:
        return_data = ''

        try:
            if self.data['todayServiceDay']['name'] == '평일':  # 평일 시간표
                schedule_data_up = self.data['weekdaySchedule']['up']
                schedule_data_down = self.data['weekdaySchedule']['down']

                it = schedule_data_up.__iter__()  # 상행선
                flag = False
                for i in schedule_data_up:
                    it.__next__()
                    if datetime.datetime.strptime(i['departureTime'], '%H:%M:%S') > self.time:
                        return_data += i['headsign'] +"방면 "+ i['departureTime'] + ", " + it.__next__()['departureTime']
                        # print(i['departureTime'], end=' ')
                        # print(it.__next__()['departureTime'])
                        flag = True
                        break
                    else:
                        continue

                if flag == False:
                    return_data += schedule_data_up[-1]['headsign'] + schedule_data_up[-1]['departureTime']+ " 막차입니다"

                return_data +=  "\n\n"

                flag = False
                it = schedule_data_down.__iter__()  # 하행선
                for i in schedule_data_down:
                    it.__next__()
                    if datetime.datetime.strptime(i['departureTime'], '%H:%M:%S') > self.time:
                        return_data += i['headsign'] +"방면 "+i['departureTime'] + ", " + it.__next__()['departureTime']
                        flag = True
                        # print(i['departureTime'], end=' ')
                        # print(it.__next__()['departureTime'], end=' ')
                        break

                    else:
                        continue

                if flag == False:
                    return_data += schedule_data_down[-1]['headsign'] + schedule_data_down[-1]['departureTime']+ " 막차입니다"

            else:  # 주말 시간표
                schedule_data_up = self.data['sundaySchedule']['up']
                schedule_data_down = self.data['sundaySchedule']['down']

                flag = False

                it = schedule_data_up.__iter__()
                for i in schedule_data_up:
                    it.__next__()
                    if datetime.datetime.strptime(i['departureTime'], '%H:%M:%S') > self.time:
                        return_data += i['headsign'] +"방면 "+i['departureTime'] + ", " + it.__next__()['departureTime']
                        flag = True
                        # print(i['departureTime'], end=' ')
                        # print(it.__next__()['departureTime'])
                        break

                    else:
                        continue

                if flag == False:
                    return_data += schedule_data_up[-1]['headsign'] +schedule_data_up[-1]['departureTime']+ " 막차입니다"
                return_data += "\n\n"

                flag = False
                it = schedule_data_down.__iter__()
                for i in schedule_data_down:
                    it.__next__()
                    if datetime.datetime.strptime(i['departureTime'], '%H:%M:%S') > self.time:
                        return_data += i['headsign'] +"방면 "+i['departureTime'] + ", " + it.__next__()['departureTime']
                        flag = True
                        # print(i['departureTime'], end=' ')
                        # print(it.__next__()['departureTime'])
                        break

                    else:
                        continue

                if flag == False:
                    return_data += schedule_data_down[-1]['headsign'] +schedule_data_down[-1]['departureTime'] + " 막차입니다"

        except Exception as e:
            return str(e)

        return return_data

    def get_time(self):
        return gen.is_Text(self.time)
    #boto3 주석 해제하기
# print(Test("23:59:11", "455").arrival_time())