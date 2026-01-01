import requests, os
from dotenv import load_dotenv
from bs4 import BeautifulSoup

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
    
    def Scavenge(self):
        x = self.Scavenging()
        return "OK" if x else x

    def LobsterQuest(self,url):
        headers = {"User-Agent": "Mozilla/5.0 (X11; CrOS x86_64 12871.102.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.141 Safari/537.36"}
        #2 retry chances
        exc,err = None,None
        for i in range(2):
            try:
                response = requests.get(url,headers=headers,timeout=10)
                status = response.status_code
                if status == 200:
                    return response
                else:
                    err = response
                    continue
            except Exception as e:
                exc = e
                continue
        return exc if err else err

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

    def Scavenging(self):
        latestNew = self.LobsterQuest(self.BaseUrl+'/wiki/Main_Page')
        if latestNew.status_code != 200:
            return "Error ["+str(latestNew.status_code)+"] : "+latestNew.text
        soupBase = BeautifulSoup(latestNew.text,'html.parser')

        FilterTitle = soupBase.find("div",{"id":"MainPage_latest_news_text","class":"latest_news_text"})
        FirstNews = FilterTitle.find('a')
        self.LatestTitle = FirstNews.text
        self.FullUrl = FirstNews['href']

        Detail = self.LobsterQuest(self.BaseUrl+self.FullUrl)
        if latestNew.status_code != 200:
            return "Error ["+str(Detail.status_code)+"] : "+Detail.text
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
