import os
from datetime import datetime

class ReportGenerator:
    def __init__(self, template_path="template.html"):
        self.template_path = template_path
        
    def generate_html(self, analysis_text, news_items, output_filename=None):
        """
        將分析結果與新聞列表帶入 HTML 樣板中。
        為求簡化，此處先使用簡單的字串替換，亦可後續改用 Jinja2
        """
        if not output_filename:
            date_str = datetime.now().strftime("%Y-%m-%d")
            output_filename = f"report_{date_str}.html"
            
        # 建立新聞清單的 HTML
        news_html = ""
        for item in news_items:
            news_html += f"<li><a href='{item['link']}' target='_blank'>[{item['source']}] {item['title']}</a></li>\n"
            
        # 簡單的 HTML 版型
        html_content = f"""
        <!DOCTYPE html>
        <html lang="zh-TW">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>台灣男團 Energy 每日監控分析報告</title>
            <style>
                body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; color: #333; max-width: 800px; margin: 0 auto; padding: 20px; background-color: #f4f7f6; }}
                .container {{ background-color: #fff; padding: 30px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }}
                h1 {{ color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px; }}
                h2 {{ color: #2980b9; margin-top: 30px; }}
                .summary {{ background-color: #e8f4f8; padding: 20px; border-left: 4px solid #3498db; border-radius: 4px; white-space: pre-wrap; }}
                ul {{ padding-left: 20px; }}
                li {{ margin-bottom: 15px; }}
                a {{ color: #3498db; text-decoration: none; }}
                a:hover {{ text-decoration: underline; }}
                .footer {{ text-align: center; margin-top: 40px; font-size: 0.9em; color: #7f8c8d; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>台灣男團 Energy 每日監控報告</h1>
                <p><strong>產出時間:</strong> {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
                
                <h2>AI 輿情與情緒分析摘要</h2>
                <div class="summary">
{analysis_text}
                </div>
                
                <h2>最新情報與新聞列表</h2>
                <ul>
{news_html}
                </ul>
                
                <div class="footer">
                    <p>自動化系統生成 • 亨通電腦股份有限公司 技術顧問開發</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        with open(output_filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
            
        return output_filename

if __name__ == "__main__":
    # 測試用
    generator = ReportGenerator()
    generator.generate_html("這是一段測試摘要。\n整體呈現正向情緒。", [{"title": "測試新聞", "link": "http://example.com", "source": "測試來源"}])
    print("HTML 報告已生成。")
