#-*- coding:utf-8 -*-
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
            soup = requests.get(arrival_subway_api_url, headers=header)  # 여기까지 기본 크롤링 준비

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
                reprocess['arivlTime'].append(
                    receptdata['realtimeArrivalList'][i]['barvlDt'])  # 여기까지 크롤링 한 내용들 기준으로 업데이트

            retn_str = "-------------------------------------------------\n" + \
                       reprocess['reqDate'] + "기준 " + station + " 도착정보입니다\n" + \
                       "-------------------------------------------------\n"
            print(len(reprocess['arivlTime']))
            for i in range(len(reprocess['arivlTime'])):
                rept_str = str(i + 1) + ".\n[" + reprocess['heading'][i] + "] - " + "\n" + "도착 예정 시각 :" + \
                           reprocess['arivlTime'][i] + "초 후\n\n" + reprocess['subwayPos'][i] + "\n\n"
                retn_str += rept_str

            retn_str += "*실제 열차 도착 시간과 상이할 수 있습니다.\n" \
                        "*API의 문제로 일부 역에서는 도착 예정 시간이 0초로 표기되는 오류가 있을 수 있습니다."

            return retn_str


        except Exception as e:
            return ("[" + str(e) + "] 현재 열차 운행 시간이 아니거나, API 서버와의 통신에 실패하였습니다")

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
    #                                                                                                     '') + " 어떠세요?"

    def weather(self, location):

        local_code_dict = {'수도권(서울)': '109', '부산': '11H20201', '대구': '11H10701', '광주': '11F20501', '전주': '11F10201',
                           '대전': '11C20401', '청주': '11C10301', '강원': '105', '제주': '11G00201', '서울': '11B10101',
                           '인천': '11B20201', '수원': '11B20601', '성남': '11B20605', '안양': '11B20602', '광명': '11B10103',
                           '과천': '11B10102', '평택': '11B20606', '오산': '11B20603', '의왕': '11B20609', '용인': '11B20612',
                           '군포': '11B20610', '안성': '11B20611', '화성': '11B20604', '양평': '11B20503', '구리': '11B20501',
                           '남양주': '11B20502', '하남': '11B20504', '이천': '11B20701', '여주': '11B20703', '의정부': '11B20301',
                           '고양': '11B20302', '파주': '11B20305', '양주': '11B20304', '동두천': '11B20401', '연천': '11B20402',
                           '포천': '11B20403', '가평': '11B20404', '강화': '11B20101', '김포': '11B20102', '시흥': '11B20202',
                           '부천': '11B20204', '안산': '11B20203', '백령도': '11A00101', '울산': '11H20101', '김해': '11H20304',
                           '양산': '11H20102', '창원': '11H20301', '밀양': '11H20601', '함안': '11H20603', '창녕': '11H20604',
                           '의령': '11H20602', '진주': '11H20701', '하동': '11H20704', '사천': '11H20402', '거창': '11H20502',
                           '합천': '11H20503', '산청': '11H20703', '함양': '11H20501', '통영': '11H20401', '거제': '11H20403',
                           '고성': '11D20402', '남해': '11H20405', '영천': '11H10702', '경산': '11H10703', '청도': '11H10704',
                           '칠곡': '11H10705', '김천': '11H10601', '구미': '11H10602', '군위': '11H10603', '고령': '11H10604',
                           '성주': '11H10605', '안동': '11H10501', '의성': '11H10502', '청송': '11H10503', '상주': '11H10302',
                           '문경': '11H10301', '예천': '11H10303', '영주': '11H10401', '봉화': '11H10402', '영양': '11H10403',
                           '울진': '11H10101', '영덕': '11H10102', '포항': '11H10201', '경주': '11H10202', '울릉도': '11E00101',
                           '독도': '11E00102', '나주': '11F20503', '장성': '11F20502', '담양': '11F20504', '화순': '11F20505',
                           '영광': '21F20102', '함평': '21F20101', '목포': '21F20801', '무안': '21F20804', '영암': '21F20802',
                           '진도': '21F20201', '신안': '21F20803', '흑산도': '11F20701', '순천': '11F20603', '순천시': '11F20405',
                           '광양': '11F20402', '구례': '11F20601', '곡성': '11F20602', '완도': '11F20301', '강진': '11F20303',
                           '장흥': '11F20304', '해남': '11F20302', '여수': '11F20401', '고흥': '11F20403', '보성': '11F20404',
                           '익산': '11F10202', '군산': '21F10501', '정읍': '11F10203', '김제': '21F10502', '남원': '11F10401',
                           '고창': '21F10601', '무주': '11F10302', '부안': '21F10602', '순창': '11F10403', '완주': '11F10204',
                           '임실': '11F10402', '장수': '11F10301', '진안': '11F10303', '세종': '11C20404', '공주': '11C20402',
                           '논산': '11C20602', '계룡': '11C20403', '금산': '11C20601', '천안': '11C20301', '아산': '11C20302',
                           '예산': '11C20303', '서산': '11C20101', '태안': '11C20102', '당진': '11C20103', '홍성': '11C20104',
                           '보령': '11C20201', '서천': '11C20202', '청양': '11C20502', '부여': '11C20501', '증평': '11C10304',
                           '괴산': '11C10303', '진천': '11C10102', '충주': '11C10101', '음성': '11C10103', '제천': '11C10201',
                           '단양': '11C10202', '보은': '11C10302', '옥천': '11C10403', '영동': '11C10402', '추풍령': '11C10401',
                           '철원': '11D10101', '화천': '11D10102', '인제': '11D10201', '양구': '11D10202', '춘천': '11D10301',
                           '홍천': '11D10302', '원주': '11D10401', '횡성': '11D10402', '영월': '11D10501', '정선': '11D10502',
                           '평창': '11D10503', '대관령': '11D20201', '속초': '11D20401', '양양': '11D20403', '강릉': '11D20501',
                           '동해': '11D20601', '삼척': '11D20602', '태백': '11D20301', '서귀포': '11G00401', '성산': '11G00101',
                           '고산': '11G00501', '성판악': '11G00302', '이어도': '11G00601', '추자도': '11G00800'}
        try:
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

            return location + "의 " + update_date + "시에 업데이트 된 네이버 날씨 정보입니다!\n기온 : " + today_temp + "°C\n최저기온 : " + today_temp_min + "C\n최고 기온 : " + today_temp_max + "C\n날씨 : " + today_weather + "\n미세먼지 : " + today_dust10 + "\n초미세먼지 : " + today_dust25 + "\n자외선 : " + today_temp_ray + "\n이에요! 참고하세요"


        except Exception as e:
            print(e)
            try:
                local_code = local_code_dict[location]

            except Exception as e:

                return "찾는 지역이 없습니다, '시' 또는 '도'의 이름을 입력해주세요! ex)시흥 날씨"  # 이 부분 오류 메시지로 대체하면 됩니다

            url = "http://apis.data.go.kr/1360000/VilageFcstMsgService/getLandFcst?serviceKey=M733F8Tb2upYGqNeTgj0ArKYkqk%2Bbc1GtEhry7fELSoGf4WjvU1wLnWQmgd%2FEavkJGqc%2B23pay4r%2BeqfOnpRmA%3D%3D&pageNo=1&numOfRows=10&dataType=json&regId=" + local_code
            json_data = requests.get(url).text
            json_data = json.loads(json_data)
            form = json_data['response']['body']['items']['item']
            form = form[len(form) - 1]
            date = datetime.datetime.strptime(str(form['announceTime']), "%Y%m%d%H%M")
            date = str(date + datetime.timedelta(hours=5))
            temp = form['ta']
            wt = form['wf']

            return str(date) + "\n기상청 날씨 정보입니다!\n기온 : " + str(temp) + "°C\n날씨 : " + str(
                wt) + "\n미세먼지 : -" + "\n초미세먼지 : -" + "\n자외선 : -"


