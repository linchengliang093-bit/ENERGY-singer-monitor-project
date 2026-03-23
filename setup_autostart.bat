@echo off
chcp 65001 >nul
echo ========================================================
echo   台灣男團 Energy 監控系統 - 自動化排程設定工具
echo ========================================================
echo.
echo 此工具將會為您在 Windows 系統中建立一個「每日自動任務」。
echo 每天早上 09:00，系統會在背景悄悄為您抓取資料並產生最新報表。
echo.

set TASK_NAME=EnergySinger_DailyReport
set SCRIPT_PATH=%~dp0main.py
set WORKING_DIR=%~dp0

:: 嘗試自動將本資料夾設為執行路徑
schtasks /create /tn "%TASK_NAME%" /tr "cmd.exe /c cd /d \"%WORKING_DIR%\" && python main.py --now" /sc daily /st 09:00 /f

echo.
echo 設定完成！請確認上方有無 [成功: 已經成功建立排程工作] 的字樣。
echo 若日後想要取消自動產出，請至 Windows 搜尋「工作排程器」刪除即可。
pause
