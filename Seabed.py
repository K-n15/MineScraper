import requests, re, os
from google import genai
from dotenv import load_dotenv
from bs4 import BeautifulSoup

load_dotenv()
Summarizer = genai.Client(api_key = os.getenv("AI_KEY"))

def spiderQuest(url):
    headers = {"User-Agent": "Mozilla/5.0 (X11; CrOS x86_64 12871.102.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.141 Safari/537.36"}
    response = requests.get(url,headers=headers,timeout=10)
    if response.status_code == 408 :
        return "REQUEST_TIMEOUT"
    elif  response.status_code == 504:
        return "GATEWAY_TIMEOUT"
    return response

def Conclude(context):
    text = "Summarize this in one paragraph:\n" + context
    try:
        result = Summarizer.models.generate_content(
            model="gemini-2.5-flash",
            contents=text
        )
    except Exception as e:
        return "Error : " + str(e)
    else:
        return result.text

def spider():
    BaseUrl = 'https://en.wikinews.org'

    latestNew = spiderQuest(BaseUrl+'/wiki/Main_Page')
    soupBase = BeautifulSoup(latestNew.text,'html.parser')

    FilterTitle = soupBase.find("div",{"id":"MainPage_latest_news_text","class":"latest_news_text"})

    FirstNews = FilterTitle.find('a')
    Topic = FirstNews.text
    Link = FirstNews['href']

    Detail = spiderQuest(BaseUrl+Link)
    stock = BeautifulSoup(Detail.text,'html.parser')

    FilterDetail = stock.find("div",{"id":"bodyContent"})
    published = stock.find("strong",{"class":"published"})
    context = ""
    for i in FilterDetail.find_all('p'):
        if i.find_parent(id = ['commentrequest','social_bookmarks']):
            continue
        context += i.text if i.getText().strip() else ""
    Conclude(context)

if __name__ == '__main__':
    spider()