class s3IOEvent():
    def upload_feedback(self, params):  # 피드백 업로드 기능
        s3 = boto3.resource('s3')
        bucket = s3.Bucket('sandol')  # 이 부분 해당 버킷 생성 후 적절히 수정 예정
        params = "[" + str(datetime.datetime.today()) + "] :" + params + "\n"
        try:
            local_file = "/tmp/" + "feedback.txt"
            bucket.download_file("feedback.txt", local_file)
        except Exception as e:
            return "서버에서 피드백 파일을 불러오는 중 오류가 발생했어요 [Errno 1]"

        try:
            with open("/tmp/feedback.txt", "a", encoding="UTF-8") as f:
                f.writelines(params)
        except Exception as e:
            return "파일을 저장 중 오류가 발생했습니다 [Errno 2]"

        try:
            s3 = boto3.client('s3')  # 이 부분 해당 버킷 생성 후 적절히 수정 예정
            s3.upload_file("/tmp/feedback.txt", 'sandol', 'feedback.txt')

        except Exception as e:
            return "파일을 서버에 업로드 하는 중 오류가 발생했습니다 [Errno 3]"

        return "피드백 주셔서 감사해요! 빠른 시일내에 검토 후 적용해볼게요!"

    def read_feedback(self, params):  # 피드백 읽기 기능 (관리자 전용)
        if params == '1':  # 읽기
            s3 = boto3.resource('s3')
            bucket = s3.Bucket("sandol")

            try:
                local_file = "/tmp/" + "feedback.txt"
                bucket.download_file("feedback.txt", local_file)
            except Exception as e:
                return "서버에서 피드백 파일을 불러오는 중 오류가 발생했어요 [Errno 1]" + str(e)

            try:
                with open("/tmp/feedback.txt", "r", encoding="UTF-8") as f:  # 이 부분 해당 버킷 생성 후 적절히 수정 예정
                    txt = ''.join(f.readlines())
                    return txt

            except Exception as e:
                return "파일을 읽는 중 오류가 발생했습니다 [Errno 2]" + str(e)

        elif params == '2':  # 지우기
            s3 = boto3.resource('s3')
            bucket = s3.Bucket('sandol')  # 이 부분 해당 버킷 생성 후 적절히 수정 예정
            params = "#feedbacks\n"
            try:
                local_file = "/tmp/" + "feedback.txt"
                bucket.download_file("feedback.txt", local_file)
            except Exception as e:
                return "서버에서 피드백 파일을 불러오는 중 오류가 발생했어요 [Errno 1]"

            try:
                with open("/tmp/feedback.txt", "w", encoding="UTF-8") as f:  # 이 부분 해당 버킷 생성 후 적절히 수정 예정
                    f.writelines(params)
            except Exception as e:
                return "파일을 삭제 중 오류가 발생했습니다 [Errno 2]"

            try:
                s3 = boto3.client('s3')
                s3.upload_file("/tmp/feedback.txt", 'sandol', 'feedback.txt')

            except Exception as e:
                return "파일을 서버에 업로드 하는 중 오류가 발생했습니다 [Errno 3]"
            return "성공적으로 파일 내용을 삭제했습니다"


        else:  # param error
            return '잘못된 파라미터'

    def upload_meal(self, store_name, lunch_list, dinner_list,input_date, owner_id):  # 식사 업로드 기능
        owner_id_dec = {'미가식당': "32d8a05a91242ffb4c64b5630ec55953121dffd83a121d985e26e06e2c457197e6",
                        '웰스프레쉬': "d367f2ec55f41b4207156f4b8fce5ce885b05d8c3b238cf8861c55a9012f6f5895",
                        '푸드라운지': "d367f2ec55f41b4207156f4b8fce5ce885b05d8c3b238cf8861c55a9012f6f5895"
                        }
        sandol_team = ['d367f2ec55f41b4207156f4b8fce5ce885b05d8c3b238cf8861c55a9012f6f5895',
                       '339b0444bfabbffa0f13508ea7c45b61675b5720234cca8f73cd7421c22de9e546']

        print (owner_id_dec[store_name] != owner_id, owner_id not in sandol_team)
        if (owner_id_dec[store_name] != owner_id) and owner_id not in sandol_team:
            return "권한이 없습니다"

        if store_name not in owner_id_dec.keys():
            return "해당하는 식당이 없습니다."

        else:
            store_file = store_name + ".txt"  # 이 부분 해당 버킷 생성 후 적절히 수정 예정
            store_file = store_file.
            s3 = boto3.resource('s3')
            bucket = s3.Bucket("sandol")

            try:
                local_file = "/tmp/" + store_file
                # local_file = "./restaurant_menu/" + store_file

                bucket.download_file(store_file, local_file)  # 이 부분 해당 버킷 생성 후 적절히 수정 예정

            except Exception as e:
                return "저장소에서 파일을 찾을 수 없습니다." +str(e)  # 파일을 /tmp/에 복사하여 다운로드

            try:
                modified_data = input_date + "\n중식 : " + lunch_list + "\n석식 : " + dinner_list
                with open(local_file, "w", encoding="UTF-8") as f:
                    f.writelines(modified_data)

            except Exception:
                return "파일을 수정하는 중 오류가 발생했습니다."

            try:
                s3 = boto3.client('s3')  # 이 부분 해당 버킷 생성 후 적절히 수정 예정
                s3.upload_file(local_file, 'sandol', store_file)

            except Exception:
                return "파일을 저장소에 업로드하는 중 오류가 발생했습니다."

        return "네! 학생들에게 잘 전달할게요! 감사합니다!"

    def read_meal(self, store_name):
        t = ['월', '화', '수', '목', '금', '토', '일']
        store_file = store_name + ".txt"
        s3 = boto3.resource('s3')  # 이 부분 해당 버킷 생성 후 적절히 수정 예정
        bucket = s3.Bucket("sandol")
        try:
            local_file = "/tmp/" + store_file
            # local_file = "./restaurant_menu/" + store_file  #이 부분 해당 버킷 생성 후 적절히 수정 예정
            bucket.download_file(store_file, local_file)

        except Exception:
            return "저장소에서 파일을 가져오는데 실패했습니다"  # 파일을 /tmp/에 복사하여 다운로드

        try:
            with open(local_file, "r", encoding="UTF-8") as f:
                data = f.readlines()
                date = data[0].replace("\n", '')
                lunch = data[1].split(" : ")[1].replace("\n", '')
                dinner = data[2].split(" : ")[1].replace("\n", '')
                return_data = "[" + date + " " + t[datetime.datetime.today().weekday()] + "요일] " + store_name + "메뉴\n", "중식 : " + lunch.replace(
                    ' ', ', ') + "\n" \
                                 "석식 : " + dinner.replace(' ', ', ')
                return return_data

        except Exception:
            return "파일을 여는 중 오류가 발생했습니다."
#print (s3IOEvent.upload_meal(s3IOEvent, "미가식당","ㅁ ㅁㄴ ㅇㄹ", "ㅇ ㄹㅇ ㄹㄴ","2021-03-29", "32d8a05a91242ffb4c64b5630ec55953121dffd83a121d985e26e06e2c457197e6"))