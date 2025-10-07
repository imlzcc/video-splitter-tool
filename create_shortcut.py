#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
创建桌面快捷方式的脚本
"""

import os
import sys
from pathlib import Path

def create_desktop_shortcut():
    """创建桌面快捷方式"""
    try:
        # 获取当前脚本所在目录
        current_dir = Path(__file__).parent.absolute()
        
        # 获取桌面路径
        desktop = Path.home() / "Desktop"
        
        # 创建快捷方式文件路径
        shortcut_path = desktop / "视频分割工具.lnk"
        
        print("=" * 50)
        print("创建桌面快捷方式")
        print("=" * 50)
        print(f"当前目录: {current_dir}")
        print(f"桌面路径: {desktop}")
        print()
        
        # 创建 VBS 脚本来生成快捷方式
        vbs_content = f'''
Set oWS = WScript.CreateObject("WScript.Shell")
sLinkFile = "{shortcut_path}"
Set oLink = oWS.CreateShortcut(sLinkFile)
oLink.TargetPath = "{current_dir}\\run.bat"
oLink.WorkingDirectory = "{current_dir}"
oLink.Description = "视频批量分割工具 - 使用FFmpeg和Tkinter"
oLink.IconLocation = "python.exe,0"
oLink.Save
'''
        
        # 写入临时 VBS 文件
        vbs_file = Path.home() / "AppData" / "Local" / "Temp" / "CreateShortcut.vbs"
        vbs_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(vbs_file, 'w', encoding='utf-8') as f:
            f.write(vbs_content)
        
        # 执行 VBS 脚本
        import subprocess
        result = subprocess.run(['cscript', '//nologo', str(vbs_file)], 
                              capture_output=True, text=True)
        
        # 清理临时文件
        vbs_file.unlink()
        
        if shortcut_path.exists():
            print("=" * 50)
            print("快捷方式创建成功！")
            print("=" * 50)
            print(f"桌面快捷方式: {shortcut_path.name}")
            print(f"位置: {desktop}")
            print()
            print("现在您可以直接双击桌面上的\"视频分割工具\"图标来启动程序！")
            print()
            
            # 询问是否打开桌面
            choice = input("是否要打开桌面查看快捷方式？(Y/N): ").strip().upper()
            if choice == 'Y':
                os.startfile(str(desktop))
                
        else:
            print("错误: 快捷方式创建失败！")
            print("请检查权限或手动创建快捷方式。")
            
    except Exception as e:
        print(f"创建快捷方式时出错: {e}")
        print("请尝试手动创建快捷方式。")

if __name__ == "__main__":
    create_desktop_shortcut()
    input("\n按任意键退出...")
