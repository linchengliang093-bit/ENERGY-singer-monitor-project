import os
import time
import schedule
from dotenv import load_dotenv

from scraper import NewsScraper
from analyzer import DataAnalyzer
from report_generator import ReportGenerator
from notifier import TelegramNotifier, LineMessagingNotifier

def job():
    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 開始執行 台灣男團 Energy 自動化監控...")
    
    # 載入環境變數設定
    load_dotenv()
    
    # 設定監控關鍵字
    keywords = ["Energy 男團", "Energy 演唱會", "坤達 書偉 Energy", "Energy 小巨蛋"]
    
    # 1. 資料搜集
    print("正在搜集 Google News 資訊...")
    scraper = NewsScraper(keywords)
    google_news_items = scraper.fetch_google_news()
    
    print("正在透過 Tavily AI 進行深度搜尋...")
    tavily_news_items = scraper.fetch_tavily_news()
    
    print("正在透過 DuckDuckGo 進行備援搜尋...")
    ddg_news_items = scraper.fetch_duckduckgo_news()
    
    # 合併三邊的結果
    news_items = google_news_items + tavily_news_items + ddg_news_items
    
    # 2. 資料分析
    print(f"共抓取 {len(news_items)} 則新聞，正在進行 AI 摘要分析...")
    # 若需傳遞 key, DataAnalyzer(api_key="your_key")，不傳則預設找環境變數 GEMINI_API_KEY
    analyzer = DataAnalyzer()
    analysis_text = analyzer.analyze_news(news_items)
    
    # 3. 報告生成
    print("正在產生 HTML 報表...")
    generator = ReportGenerator()
    html_filename = generator.generate_html(analysis_text, news_items)
    print(f"報表已儲存至: {html_filename}")
    
    # 4. 通知發送
    # 通知中可以附上摘要及檔案位置或直接提供網頁公開連結
    msg = f"\n林董您好，今日 台灣男團 Energy 監控報告已產生。\n\n【重點摘要】\n{analysis_text[:200]}...\n\n詳細報表路徑： {os.path.abspath(html_filename)}"
    
    # Line 通知 (Messaging API)
    line_notifier = LineMessagingNotifier()
    if os.environ.get("LINE_CHANNEL_ACCESS_TOKEN") and os.environ.get("LINE_USER_ID"):
        print("正在發送 Line 通知...")
        line_notifier.send_message(msg)
    else:
        print("尚未設定 LINE_CHANNEL_ACCESS_TOKEN 或 LINE_USER_ID，跳過 Line 通知。")
    
    # Telegram 通知
    tg_notifier = TelegramNotifier()
    if os.environ.get("TELEGRAM_BOT_TOKEN") and os.environ.get("TELEGRAM_CHAT_ID"):
        print("正在發送 Telegram 通知...")
        tg_notifier.send_message(msg)
    else:
        print("尚未設定 TELEGRAM_BOT_TOKEN 或 TELEGRAM_CHAT_ID，跳過 Telegram 通知。")
        
    print("=== 今日任務執行完畢 ===")

def main():
    import argparse
    parser = argparse.ArgumentParser(description="台灣男團 Energy 監控系統")
    parser.add_argument("--now", action="store_true", help="立即執行一次")
    parser.add_argument("--schedule", action="store_true", help="啟動每日 9:00 定時執行")
    args = parser.parse_args()
    
    if args.now:
        job()
    elif args.schedule:
        print("啟動定時服務中... 每日 09:00 執行。")
        schedule.every().day.at("09:00").do(job)
        while True:
            schedule.run_pending()
            time.sleep(60)
    else:
        # 如果沒有帶參數，預設執行一次
        job()

if __name__ == "__main__":
    main()
