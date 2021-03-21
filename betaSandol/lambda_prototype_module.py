from bs4 import BeautifulSoup
import requests
import boto3
import random
import datetime
import json
class CrawlingFunction():
    def subway(self, station):
        try:
            header = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36"}
            arrival_subway_api_url = "http://swopenapi.seoul.go.kr/api/subway/49664c636d6a68303634704d4f7649/json/realtimeStationArrival/0/5/" + station
            soup = requests.get(arrival_subway_api_url, headers=header)     #여기까지 기본 크롤링 준비

            if soup.status_code != 200:
                raise Exception('API 서버에 연결을 실패했습니다 잠시후 다시 시도해주세요')
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
                reprocess['arivlTime'].append(receptdata['realtimeArrivalList'][i]['barvlDt'])              #여기까지 크롤링 한 내용들 기준으로 업데이트


            retn_str = "-------------------------------------------------\n" + \
                       reprocess['reqDate'] + "기준 " + station + " 도착정보입니다\n" + \
                       "-------------------------------------------------\n"
            print(len(reprocess['arivlTime']))
            for i in range(len(reprocess['arivlTime'])):
                rept_str = str(i + 1) + ".\n[" + reprocess['heading'][i] + "] - "  + "\n" + "도착 예정 시각 :" + reprocess['arivlTime'][i] + "초 후\n\n" +  reprocess['subwayPos'][i] + "\n\n"
                retn_str += rept_str

            retn_str += "*실제 열차 도착 시간과 상이할 수 있습니다.\n" \
                        "*API의 문제로 일부 역에서는 도착 예정 시간이 0초로 표기되는 오류가 있을 수 있습니다."

            return retn_str

            '''
            출력 예시

            2021-01-10
            -----------------------------------------------------
            15 : 50 : 18.0 기준 열차 도착 정보입니다. (recptnDt)
            -----------------------------------------------------
            1.
            [당고개행 - 신길온천방면 ](trainLineNm) - 도착(arivlCd)

            도착 예정시각 : 0 초 후

            정왕 도착

            2.
            [오이도행 - 오이도방면 ](trainLineNm) - 운행중(arivlCd)

            도착 예정시각 : 0 초 후

            [3]번째 전역 (초지)

            *실제 열차 도착 시간과 상이할 수 있습니다.
            *API의 문제로 일부 역에서는 도착 예정 시간이 0초로 표기되는 오류가 있을 수 있습니다.
            '''
        except Exception as e:
            return ("["+str(e)+"] 현재 열차 운행 시간이 아니거나, API 서버와의 통신에 실패하였습니다")

    def random_meal(self):
        s3 = boto3.resource('s3')
        bucket = s3.Bucket("my-lambda-bucket-text")
        try:
            local_file = "/tmp/" + "test.txt"
            bucket.download_file("tmp/test.txt", local_file)    #s3에서 파일을 다운로드 후 /tmp에 저장
        except Exception as e:
            return str(e)

        with open("../../../KaKaoTalk ChatBot/openbuilder/tmp/test.txt", "r", encoding ='UTF-8') as rf:
            data = rf.readlines()  # 파일을 전부 읽어서 list로 변환
        # date = datetime.date.fromisoformat(data[0].replace("\n", "").split(" : ")[1])

        # try:
        #     if (date != datetime.date.today()):  # 만약  Datetime이 다르다면 크롤링을 하고 파일을 저장 / 즉, 하루마다 업데이트함 (태평양 시 기준)
        #         try:
        #             url = 'https://map.naver.com/v5/api/search?caller=pcweb&query=정왕역 맛집&displayCount=100'
        #             header = {
        #                 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'}
        #
        #             html = requests.get(url, data=header).text
        #             req_json = json.loads(html)
        #             data = ''
        #             data = data + ("date : " + str(datetime.date.today()) + "\n")
        #
        #             for line in range(100):
        #                 data = data + (req_json['result']['place']['list'][line]['name'] + "(" +
        #                                req_json['result']['place']['list'][line]['category'][0] + ")->" +
        #                                req_json['result']['place']['list'][line]['category'][1] + "\n")
        #             with open("/tmp/test.txt", "w", encoding="UTF-8") as wf:
        #                 wf.writelines(data)
        #         except Exception as e:
        #             return "third"+str(e)
        #         s3 = boto3.client("s3")
        #         s3.upload_file("/tmp/test.txt", "my-lambda-buckcet-text", "tmp/test.txt")
        #         data = data.split("\n")
        # except Exception as e:
        #     return "second" + str(e)

        idx = random.randint(0,100)
        result_string = data[idx]
        return "☆빠밤★\n"+ result_string.split("->")[0] +" 에서, "+result_string.split("->")[1].replace("\n", '')+" 어떠세요?"


