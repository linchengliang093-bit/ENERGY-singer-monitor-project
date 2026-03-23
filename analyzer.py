import os
from google import genai
from google.genai import types

class DataAnalyzer:
    def __init__(self, api_key=None):
        # 如果沒有傳入 api_key，會嘗試從環境變數 GEMINI_API_KEY 取得
        self.client = genai.Client(api_key=api_key or os.environ.get("GEMINI_API_KEY"))

    def analyze_news(self, news_items):
        """
        接收新聞列表，並使用 Gemini 生成總結報告
        """
        if not news_items:
            return "無爬取到任何相關新聞。"

        # 組合所有的標題作為分析素材
        content_to_analyze = "\n".join([f"- {item['title']} (來源: {item['source']})" for item in news_items])
        
        prompt = f"""
        你是一位專業的品牌與社群監控分析師。請根據以下蒐集到的最新新聞標題，為我撰寫一份簡短的總結報告。
        監控目標：台灣男團 Energy 最新動態與輿情。
        
        請包含以下內容：
        1. 整體輿情摘要（用幾句話總結大家在討論什麼）
        2. 情緒分析（整體為正向、負向或中立）
        3. 條列式列出前三大重要資訊或活動情報
        
        新聞原始資料：
        {content_to_analyze}
        """

        try:
            # 預設使用 gemini-2.5-flash 作為基礎快速分析，或依設定調整
            response = self.client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt,
            )
            return response.text
        except Exception as e:
            return f"LLM 分析發生錯誤: {str(e)}"

# 簡單測試
if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv() # 確保讀取 .env 中的 GEMINI_API_KEY
    
    # 測試用假資料
    dummy_news = [
        {"title": "Energy 睽違多年合體！小巨蛋演唱會秒殺", "source": "娛樂新聞網"},
        {"title": "Energy 復出主打歌〈星期五晚上〉洗腦神曲，網紅爭相模仿", "source": "社群報"},
        {"title": "有網友抱怨 Energy 演唱會黃牛票太過猖獗", "source": "批踢踢實業坊"}
    ]
    
    analyzer = DataAnalyzer()
    print("分析結果：\n" + analyzer.analyze_news(dummy_news))
