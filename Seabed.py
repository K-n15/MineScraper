import requests
from bs4 import BeautifulSoup

def scrape(url=''):
    headers = {"User-Agent": "Mozilla/5.0 (X11; CrOS x86_64 12871.102.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.141 Safari/537.36"}
    response = requests.get(url,headers=headers,timeout=10)
    if response.status_code == 408 :
        return "REQUEST_TIMEOUT"
    elif  response.status_code == 504:
        return "GATEWAY_TIMEOUT"
    soup = BeautifulSoup(response.text, 'html.parser')
    sauce = soup.find("h1")
    cream = soup.find("p")
    spice = soup.find("a").get("href")
    print(sauce.text)
    print(cream.text)
    print(spice)
    print(soup.find('#start-of-content','id'))

if __name__ == '__main__':
    scrape('https://news.ycombinator.com/newest')