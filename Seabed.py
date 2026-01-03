import requests, os
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from urllib3.util.retry import Retry

class Lobster:
    def __init__(self):
        self.BaseUrl = 'https://en.wikinews.org'
        self.LatestTitle = ""
        self.LastestRelease = ""
        self.LatestSums  = ""
        self.FullUrl = ""
        self.Scavenging()

    def getLatestNew(self):
        return self.LatestSums,self.FullUrl
    
    def getLastRelease(self):
        return self.LastestRelease
    
    def currentTitle(self):
        return self.LatestTitle
    
    def Scavenge(self):
        x = self.Scavenging()
        return "OK" if x else x

    def LobsterQuest(self,url):
        retry = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET"]
        )

        session = requests.Session()
        adapter = requests.adapters.HTTPAdapter(max_retries=retry)
        session.mount('https://', adapter)
        session.mount('http://', adapter)

        headers = {"User-Agent": "Mozilla/5.0 (X11; CrOS x86_64 12871.102.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.141 Safari/537.36"}
        try:
            response = requests.get(url,headers=headers,timeout=10)
            response.raise_for_status()
            return response, response.status_code
        except Exception as e:
            return f"{e}",500

    def Conclude(self,context):
        load_dotenv()
        try:
            API_KEY = os.environ.get("GEMINI_API_KEY") 
            MODEL = "gemini-2.5-flash"
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent"
            headers = { 
                "Content-Type": "application/json",
                "x-goog-api-key": API_KEY,
                }
            text = "Summarize this in one paragraph:\n" + context
            data = {
                "contents": [{
                    "parts": [{"text": text}]
                }]
            }
            response = requests.post(url, headers=headers, json=data, timeout=10)
            if response.status_code == 200:
                result = response.json()
                text = result['candidates'][0]['content']['parts'][0]['text']
                print("--- SUCCESS ---")
                return text
            else:
                print(f"--- API Error: {response.status_code} ---")
                print(response.text)
                return response.text

        except Exception as e:
            print(f"--- Network Failed: {e} ---")
            return "Error : " + str(e)
        
    def FirstNewDetail(self):
        latestNew,code = self.LobsterQuest(self.BaseUrl+'/wiki/Main_Page')
        if code != 200:
            return "Error ["+str(code)+"] : "+latestNew.text,code
        soupBase = BeautifulSoup(latestNew.text,'html.parser')

        FilterTitle = soupBase.find("div",{"id":"MainPage_latest_news_text","class":"latest_news_text"})
        FirstNews = FilterTitle.find('a')
        return FirstNews.text,code

    def Scavenging(self):
        latestNew,code = self.LobsterQuest(self.BaseUrl+'/wiki/Main_Page')
        if code != 200:
            return "Error ["+str(code)+"] : "+latestNew.text
        soupBase = BeautifulSoup(latestNew.text,'html.parser')

        FilterTitle = soupBase.find("div",{"id":"MainPage_latest_news_text","class":"latest_news_text"})
        FirstNews = FilterTitle.find('a')
        self.LatestTitle = FirstNews.text
        self.FullUrl = self.BaseUrl+FirstNews['href']
        routeUrl = FirstNews['href']

        Detail,code = self.LobsterQuest(self.BaseUrl+routeUrl)
        if code != 200:
            return "Error ["+str(code)+"] : "+Detail.text
        stock = BeautifulSoup(Detail.text,'html.parser')

        FilterDetail = stock.find("div",{"id":"bodyContent"})
        self.LastestRelease = stock.find("strong",{"class":"published"}).text
        context = ""
        for i in FilterDetail.find_all('p'):
            if i.find_parent(id = ['commentrequest','social_bookmarks']):
                continue
            context += i.text if i.getText().strip() else ""
        summarize = self.Conclude(context)
        print("Success")
        self.LatestSums  = self.LastestRelease + ' : ' + self.LatestTitle + '\n' + summarize


if __name__ == '__main__':
    seafood = Lobster()
    print(seafood.getLatestNew())
