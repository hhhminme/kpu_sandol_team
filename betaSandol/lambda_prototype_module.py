from bs4 import BeautifulSoup
import requests
import boto3
import random
import datetime
import json

imoge_mapping = {
    'emotion':{
        'paw' : 'πΎ',
        'smile' : 'πΊ',
        'happy' : 'πΈ',
        'sad' : 'πΉ',
        'love' : 'π»',
        'confident' : 'πΌ',
        'angry' : 'πΎ',
        'surprise' : 'π',
        'walk' : 'π',
        'nexpression' : 'π±'

    },
    'weather':{
        'νλ¦Ό' : 'β',
        'κ΅¬λ¦λ§μ' : 'β',
        'hvy_rain' : 'β',
        'λΉ' : 'β',
        'μ½κ°νλ¦Ό' : 'π€',
        'λ§μ' : 'β',
        'sun_wth_rain' : 'π¦',
        'thunder' : 'π©',
        'λ°λ' : 'πͺ',
        'μκ°' : 'π«'
    }
}
class CrawlingFunction():
    def subway(self, station):
        try:
            header = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36"}
            arrival_subway_api_url = "http://swopenapi.seoul.go.kr/api/subway/49664c636d6a68303634704d4f7649/json/realtimeStationArrival/0/5/" + station
            soup = requests.get(arrival_subway_api_url, headers=header)  # μ¬κΈ°κΉμ§ κΈ°λ³Έ ν¬λ‘€λ§ μ€λΉ

            if soup.status_code != 200:
                raise Exception('[Crawling-Error #001] API μλ²μ μ°κ²°μ μ€ν¨νμ΅λλ€ μ μν λ€μ μλν΄μ£ΌμΈμ'+ imoge_mapping['emotion']['sad'])

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
                    receptdata['realtimeArrivalList'][i]['barvlDt'])  # μ¬κΈ°κΉμ§ ν¬λ‘€λ§ ν λ΄μ©λ€ κΈ°μ€μΌλ‘ μλ°μ΄νΈ

            retn_str = reprocess['reqDate'] + "κΈ°μ€ " + station + " λμ°©μ λ³΄μλλ€"+ imoge_mapping['emotion']['walk']
            print(len(reprocess['arivlTime']))
            for i in range(len(reprocess['arivlTime'])):
                rept_str = str(i + 1) + ".\n[" + reprocess['heading'][i] + "] - " + "\n" + "λμ°© μμ  μκ° :" + \
                           reprocess['arivlTime'][i] + "μ΄ ν\n\n" + reprocess['subwayPos'][i] + "\n\n"
                retn_str += rept_str

            retn_str += imoge_mapping['emotion']['paw']+"μ€μ  μ΄μ°¨ λμ°© μκ°κ³Ό μμ΄ν  μ μμ΅λλ€.\n"+ imoge_mapping['emotion']['paw']+"APIμ λ¬Έμ λ‘ μΌλΆ μ­μμλ λμ°© μμ  μκ°μ΄ 0μ΄λ‘ νκΈ°λλ μ€λ₯κ° μμ μ μμ΅λλ€."

            return retn_str


        except Exception as e:
            return ("[Crawling_Error #002] νμ¬ μ΄μ°¨ μ΄ν μκ°μ΄ μλκ±°λ, API μλ²μμ ν΅μ μ μ€ν¨νμμ΅λλ€"+ imoge_mapping['emotion']['sad'])

    # def random_meal(self):
    #     s3 = boto3.resource('s3')
    #     bucket = s3.Bucket("sandol")
    #     try:
    #         local_file = "/tmp/" + "test.txt"
    #         bucket.download_file("tmp/test.txt", local_file)  # s3μμ νμΌμ λ€μ΄λ‘λ ν /tmpμ μ μ₯
    #
    #     except Exception as e:
    #         return str(e)
    #
    #     with open("/tmp/test.txt", "r", encoding='UTF-8') as rf:
    #         data = rf.readlines()  # νμΌμ μ λΆ μ½μ΄μ listλ‘ λ³ν
    #
    #     idx = random.randint(0, 100)
    #     result_string = data[idx]
    #     return "βλΉ λ°€β\n" + result_string.split("->")[0] + " μμ, " + result_string.split("->")[1].replace("\n",
    #                                                                                                     '') + " μ΄λ μΈμ?"

    def today_covid(self):
        try:
            url = 'https://m.search.naver.com/p/csearch/content/nqapirender.nhn?where=nexearch&pkid=9005&key=diffV2API'
            html = requests.get(url).text
            data = json.loads(html)
            return (data['result']['list'][-1]['date'] +"μΌκΉμ§ μ½λ‘λ λ°μ νν©μ΄μμ"+imoge_mapping['emotion']['walk']+"\n"+imoge_mapping['emotion']['paw']+"μ§μ­λ°μ : " + data['result']['list'][-1]['local'] +"λͺ\n" + imoge_mapping['emotion']['paw'] + "ν΄μΈμ μ : "+data['result']['list'][-1]['oversea']+"λͺ μλλ€!\nμ½λ‘λ μ‘°μ¬νμΈμ"+imoge_mapping['emotion']['nexpression'])

        except Exception as e:
            return "μ½λ‘λ νμ§μ μ λ³΄λ₯Ό λΆλ¬μ€λλ° μ€ν¨νμ΄μ" + imoge_mapping['emotion']['sad']

    def weather(self, location):
        local_code_dict = {'μλκΆ(μμΈ)': '109', 'λΆμ°': '11H20201', 'λκ΅¬': '11H10701', 'κ΄μ£Ό': '11F20501', 'μ μ£Ό': '11F10201',
                           'λμ ': '11C20401', 'μ²­μ£Ό': '11C10301', 'κ°μ': '105', 'μ μ£Ό': '11G00201', 'μμΈ': '11B10101',
                           'μΈμ²': '11B20201', 'μμ': '11B20601', 'μ±λ¨': '11B20605', 'μμ': '11B20602', 'κ΄λͺ': '11B10103',
                           'κ³Όμ²': '11B10102', 'νν': '11B20606', 'μ€μ°': '11B20603', 'μμ': '11B20609', 'μ©μΈ': '11B20612',
                           'κ΅°ν¬': '11B20610', 'μμ±': '11B20611', 'νμ±': '11B20604', 'μν': '11B20503', 'κ΅¬λ¦¬': '11B20501',
                           'λ¨μμ£Ό': '11B20502', 'νλ¨': '11B20504', 'μ΄μ²': '11B20701', 'μ¬μ£Ό': '11B20703', 'μμ λΆ': '11B20301',
                           'κ³ μ': '11B20302', 'νμ£Ό': '11B20305', 'μμ£Ό': '11B20304', 'λλμ²': '11B20401', 'μ°μ²': '11B20402',
                           'ν¬μ²': '11B20403', 'κ°ν': '11B20404', 'κ°ν': '11B20101', 'κΉν¬': '11B20102', 'μν₯': '11B20202',
                           'λΆμ²': '11B20204', 'μμ°': '11B20203', 'λ°±λ Ήλ': '11A00101', 'μΈμ°': '11H20101', 'κΉν΄': '11H20304',
                           'μμ°': '11H20102', 'μ°½μ': '11H20301', 'λ°μ': '11H20601', 'ν¨μ': '11H20603', 'μ°½λ': '11H20604',
                           'μλ Ή': '11H20602', 'μ§μ£Ό': '11H20701', 'νλ': '11H20704', 'μ¬μ²': '11H20402', 'κ±°μ°½': '11H20502',
                           'ν©μ²': '11H20503', 'μ°μ²­': '11H20703', 'ν¨μ': '11H20501', 'ν΅μ': '11H20401', 'κ±°μ ': '11H20403',
                           'κ³ μ±': '11D20402', 'λ¨ν΄': '11H20405', 'μμ²': '11H10702', 'κ²½μ°': '11H10703', 'μ²­λ': '11H10704',
                           'μΉ κ³‘': '11H10705', 'κΉμ²': '11H10601', 'κ΅¬λ―Έ': '11H10602', 'κ΅°μ': '11H10603', 'κ³ λ Ή': '11H10604',
                           'μ±μ£Ό': '11H10605', 'μλ': '11H10501', 'μμ±': '11H10502', 'μ²­μ‘': '11H10503', 'μμ£Ό': '11H10302',
                           'λ¬Έκ²½': '11H10301', 'μμ²': '11H10303', 'μμ£Ό': '11H10401', 'λ΄ν': '11H10402', 'μμ': '11H10403',
                           'μΈμ§': '11H10101', 'μλ': '11H10102', 'ν¬ν­': '11H10201', 'κ²½μ£Ό': '11H10202', 'μΈλ¦λ': '11E00101',
                           'λλ': '11E00102', 'λμ£Ό': '11F20503', 'μ₯μ±': '11F20502', 'λ΄μ': '11F20504', 'νμ': '11F20505',
                           'μκ΄': '21F20102', 'ν¨ν': '21F20101', 'λͺ©ν¬': '21F20801', 'λ¬΄μ': '21F20804', 'μμ': '21F20802',
                           'μ§λ': '21F20201', 'μ μ': '21F20803', 'νμ°λ': '11F20701', 'μμ²': '11F20603', 'μμ²μ': '11F20405',
                           'κ΄μ': '11F20402', 'κ΅¬λ‘': '11F20601', 'κ³‘μ±': '11F20602', 'μλ': '11F20301', 'κ°μ§': '11F20303',
                           'μ₯ν₯': '11F20304', 'ν΄λ¨': '11F20302', 'μ¬μ': '11F20401', 'κ³ ν₯': '11F20403', 'λ³΄μ±': '11F20404',
                           'μ΅μ°': '11F10202', 'κ΅°μ°': '21F10501', 'μ μ': '11F10203', 'κΉμ ': '21F10502', 'λ¨μ': '11F10401',
                           'κ³ μ°½': '21F10601', 'λ¬΄μ£Ό': '11F10302', 'λΆμ': '21F10602', 'μμ°½': '11F10403', 'μμ£Ό': '11F10204',
                           'μμ€': '11F10402', 'μ₯μ': '11F10301', 'μ§μ': '11F10303', 'μΈμ’': '11C20404', 'κ³΅μ£Ό': '11C20402',
                           'λΌμ°': '11C20602', 'κ³λ£‘': '11C20403', 'κΈμ°': '11C20601', 'μ²μ': '11C20301', 'μμ°': '11C20302',
                           'μμ°': '11C20303', 'μμ°': '11C20101', 'νμ': '11C20102', 'λΉμ§': '11C20103', 'νμ±': '11C20104',
                           'λ³΄λ Ή': '11C20201', 'μμ²': '11C20202', 'μ²­μ': '11C20502', 'λΆμ¬': '11C20501', 'μ¦ν': '11C10304',
                           'κ΄΄μ°': '11C10303', 'μ§μ²': '11C10102', 'μΆ©μ£Ό': '11C10101', 'μμ±': '11C10103', 'μ μ²': '11C10201',
                           'λ¨μ': '11C10202', 'λ³΄μ': '11C10302', 'μ₯μ²': '11C10403', 'μλ': '11C10402', 'μΆνλ Ή': '11C10401',
                           'μ² μ': '11D10101', 'νμ²': '11D10102', 'μΈμ ': '11D10201', 'μκ΅¬': '11D10202', 'μΆμ²': '11D10301',
                           'νμ²': '11D10302', 'μμ£Ό': '11D10401', 'ν‘μ±': '11D10402', 'μμ': '11D10501', 'μ μ ': '11D10502',
                           'νμ°½': '11D10503', 'λκ΄λ Ή': '11D20201', 'μμ΄': '11D20401', 'μμ': '11D20403', 'κ°λ¦': '11D20501',
                           'λν΄': '11D20601', 'μΌμ²': '11D20602', 'νλ°±': '11D20301', 'μκ·ν¬': '11G00401', 'μ±μ°': '11G00101',
                           'κ³ μ°': '11G00501', 'μ±νμ': '11G00302', 'μ΄μ΄λ': '11G00601', 'μΆμλ': '11G00800'}
        try:
            url = 'https://search.naver.com/search.naver?query=' + location + "λ μ¨"
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
            return location + "μ " + update_date + "μμ μλ°μ΄νΈ λ λ€μ΄λ² λ μ¨ μ λ³΄μλλ€!"+ imoge_mapping['emotion']['walk']+"\n\nκΈ°μ¨ : " + today_temp + "Β°C (" + today_temp_min + "C / " + today_temp_max + "C)\n" + weather_icon + today_weather + "\n\nλ―ΈμΈλ¨Όμ§ : " + today_dust10.replace("γ₯","γ₯, ") + "\nμ΄λ―ΈμΈλ¨Όμ§ : " + today_dust25.replace("γ₯","γ₯, ") + "\nμμΈμ  : " + today_temp_ray + "μ΄μμ! μ°Έκ³ νμΈμ"


        except Exception as e:
            try:
                local_code = local_code_dict[location]

            except Exception as e:
                return "[Crawling-Error #011] μ°Ύλ μ§μ­μ΄ μμ΅λλ€" + imoge_mapping['emotion']['paw'] + " 'μ' λλ 'λ'μ μ΄λ¦μ μλ ₯ν΄μ£ΌμΈμ! ex)μν₯ λ μ¨"  # μ΄ λΆλΆ μ€λ₯ λ©μμ§λ‘ λμ²΄νλ©΄ λ©λλ€

            url = "http://apis.data.go.kr/1360000/VilageFcstMsgService/getLandFcst?serviceKey=M733F8Tb2upYGqNeTgj0ArKYkqk%2Bbc1GtEhry7fELSoGf4WjvU1wLnWQmgd%2FEavkJGqc%2B23pay4r%2BeqfOnpRmA%3D%3D&pageNo=1&numOfRows=10&dataType=json&regId=" + local_code
            json_data = requests.get(url).text
            json_data = json.loads(json_data)
            form = json_data['response']['body']['items']['item']
            form = form[len(form) - 1]
            date = datetime.datetime.strptime(str(form['announceTime']), "%Y%m%d%H%M")
            date = str(date + datetime.timedelta(hours=5))
            temp = form['ta']
            wt = form['wf']

            return str(date) + "\nκΈ°μμ²­ λ μ¨ μ λ³΄μλλ€!"+ imoge_mapping['emotion']['walk']+"\nκΈ°μ¨ : " + str(temp) + "Β°C\nλ μ¨ : " + str(
                wt) + "\nλ―ΈμΈλ¨Όμ§ : -" + "\nμ΄λ―ΈμΈλ¨Όμ§ : -" + "\nμμΈμ  : -"


