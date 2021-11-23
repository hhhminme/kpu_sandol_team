import requests
from bs4 import BeautifulSoup
import settings


class Announcement:
    def __init__(self):
        self.URL = "https://www.kpu.ac.kr/front/boardlist.do?bbsConfigFK=1&siteGubun=14&menuGubun=1"
        self.ORIGIN = "https://www.kpu.ac.kr"
        self.TITLE = "교내 최신 학사공지 내역입니다"
        self.MAX_ANNOUNCEMENT_CNT = 5  # 최대 가져올 공지 수
        self.WEB_LINK_URL = "https://www.kpu.ac.kr/contents/main/cor/noticehaksa.html"

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

            return settings.GEN.set_list(self.TITLE, result,
                                         is_Button=settings.GEN_OPTION.button(label="바로가기", action="webLink",
                                                                              webLinkUrl=self.WEB_LINK_URL))

        except Exception as e:
            return settings.GEN.set_text(f"{e}")


if __name__ == "__main__":
    print(Announcement().announce())