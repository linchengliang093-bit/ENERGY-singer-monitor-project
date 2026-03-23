import os
import requests

class LineMessagingNotifier:
    def __init__(self, token=None, user_id=None):
        self.token = token or os.environ.get("LINE_CHANNEL_ACCESS_TOKEN")
        self.user_id = user_id or os.environ.get("LINE_USER_ID")
        self.api_url = "https://api.line.me/v2/bot/message/push"
        
    def send_message(self, message):
        """
        發送文字訊息至 Line Messaging API
        """
        if not self.token or not self.user_id:
            print("未設定 LINE_CHANNEL_ACCESS_TOKEN 或 LINE_USER_ID，跳過 Line 發送。")
            return False
            
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.token}"
        }
        data = {
            "to": self.user_id,
            "messages": [
                {
                    "type": "text",
                    "text": message
                }
            ]
        }
        
        try:
            response = requests.post(self.api_url, headers=headers, json=data)
            response.raise_for_status()
            return True
        except Exception as e:
            print(f"發送 Line Messaging API 通知失敗: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(e.response.text)
            return False

class TelegramNotifier:
    def __init__(self, token=None, chat_id=None):
        self.token = token or os.environ.get("TELEGRAM_BOT_TOKEN")
        self.chat_id = chat_id or os.environ.get("TELEGRAM_CHAT_ID")
        self.api_url_template = "https://api.telegram.org/bot{}/sendMessage"
        
    def send_message(self, message):
        """
        發送文字訊息至 Telegram
        """
        if not self.token or not self.chat_id:
            print("未設定 TELEGRAM_BOT_TOKEN 或 TELEGRAM_CHAT_ID，跳過發送。")
            return False
            
        api_url = self.api_url_template.format(self.token)
        data = {
            "chat_id": self.chat_id,
            "text": message
        }
        
        try:
            response = requests.post(api_url, data=data)
            response.raise_for_status()
            return True
        except Exception as e:
            print(f"發送 Telegram 通知失敗: {str(e)}")
            return False

if __name__ == "__main__":
    # 測試用
    # line_notifier = LineNotifier(token="YOUR_LINE_TOKEN")
    # line_notifier.send_message("這是一則 Line 測試通知")
    
    # tg_notifier = TelegramNotifier(token="YOUR_TG_TOKEN", chat_id="YOUR_TG_CHAT_ID")
    # tg_notifier.send_message("這是一則 Telegram 測試通知")
    pass
