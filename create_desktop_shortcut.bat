@echo off
echo ========================================
echo 创建桌面快捷方式
echo ========================================
echo.

set "current_dir=%~dp0"
set "desktop=%USERPROFILE%\Desktop"
set "shortcut_name=视频分割工具.lnk"

echo 当前目录: %current_dir%
echo 桌面路径: %desktop%
echo.

echo 正在创建桌面快捷方式...

:: 创建 VBS 脚本来生成快捷方式
echo Set oWS = WScript.CreateObject("WScript.Shell") > "%temp%\CreateShortcut.vbs"
echo sLinkFile = "%desktop%\%shortcut_name%" >> "%temp%\CreateShortcut.vbs"
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> "%temp%\CreateShortcut.vbs"
echo oLink.TargetPath = "%current_dir%run.bat" >> "%temp%\CreateShortcut.vbs"
echo oLink.WorkingDirectory = "%current_dir%" >> "%temp%\CreateShortcut.vbs"
echo oLink.Description = "视频批量分割工具 - 使用FFmpeg和Tkinter" >> "%temp%\CreateShortcut.vbs"
echo oLink.IconLocation = "python.exe,0" >> "%temp%\CreateShortcut.vbs"
echo oLink.Save >> "%temp%\CreateShortcut.vbs"

:: 执行 VBS 脚本
cscript //nologo "%temp%\CreateShortcut.vbs"

:: 清理临时文件
del "%temp%\CreateShortcut.vbs"

if exist "%desktop%\%shortcut_name%" (
    echo.
    echo ========================================
    echo 快捷方式创建成功！
    echo ========================================
    echo 桌面快捷方式: %shortcut_name%
    echo 位置: %desktop%
    echo.
    echo 现在您可以直接双击桌面上的"视频分割工具"图标来启动程序！
    echo.
    
    :: 询问是否打开桌面
    set /p open_desktop="是否要打开桌面查看快捷方式？(Y/N): "
    if /i "%open_desktop%"=="Y" (
        explorer "%desktop%"
    )
) else (
    echo.
    echo 错误: 快捷方式创建失败！
    echo 请检查权限或手动创建快捷方式。
)

echo.
pause