class s3IOEvent():
    def upload_feedback(self, params):
        s3 = boto3.resource('s3')
        bucket = s3.Bucket('my-lambda-bucket-text')
        params = "[" + str(datetime.datetime.today()) + "] :" + params + "\n"
        try:
            local_file = "/tmp/" + "feedback.txt"
            bucket.download_file("tmp/feedback.txt", local_file)
        except Exception as e:
            return "서버에서 피드백 파일을 불러오는 중 오류가 발생했어요 [Errno 1]"

        try:
            with open("/tmp/feedback.txt", "a", encoding="UTF-8") as f:
                f.writelines(params)
        except Exception as e:
            return "파일을 저장 중 오류가 발생했습니다 [Errno 2]"

        try:
            s3 = boto3.client('s3')
            s3.upload_file("/tmp/feedback.txt", 'my-lambda-bucket-text', 'tmp/feedback.txt')

        except Exception as e:
            return "파일을 서버에 업로드 하는 중 오류가 발생했습니다 [Errno 3]"

        return "성공적으로 파일을 저장했습니다."

    def read_feedback(self, params):
        if params == '1':
            s3 = boto3.resource('s3')
            obj = s3.Object('my-lambda-bucket-text', 'tmp/feedback.txt')
            body = obj.get()['Body'].read().decode('UTF-8')
            return str(body)

        elif params == '2':
            s3 = boto3.resource('s3')
            bucket = s3.Bucket('my-lambda-bucket-text')
            params = "#feedbacks\n"
            try:
                local_file = "/tmp/" + "feedback.txt"
                bucket.download_file("tmp/feedback.txt", local_file)
            except Exception as e:
                return "서버에서 피드백 파일을 불러오는 중 오류가 발생했어요 [Errno 1]"

            try:
                with open("/tmp/feedback.txt", "w", encoding="UTF-8") as f:
                    f.writelines(params)
            except Exception as e:
                return "파일을 삭제 중 오류가 발생했습니다 [Errno 2]"

            try:
                s3 = boto3.client('s3')
                s3.upload_file("/tmp/feedback.txt", 'my-lambda-bucket-text', 'tmp/feedback.txt')

            except Exception as e:
                return "파일을 서버에 업로드 하는 중 오류가 발생했습니다 [Errno 3]"
            return "성공적으로 파일 내용을 삭제했습니다"


        else:
            return '잘못된 파라미터'

    def upload_meal(self, input_date,store_name, lunch_list, dinner_list, owner_id):
        owner_id_dec = {'미가식당': "d38639b2a8ede3ff7f3ae424e41a38acf7b05d8c3b238cf8861c55a9012f6f5895",
                        '웰스프레쉬': "d38639b2a8ede3ff7f3ae424e41a38acf7b05d8c3b238cf8861c55a9012f6f5895",
                        '푸드라운지': "d38639b2a8ede3ff7f3ae424e41a38acf7b05d8c3b238cf8861c55a9012f6f5895"
                        }
        sandol_team = ['d38639b2a8ede3ff7f3ae424e41a38acf7b05d8c3b238cf8861c55a9012f6f5895',
                       'd38639b2a8ede3ff7f3ae424e41a38acf7b05d8c3b238cf8861c55a9012f6f5895',
                       'd38639b2a8ede3ff7f3ae424e41a38acf7b05d8c3b238cf8861c55a9012f6f5895']

        if store_name == '미가식당' and (owner_id == owner_id_dec[store_name] or owner_id in sandol_team):
            store_file = store_name + ".txt"

            s3 = boto3.resource('s3')
            bucket = s3.Bucket('my-lambda-bucket-text')

            try:
                local_file = "/tmp/" + store_file
                #local_file = "./restaurant_menu/" + store_file

                bucket.download_file("restaurant_menu/" + store_file, local_file)
            except Exception as e:
                return "fist _" + str(e)  # 파일을 /tmp/에 복사하여 다운로드

            try:
                modified_data = input_date + "\n중식 : " + lunch_list + "\n석식 : " + dinner_list
                with open (local_file, "w", encoding="UTF-8") as f:
                    f.writelines(modified_data)

            except Exception as e:
                return "secn _" + str(e)

            try:
                s3 = boto3.client('s3')
                s3.upload_file(local_file, 'my-lambda-bucket-text', "restaurant_menu/"+store_file)
            except Exception as e:
                return "thrd _" + str(e)
        else:
            return "권한이 없습니다"
    def read_meal(self, store_name):
        t = ['월', '화', '수', '목', '금', '토', '일']
        store_file = store_name + ".txt"
        s3 = boto3.resource('s3')
        bucket = s3.Bucket("my-lambda-bucket-text")
        try:
            # local_file = "/tmp/" + store_file
            local_file = "./restaurant_menu/" + store_file
            bucket.download_file("restaurant_menu/" + store_file, local_file)

        except Exception as e:
            return "fist _" + str(e)  # 파일을 /tmp/에 복사하여 다운로드

        try:
            with open(local_file,"r",encoding="UTF-8") as f:
                data = f.readlines()
                date = data[0].replace("\n",'')
                lunch = data[1].split(" : ")[1].replace("\n",'')
                dinner = data[2].split(" : ")[1].replace("\n",'')
                return_data = "["+date+" "+t[datetime.datetime.today().weekday()]+"요일] "+store_name+"메뉴\n" \
                                                                                              "중식 : "+lunch.replace(' ', ', ')+"\n" \
                                                                                                           "석식 : "+dinner.replace(' ', ', ')
                return return_data

        except Exception as e:
            return "second _" + str(e)