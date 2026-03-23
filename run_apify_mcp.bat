@echo off
chcp 65001 >nul
echo 正在準備啟動 Apify MCP Server...
echo ==============================================
echo 請確認您已經備妥 APIFY_TOKEN (可在 .env 檔案中設定)
echo.

npx -y @apify/mcp-server

pause
