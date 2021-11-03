import alphaSandol as settings
from bs4 import BeautifulSoup
import requests


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

        result = f"오늘 {location}의 날씨를 알려드릴게요!\n" \
                  f"오늘 날씨는{settings.IMOGE('weather', weather_info.strip())}{weather_info}이고,\n" \
                  f"기온은 {temp}C 으로 {compare_yesterday}\n"
        try:
            result += f"미세먼지는 {chart[0]}, \n"
        except:
            result += f"미세먼지는 -, \n"

        try:
            f"초미세먼지는 {chart[1]}이며, \n"
        except:
            f"초미세먼지는 -이며, \n"

        try:
            f"자외선은 {chart[2]} 입니다!"
        except:
            f"자외선은 - 입니다!"

        return settings.GEN.set_text(result)


if __name__ == "__main__":
    import json
    print(json.dumps(Weather().weather()))