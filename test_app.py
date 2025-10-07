#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
视频分割工具测试脚本
用于验证基本功能是否正常工作
"""

import os
import sys
import tempfile
import shutil
from pathlib import Path

def test_imports():
    """测试所有必要的模块是否能正确导入"""
    print("测试模块导入...")
    
    try:
        import tkinter as tk
        print("✓ tkinter 导入成功")
    except ImportError as e:
        print(f"✗ tkinter 导入失败: {e}")
        return False
    
    try:
        import ffmpeg
        print("✓ ffmpeg-python 导入成功")
    except ImportError as e:
        print(f"✗ ffmpeg-python 导入失败: {e}")
        print("请运行: pip install ffmpeg-python")
        return False
    
    try:
        import threading
        import json
        import random
        import time
        import logging
        print("✓ 标准库模块导入成功")
    except ImportError as e:
        print(f"✗ 标准库模块导入失败: {e}")
        return False
    
    return True

def test_ffmpeg():
    """测试 FFmpeg 是否可用"""
    print("\n测试 FFmpeg 可用性...")
    
    try:
        import ffmpeg
        # 尝试获取 FFmpeg 版本信息
        result = ffmpeg.run(ffmpeg.input('', f='lavfi', i='testsrc=duration=1:size=320x240:rate=1'), 
                           capture_stdout=True, capture_stderr=True, overwrite_output=True)
        print("✓ FFmpeg 可用")
        return True
    except Exception as e:
        print(f"✗ FFmpeg 不可用: {e}")
        print("请确保 FFmpeg 已安装并添加到 PATH 环境变量")
        return False

def test_app_creation():
    """测试应用程序是否能正常创建"""
    print("\n测试应用程序创建...")
    
    try:
        import tkinter as tk
        from video_splitter_app import VideoSplitterApp
        
        # 创建隐藏的根窗口
        root = tk.Tk()
        root.withdraw()  # 隐藏窗口
        
        # 创建应用程序实例
        app = VideoSplitterApp(root)
        
        print("✓ 应用程序创建成功")
        
        # 清理
        root.destroy()
        return True
        
    except Exception as e:
        print(f"✗ 应用程序创建失败: {e}")
        return False

def test_config_handling():
    """测试配置文件处理"""
    print("\n测试配置文件处理...")
    
    try:
        import tkinter as tk
        from video_splitter_app import VideoSplitterApp
        import json
        import tempfile
        import os
        
        # 创建临时目录
        with tempfile.TemporaryDirectory() as temp_dir:
            original_dir = os.getcwd()
            os.chdir(temp_dir)
            
            try:
                # 创建隐藏的根窗口
                root = tk.Tk()
                root.withdraw()
                
                # 创建应用程序实例
                app = VideoSplitterApp(root)
                
                # 测试保存配置
                app.source_folder.set("test_source")
                app.output_folder.set("test_output")
                app.min_duration.set(10)
                app.max_duration.set(20)
                app.save_config()
                
                # 检查配置文件是否创建
                if os.path.exists("config.json"):
                    print("✓ 配置文件保存成功")
                else:
                    print("✗ 配置文件保存失败")
                    return False
                
                # 测试加载配置
                app.source_folder.set("")
                app.output_folder.set("")
                app.min_duration.set(5)
                app.max_duration.set(15)
                app.load_config()
                
                if (app.source_folder.get() == "test_source" and 
                    app.output_folder.get() == "test_output" and
                    app.min_duration.get() == 10 and
                    app.max_duration.get() == 20):
                    print("✓ 配置文件加载成功")
                else:
                    print("✗ 配置文件加载失败")
                    return False
                
                # 清理
                root.destroy()
                return True
                
            finally:
                os.chdir(original_dir)
                
    except Exception as e:
        print(f"✗ 配置文件处理失败: {e}")
        return False

def main():
    """主测试函数"""
    print("视频分割工具 - 功能测试")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_ffmpeg,
        test_app_creation,
        test_config_handling
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 50)
    print(f"测试结果: {passed}/{total} 通过")
    
    if passed == total:
        print("✓ 所有测试通过！程序可以正常运行。")
        return True
    else:
        print("✗ 部分测试失败，请检查上述错误信息。")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