class s3IOEvent():
    def upload_feedback(self, params):  # νΌλλ°± μλ‘λ κΈ°λ₯
        s3 = boto3.resource('s3')
        bucket = s3.Bucket('sandol')  # μ΄ λΆλΆ ν΄λΉ λ²ν· μμ± ν μ μ ν μμ  μμ 
        params = "[" + str(datetime.datetime.today()) + "] :" + params + "\n"
        try:
            local_file = "/tmp/" + "feedback.txt"
            bucket.download_file("feedback.txt", local_file)
        except Exception as e:
            return "[File-Open-Error #101] μλ²μμ νΌλλ°± νμΌμ λΆλ¬μ€λ μ€ μ€λ₯κ° λ°μνμ΄μ"+ imoge_mapping['emotion']['sad']

        try:
            with open("/tmp/feedback.txt", "a", encoding="UTF-8") as f:
                f.writelines(params)
        except Exception as e:
            return "[File-Open-Error #102] νμΌμ μ μ₯ μ€ μ€λ₯κ° λ°μνμ΅λλ€" + imoge_mapping['emotion']['sad']

        try:
            s3 = boto3.client('s3')  # μ΄ λΆλΆ ν΄λΉ λ²ν· μμ± ν μ μ ν μμ  μμ 
            s3.upload_file("/tmp/feedback.txt", 'sandol', 'feedback.txt')

        except Exception as e:
            return "[File-Open-Error #103] νμΌμ μλ²μ μλ‘λ νλ μ€ μ€λ₯κ° λ°μνμ΅λλ€" + imoge_mapping['emotion']['sad']

        return "νΌλλ°± μ£Όμμ κ°μ¬ν΄μ! λΉ λ₯Έ μμΌλ΄μ κ²ν  ν μ μ©ν΄λ³Όκ²μ!" + imoge_mapping['emotion']['love']

    def read_feedback(self, params, bot_id):  # νΌλλ°± μ½κΈ° κΈ°λ₯ (κ΄λ¦¬μ μ μ©)
        sandol_team = ['d367f2ec55f41b4207156f4b8fce5ce885b05d8c3b238cf8861c55a9012f6f5895',
                       '339b0444bfabbffa0f13508ea7c45b61675b5720234cca8f73cd7421c22de9e546',
                       '04eabc8b965bf5ae6cccb122a18521969cc391162e3fd5f61b85efe8bb12e5e98a',
                       'def99464e022b38389697fe68d54bbba723d1da291094c19bbf5eaace7b059a997']

        if bot_id not in sandol_team:
            return "κΆνμ΄ μμ΅λλ€"
        if params == '1':  # μ½κΈ°
            s3 = boto3.resource('s3')
            bucket = s3.Bucket("sandol")

            try:
                local_file = "/tmp/" + "feedback.txt"
                bucket.download_file("feedback.txt", local_file)
            except Exception as e:
                return "[File-Open-Error #111] μλ²μμ νΌλλ°± νμΌμ λΆλ¬μ€λ μ€ μ€λ₯κ° λ°μνμ΄μ "

            try:
                with open("/tmp/feedback.txt", "r", encoding="UTF-8") as f:  # μ΄ λΆλΆ ν΄λΉ λ²ν· μμ± ν μ μ ν μμ  μμ 
                    txt = ''.join(f.readlines())
                    return txt

            except Exception as e:
                return "[File-Open-Error #112] νμΌμ μ½λ μ€ μ€λ₯κ° λ°μνμ΅λλ€"

        elif params == '2':  # μ§μ°κΈ°
            s3 = boto3.resource('s3')
            bucket = s3.Bucket('sandol')  # μ΄ λΆλΆ ν΄λΉ λ²ν· μμ± ν μ μ ν μμ  μμ 
            params = "#feedbacks\n"
            try:
                local_file = "/tmp/" + "feedback.txt"
                bucket.download_file("feedback.txt", local_file)
            except Exception as e:
                return "[File-Open-Error #113] μλ²μμ νΌλλ°± νμΌμ λΆλ¬μ€λ μ€ μ€λ₯κ° λ°μνμ΄μ"

            try:
                with open("/tmp/feedback.txt", "w", encoding="UTF-8") as f:  # μ΄ λΆλΆ ν΄λΉ λ²ν· μμ± ν μ μ ν μμ  μμ 
                    f.writelines(params)
            except Exception as e:
                return "[File-Open-Error #114] νμΌμ μ­μ  μ€ μ€λ₯κ° λ°μνμ΅λλ€"

            try:
                s3 = boto3.client('s3')
                s3.upload_file("/tmp/feedback.txt", 'sandol', 'feedback.txt')

            except Exception as e:
                return "[File-Open-Error #115] νμΌμ μλ²μ μλ‘λ νλ μ€ μ€λ₯κ° λ°μνμ΅λλ€"
            return "μ±κ³΅μ μΌλ‘ νμΌ λ΄μ©μ μ­μ νμ΅λλ€"


        else:  # param error
            return '[Param-Error #116] μλͺ»λ νλΌλ―Έν°'

    def upload_meal(self, store_name, lunch_list, dinner_list,input_date, owner_id):  # μμ¬ μλ‘λ κΈ°λ₯
        owner_id_dec = {'λ―Έκ°μλΉ': "32d8a05a91242ffb4c64b5630ec55953121dffd83a121d985e26e06e2c457197e6",
                        'μ°μ€νλ μ¬': "d367f2ec55f41b4207156f4b8fce5ce885b05d8c3b238cf8861c55a9012f6f5895",
                        'νΈλλΌμ΄μ§': "46f338132e6af63c32c07220c318f0e7c570e8eb6f375c9e8bb59ce33776f27c4c"
                        }
        sandol_team = ['d367f2ec55f41b4207156f4b8fce5ce885b05d8c3b238cf8861c55a9012f6f5895',
                       '339b0444bfabbffa0f13508ea7c45b61675b5720234cca8f73cd7421c22de9e546',
                       '04eabc8b965bf5ae6cccb122a18521969cc391162e3fd5f61b85efe8bb12e5e98a',
                       'def99464e022b38389697fe68d54bbba723d1da291094c19bbf5eaace7b059a997']

        if (owner_id_dec[store_name] != owner_id) and owner_id not in sandol_team:
            return "[Permission-Error #121-1] κΆνμ΄ μμ΅λλ€" + imoge_mapping['emotion']['angry']

        if store_name not in owner_id_dec.keys():
            return "[Not-Found-Error #121-2] ν΄λΉνλ μλΉμ΄ μμ΅λλ€."+ imoge_mapping['emotion']['sad']

        else:
            store_file = "restaurant_menu.txt"
            s3 = boto3.resource('s3')
            bucket = s3.Bucket("sandol")
            local_file = "/tmp/" + store_file

            try:
                # local_file = "./restaurant_menu/" + store_file
                s3.meta.client.download_file("sandol", "restaurant_menu.txt", '/tmp/restaurant_menu.txt')

            except Exception as e:
                return "[File-Open-Error #122] μ μ₯μμμ νμΌμ μ°Ύμ μ μμ΅λλ€."+ imoge_mapping['emotion']['sad']

            with open(local_file, "r", encoding="UTF-8") as f:
                try:
                    data = f.readlines()
                    print(data)
                    menu_info = data[data.index("πΎ"+store_name+"\n") + 1].replace('\'','').replace("\n","").split(", ") #λ΄λΆ λ°μ΄ν° μ²λ¦¬
                    menu_info[0] = input_date

                    menu_info[1] = lunch_list.replace(", ",",").replace(" ",",")
                    menu_info[2] = dinner_list.replace(",","").replace(" ",",") #λ©λ΄ μμ 

                    menu_info[1] = lunch_list.replace(" ",",")
                    menu_info[2] = dinner_list.replace(" ",",") #λ©λ΄ μμ 

                    menu_info[1] = lunch_list.replace(" ",",")
                    menu_info[2] = dinner_list.replace(" ",",") #λ©λ΄ μμ 

                    data[data.index("πΎ"+store_name+"\n") + 1] = str(menu_info)[1:-1] + "\n" #μ΅μ’ λ¬Έμμ΄
                    with open(local_file, "w", encoding='UTF-8') as rf:
                        rf.writelines(data)


                except Exception as e:
                    return "[File-Open-Error #123]νμΌμ μμ νλ μ€ μ€λ₯κ° λ°μνμ΅λλ€."+ imoge_mapping['emotion']['sad']
            try:
                s3 = boto3.client('s3')  # μ΄ λΆλΆ ν΄λΉ λ²ν· μμ± ν μ μ ν μμ  μμ 
                s3.upload_file(local_file, 'sandol', store_file)

            except Exception:
                return "[File-Open-Error #124]νμΌμ μ μ₯μμ μλ‘λνλ μ€ μ€λ₯κ° λ°μνμ΅λλ€."+ imoge_mapping['emotion']['sad']


        return "λ€! νμλ€μκ² μ μ λ¬ν κ²μ! κ°μ¬ν©λλ€!"+ imoge_mapping['emotion']['walk']

    def read_meal(self):
        store_file = "restaurant_menu.txt"
        s3 = boto3.resource('s3')  # μ΄ λΆλΆ ν΄λΉ λ²ν· μμ± ν μ μ ν μμ  μμ 
        bucket = s3.Bucket("sandol")
        try:
            local_file = "/tmp/" + store_file
            # local_file = "./restaurant_menu/" + store_file  #μ΄ λΆλΆ ν΄λΉ λ²ν· μμ± ν μ μ ν μμ  μμ 
            bucket.download_file(store_file, local_file)

        except Exception:
            return "[File-Open-Error #131] μ μ₯μμμ νμΌμ κ°μ Έμ€λλ° μ€ν¨νμ΅λλ€" + imoge_mapping['emotion']['sad'] # νμΌμ /tmp/μ λ³΅μ¬νμ¬ λ€μ΄λ‘λ

        try:
            t = ['μ', 'ν', 'μ', 'λͺ©', 'κΈ', 'ν ', 'μΌ']
            return_string = ''
            with open(local_file, "r", encoding='UTF-8') as f:
                data = f.readlines()
                for restaurant in range(0, len(data), 2):
                    menu_list = data[restaurant + 1].replace("\'", '').split(", ")
                    last_update_date = datetime.date.fromisoformat(menu_list[0])
                    return_string += (data[restaurant].replace("\n", '').replace("πΎ",imoge_mapping['emotion']['walk']) + " [" + str(last_update_date) + " " + t[last_update_date.weekday()] + "μμΌ]\n"+ imoge_mapping['emotion']['paw']+"μ€μ : " + menu_list[1] + "\n"+ imoge_mapping['emotion']['paw']+"μμ : " + menu_list[2] + "\n")

            additional_info = "\n"+imoge_mapping['emotion']['paw']+"λΆλμ΄νκ² λ©λ΄κ° λ³λλ  μ μμ΄μ!"\
                              +"\n"+imoge_mapping['emotion']['paw']+"μ£Όλ§μ νμκΈ°λ₯μ΄ μλνμ§ μμμ!"\
                              +"\n"+imoge_mapping['emotion']['paw']+"μΈλ―Έμ½ μλΉμ μμ£Όλμ μ¬μ μΌλ‘ μλ°μ΄νΈνμ§ λͺ»νκ³  μμ΄μ"+imoge_mapping['emotion']['sad']
            return_string += additional_info

            return return_string

        except Exception:
            return "[File-Open-Error #132] νμΌμ μ¬λ μ€ μ€λ₯κ° λ°μνμ΄μ.."+ imoge_mapping['emotion']['sad']

    def reset_meal(self, bot_id, date):
        sandol_team = ['d367f2ec55f41b4207156f4b8fce5ce885b05d8c3b238cf8861c55a9012f6f5895',
                       '339b0444bfabbffa0f13508ea7c45b61675b5720234cca8f73cd7421c22de9e546',
                       '04eabc8b965bf5ae6cccb122a18521969cc391162e3fd5f61b85efe8bb12e5e98a',
                       'def99464e022b38389697fe68d54bbba723d1da291094c19bbf5eaace7b059a997']
        if bot_id not in sandol_team:
            return "[Permission-Error #141] κΆνμ΄ μμ΅λλ€" + imoge_mapping['emotion']['angry']

        store_file = "restaurant_menu.txt"
        s3 = boto3.resource('s3')
        bucket = s3.Bucket("sandol")
        local_file = "/tmp/" + store_file

        try:
            # local_file = "./restaurant_menu/" + store_file
            s3.meta.client.download_file("sandol", "restaurant_menu.txt", '/tmp/restaurant_menu.txt')

        except Exception as e:
            return "[File-Open-Error #142] μ μ₯μμμ νμΌμ μ°Ύμ μ μμ΅λλ€."+ imoge_mapping['emotion']['sad']
        try:
            with open(local_file, "w", encoding="UTF-8") as f:
                rest_name = [imoge_mapping['emotion']['paw']+"λ―Έκ°μλΉ\n", imoge_mapping['emotion']['paw']+"μ°μ€νλ μ¬\n", imoge_mapping['emotion']['paw']+"νΈλλΌμ΄μ§\n"]

                return_string = ''
                for i in range (len(rest_name)):
                    return_string += rest_name[i] + "\'"+date+"\', \'μλ°μ΄νΈλμ§μμμ΅λλ€\', \'μλ°μ΄νΈλμ§μμμ΅λλ€\'\n"
                f.writelines(return_string)

        except Exception as e:
             return "[File-Open-Error #143]νμΌμ μμ νλ μ€ μ€λ₯κ° λ°μνμ΅λλ€."+ imoge_mapping['emotion']['sad']

        try:
            s3 = boto3.client('s3')  # μ΄ λΆλΆ ν΄λΉ λ²ν· μμ± ν μ μ ν μμ  μμ 
            s3.upload_file(local_file, 'sandol', store_file)

        except Exception:
            return "[File-Open-Error #144]νμΌμ μ μ₯μμ μλ‘λνλ μ€ μ€λ₯κ° λ°μνμ΅λλ€."+ imoge_mapping['emotion']['sad']
        return "νμΌμ μ μμ μΌλ‘ μ΄κΈ°ννμ΅λλ€" + imoge_mapping['emotion']['happy']