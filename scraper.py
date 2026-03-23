import os
import urllib.parse
import feedparser
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from tavily import TavilyClient

class NewsScraper:
    def __init__(self, keywords):
        self.keywords = keywords
        
    def fetch_google_news(self):
        """
        從 Google News RSS 取得包含目標關鍵字的新聞標題與連結
        """
        results = []
        for keyword in self.keywords:
            encoded_query = urllib.parse.quote(keyword)
            # 使用台灣地區的繁體中文新聞
            rss_url = f"https://news.google.com/rss/search?q={encoded_query}&hl=zh-TW&gl=TW&ceid=TW:zh-Hant"
            
            feed = feedparser.parse(rss_url)
            for entry in feed.entries[:10]: # 取前 10 則新聞
                # 解決 Google News redirect link 問題
                # 可以嘗試直接使用原始連結，或進一步拆解
                results.append({
                    "keyword": keyword,
                    "title": entry.title,
                    "link": entry.link,
                    "published": entry.published,
                    "source": entry.source.title if hasattr(entry, 'source') else "Unknown",
                    "type": "news"
                })
        return results

    def fetch_tavily_news(self):
        """
        使用 Tavily AI 搜尋引擎取得更深入的新聞與社群討論資訊
        """
        results = []
        tavily_api_key = os.environ.get("TAVILY_API_KEY")
        if not tavily_api_key:
            print("未設定 TAVILY_API_KEY，跳過 Tavily 搜尋。")
            return results
            
        try:
            client = TavilyClient(api_key=tavily_api_key)
            for keyword in self.keywords:
                # 執行搜尋，可設定特定網域來抓取社群討論，這裡為單純預設廣泛搜尋
                response = client.search(
                    query=keyword, 
                    search_depth="advanced", 
                    max_results=5
                )
                
                for item in response.get("results", []):
                    results.append({
                        "keyword": keyword,
                        "title": item.get("title", "無標題"),
                        "link": item.get("url", ""),
                        "published": "", 
                        "source": "Tavily AI",
                        "type": "tavily"
                    })
        except Exception as e:
            print(f"Tavily 搜尋發生錯誤: {str(e)}")
            
        return results

    def fetch_duckduckgo_news(self):
        """
        使用 DuckDuckGo 搜尋引擎作為免費的備援搜尋方案 (免 API Key)
        """
        results = []
        try:
            import warnings
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", RuntimeWarning)
                from duckduckgo_search import DDGS
            with DDGS() as ddgs:
                for keyword in self.keywords:
                    # 搜尋新聞，限制筆數避免過度頻繁請求
                    ddg_news = ddgs.news(keyword, max_results=5)
                    if ddg_news:
                        for item in ddg_news:
                            results.append({
                                "keyword": keyword,
                                "title": item.get("title", "無標題"),
                                "link": item.get("url", ""),
                                "published": item.get("date", ""),
                                "source": item.get("source", "DuckDuckGo"),
                                "type": "duckduckgo"
                            })
        except Exception as e:
            print(f"DuckDuckGo 搜尋發生錯誤: {str(e)}")
            
        return results

    def extract_content(self, url):
        """
        (選用) 根據 URL 爬取新聞內文的簡單實作
        """
        try:
            # 加入 User-Agent 避免被阻擋
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            }
            response = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            # 簡單抓取所有的 p 標籤作為內文
            paragraphs = soup.find_all('p')
            content = " ".join([p.get_text().strip() for p in paragraphs])
            return content[:500] + "..." if len(content) > 500 else content
        except Exception as e:
            return f"無法擷取內文: {str(e)}"

# 簡單測試用
if __name__ == "__main__":
    scraper = NewsScraper(["Energy 男團", "Energy 演唱會"])
    news = scraper.fetch_google_news()
    for item in news[:3]:
        print(f"[{item['source']}] {item['title']}\n連結: {item['link']}\n")
