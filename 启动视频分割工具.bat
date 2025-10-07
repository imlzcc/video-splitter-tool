@echo off
title 视频分割工具
cd /d "%~dp0"
echo 正在启动视频分割工具...
python video_splitter_app.py
if errorlevel 1 (
    echo.
    echo 启动失败！请检查：
    echo 1. 是否安装了 Python
    echo 2. 是否安装了依赖包：pip install -r requirements.txt
    echo 3. 是否安装了 FFmpeg
    echo.
    pause
)
