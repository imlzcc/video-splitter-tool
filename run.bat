@echo off
echo 视频批量分割工具
echo ================

REM 检查 Python 是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误: 未找到 Python，请先安装 Python 3.6 或更高版本
    pause
    exit /b 1
)

REM 检查依赖是否安装
echo 检查依赖包...
python -c "import ffmpeg" >nul 2>&1
if errorlevel 1 (
    echo 正在安装依赖包...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo 错误: 依赖包安装失败
        pause
        exit /b 1
    )
)

REM 运行程序
echo 启动程序...
python video_splitter_app.py

pause
