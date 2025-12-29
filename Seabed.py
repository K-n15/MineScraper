import requests
from bs4 import BeautifulSoup

class Lobster():
    def __init__(self):
        self.ThaiNews = "https://www.bangkokpost.com/sitemap/sitemap_thailand.xml"
        self.WorldNews = "https://www.bangkokpost.com/sitemap/sitemap_world.xml"
        self.headers = {"User-Agent": "Mozilla/5.0 (X11; CrOS x86_64 12871.102.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.141 Safari/537.36"}
        self.LastUpdate = ""

    # def scrape_thaiNews(self,topic):

    
    # def scrape_WolrdNews(self,topic):

    def CoralLayout(self):
        url = 'https://www.bangkokpost.com/sitemap.xml'
        response = requests.get(url,headers=self.headers,timeout=10)
        if response.status_code == 408 :
            return "REQUEST_TIMEOUT"
        elif  response.status_code == 504:
            return "GATEWAY_TIMEOUT"
        filtering_result = BeautifulSoup(response.text,"xml")
        RecentUpdate = filtering_result.find('lastmod')
        # if RecentUpdate != self.LastUpdate:


def scrape(url='https://www.bangkokpost.com/sitemap/sitemap_world.xml'):
    headers = {"User-Agent": "Mozilla/5.0 (X11; CrOS x86_64 12871.102.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.141 Safari/537.36"}
    response = requests.get(url,headers=headers,timeout=10)
    if response.status_code == 408 :
        return "REQUEST_TIMEOUT"
    elif  response.status_code == 504:
        return "GATEWAY_TIMEOUT"
    file = BeautifulSoup(response.text,"xml")
    # soup = BeautifulSoup(response.text, 'html.parser')
    # tree = ET.parse(soup)
    titles = file.find_all('url')
    link = []
    for i in titles:
        src = i.find('loc')
        if src:
            link.append(src.text)
    for i in link:
        print(i)
    
if __name__ == '__main__':
    scrape() 