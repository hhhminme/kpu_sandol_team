import settings
from bs4 import BeautifulSoup
import requests
import datetime


class Weather:
    def __init__(self):
        self.URL = r"https://weather.naver.com/today/02390132"

    def weather(self, location: str = "정왕") -> dict:
        soup = BeautifulSoup(requests.get(self.URL).text, 'html.parser')
        weather_box = soup.select('#content > div > div.section_center > div.card.card_today > div.today_weather > div.weather_area')[0]
        today = weather_box.find('p', {'class': 'summary'}).text.replace('\n', '  ').strip().split('  ')    # 날씨, 어제와 비교
        today_date = weather_box.find('i', {'class': 'ico_animation _cnLazy'})['data-ymdt']
        dates = datetime.datetime.strptime(today_date, '%Y%m%d%H')
        result = f"{dates}기준 정왕 날씨입니다\n현재날씨는 {today[0]}이고, {today[1]}"
        return settings.GEN.set_text(result)


if __name__ == "__main__":
    print(Weather().weather())