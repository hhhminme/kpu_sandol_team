import requests
import json
import datetime
from bs4 import BeautifulSoup
import settings


class LiveSubwayTraffic:
    def __init__(self, station_no=None) -> None:
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
                        self.return_data += i['headsign'] + " 방면 " + i['departureTime'] + ", " \
                                            + it.__next__()['departureTime'] + "\n"
                        flag = True
                        break
                    else:
                        continue

                if not flag:
                    self.return_data += schedule_data_up[-1]['headsign'] + schedule_data_up[-1][
                        'departureTime'] + " 막차입니다"

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

                if not flag:
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

                if not flag:
                    self.return_data += schedule_data_up[-1]['headsign'] + schedule_data_up[-1][
                        'departureTime'] + " 막차입니다"

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

                if not flag:
                    self.return_data += schedule_data_down[-1]['headsign'] + schedule_data_down[-1][
                        'departureTime'] + " 막차입니다"

        except Exception as e:
            return str(e)

    def get_time(self) -> dict:
        return settings.GEN.set_text(self.time)

    def get_string(self, time):
        self.time = datetime.datetime.strptime(time, '%H:%M:%S')  # time 모듈로 변환
        for subway in ["455", "11120"]:
            self.station_no = subway
            self.data = self.get_data()
            self.arrival_time()
        return settings.GEN.set_text(self.return_data)


class LastTraffic:  # 교통 관련 클래스
    def __init__(self):

        self.SUBWAY_URL = ["https://map.naver.com/v5/api/transit/subway/stations/455/schedule?lang=ko&stationID=455",
                           "https://map.naver.com/v5/api/transit/subway/stations/11120/schedule?lang=ko&stationID=11120"]

    def real_time_traffic(self):
        context = ''
        header = [f"{settings.IMOGE('emotion', 'walk')}4호선 막차시간입니다\n",
                  f"\n{settings.IMOGE('emotion', 'walk')}수인선 막차시간입니다\n"]
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
                    except Exception:
                        pass

                    try:
                        context += "".join(f"(휴일) {find_arrival_time_up2(find_weekend(arv))}\n")  # 휴일 시간이 있으면 시간 추가
                    except Exception:
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
            return settings.GEN.set_text(str(e))
        return settings.GEN.set_text(str(context[:-1]))


if __name__ == "__main__":
    print(LiveSubwayTraffic().get_string("12:13:30"))
    print(LastTraffic().real_time_traffic())
