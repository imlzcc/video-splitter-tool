#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
视频批量分割工具
使用 FFmpeg 和 Tkinter 构建的桌面应用程序
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import json
import os
import random
import time
from pathlib import Path
import ffmpeg
import logging

class VideoSplitterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("视频批量分割工具")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # 配置变量
        self.source_folder = tk.StringVar()
        self.output_folder = tk.StringVar()
        self.min_duration = tk.IntVar(value=5)
        self.max_duration = tk.IntVar(value=15)
        
        # 处理状态
        self.is_processing = False
        self.processing_thread = None
        
        # 设置日志
        self.setup_logging()
        
        # 创建界面
        self.create_widgets()
        
        # 加载配置
        self.load_config()
        
        # 绑定关闭事件
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def setup_logging(self):
        """设置日志记录"""
        # 创建日志控制台处理器
        self.log_handler = logging.StreamHandler()
        self.log_handler.setLevel(logging.INFO)
        
        # 创建格式化器
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        self.log_handler.setFormatter(formatter)
        
        # 创建日志记录器
        self.logger = logging.getLogger('VideoSplitter')
        self.logger.setLevel(logging.INFO)
        self.logger.addHandler(self.log_handler)
    
    def create_widgets(self):
        """创建GUI界面"""
        # 主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 配置网格权重
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # 源文件夹选择区域
        ttk.Label(main_frame, text="选择视频源文件夹:").grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        self.source_entry = ttk.Entry(main_frame, textvariable=self.source_folder, state="readonly")
        self.source_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(5, 5), pady=(0, 5))
        ttk.Button(main_frame, text="浏览...", command=self.browse_source_folder).grid(row=0, column=2, pady=(0, 5))
        
        # 输出文件夹选择区域
        ttk.Label(main_frame, text="选择片段保存文件夹:").grid(row=1, column=0, sticky=tk.W, pady=(0, 5))
        self.output_entry = ttk.Entry(main_frame, textvariable=self.output_folder, state="readonly")
        self.output_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(5, 5), pady=(0, 5))
        ttk.Button(main_frame, text="浏览...", command=self.browse_output_folder).grid(row=1, column=2, pady=(0, 5))
        
        # 分割参数区域
        params_frame = ttk.LabelFrame(main_frame, text="分割参数", padding="10")
        params_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 10))
        params_frame.columnconfigure(1, weight=1)
        
        # 最小时长
        ttk.Label(params_frame, text="最小片段时长 (秒):").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.min_duration_spinbox = ttk.Spinbox(params_frame, from_=1, to=300, textvariable=self.min_duration, width=10)
        self.min_duration_spinbox.grid(row=0, column=1, sticky=tk.W, padx=(0, 20))
        
        # 最大时长
        ttk.Label(params_frame, text="最大片段时长 (秒):").grid(row=0, column=2, sticky=tk.W, padx=(0, 10))
        self.max_duration_spinbox = ttk.Spinbox(params_frame, from_=1, to=300, textvariable=self.max_duration, width=10)
        self.max_duration_spinbox.grid(row=0, column=3, sticky=tk.W)
        
        # 控制按钮区域
        control_frame = ttk.Frame(main_frame)
        control_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 10))
        control_frame.columnconfigure(0, weight=1)
        
        self.start_button = ttk.Button(control_frame, text="开始分割", command=self.start_processing)
        self.start_button.grid(row=0, column=0, pady=(0, 10))
        
        # 进度条
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(control_frame, variable=self.progress_var, maximum=100)
        self.progress_bar.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # 日志控制台
        log_frame = ttk.LabelFrame(main_frame, text="操作日志", padding="5")
        log_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        main_frame.rowconfigure(4, weight=1)
        
        # 创建文本框和滚动条
        self.log_text = tk.Text(log_frame, height=15, wrap=tk.WORD)
        scrollbar = ttk.Scrollbar(log_frame, orient=tk.VERTICAL, command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=scrollbar.set)
        
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # 重定向日志到文本框
        self.setup_text_logging()
    
    def setup_text_logging(self):
        """设置日志输出到文本框"""
        class TextHandler(logging.Handler):
            def __init__(self, text_widget):
                super().__init__()
                self.text_widget = text_widget
            
            def emit(self, record):
                msg = self.format(record)
                def append():
                    self.text_widget.insert(tk.END, msg + '\n')
                    self.text_widget.see(tk.END)
                self.text_widget.after(0, append)
        
        text_handler = TextHandler(self.log_text)
        text_handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        text_handler.setFormatter(formatter)
        self.logger.addHandler(text_handler)
    
    def browse_source_folder(self):
        """浏览源文件夹"""
        folder = filedialog.askdirectory(title="选择视频源文件夹")
        if folder:
            self.source_folder.set(folder)
    
    def browse_output_folder(self):
        """浏览输出文件夹"""
        folder = filedialog.askdirectory(title="选择片段保存文件夹")
        if folder:
            self.output_folder.set(folder)
    
    def load_config(self):
        """加载配置文件"""
        config_file = "config.json"
        if os.path.exists(config_file):
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    self.source_folder.set(config.get('source_folder', ''))
                    self.output_folder.set(config.get('output_folder', ''))
                    self.min_duration.set(config.get('min_duration', 5))
                    self.max_duration.set(config.get('max_duration', 15))
                self.logger.info("配置加载成功")
            except Exception as e:
                self.logger.error(f"加载配置失败: {e}")
    
    def save_config(self):
        """保存配置文件"""
        config = {
            'source_folder': self.source_folder.get(),
            'output_folder': self.output_folder.get(),
            'min_duration': self.min_duration.get(),
            'max_duration': self.max_duration.get()
        }
        try:
            with open("config.json", 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
            self.logger.info("配置保存成功")
        except Exception as e:
            self.logger.error(f"保存配置失败: {e}")
    
    def validate_inputs(self):
        """验证输入参数"""
        if not self.source_folder.get():
            messagebox.showerror("错误", "请选择源文件夹")
            return False
        
        if not self.output_folder.get():
            messagebox.showerror("错误", "请选择输出文件夹")
            return False
        
        if not os.path.exists(self.source_folder.get()):
            messagebox.showerror("错误", "源文件夹不存在")
            return False
        
        if not os.path.exists(self.output_folder.get()):
            messagebox.showerror("错误", "输出文件夹不存在")
            return False
        
        min_dur = self.min_duration.get()
        max_dur = self.max_duration.get()
        
        if min_dur <= 0 or max_dur <= 0:
            messagebox.showerror("错误", "时长必须大于0")
            return False
        
        if min_dur > max_dur:
            messagebox.showerror("错误", "最小时长不能大于最大时长")
            return False
        
        return True
    
    def start_processing(self):
        """开始处理视频"""
        if not self.validate_inputs():
            return
        
        if self.is_processing:
            return
        
        # 禁用界面控件
        self.set_ui_state(False)
        self.is_processing = True
        
        # 清空日志
        self.log_text.delete(1.0, tk.END)
        
        # 启动后台线程
        self.processing_thread = threading.Thread(target=self.process_videos)
        self.processing_thread.daemon = True
        self.processing_thread.start()
    
    def set_ui_state(self, enabled):
        """设置界面控件状态"""
        state = 'normal' if enabled else 'disabled'
        self.source_entry.config(state=state)
        self.output_entry.config(state=state)
        self.min_duration_spinbox.config(state=state)
        self.max_duration_spinbox.config(state=state)
        self.start_button.config(state=state)
    
    def process_videos(self):
        """处理视频文件（在后台线程中执行）"""
        try:
            source_path = Path(self.source_folder.get())
            output_path = Path(self.output_folder.get())
            
            # 支持的视频格式
            video_extensions = {'.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv', '.webm', '.m4v'}
            
            # 扫描视频文件
            video_files = []
            for ext in video_extensions:
                video_files.extend(source_path.glob(f"*{ext}"))
                video_files.extend(source_path.glob(f"*{ext.upper()}"))
            
            if not video_files:
                self.logger.warning("未找到任何视频文件")
                self.root.after(0, lambda: self.processing_complete())
                return
            
            self.logger.info(f"找到 {len(video_files)} 个视频文件")
            
            # 处理每个视频文件
            total_files = len(video_files)
            for i, video_file in enumerate(video_files):
                try:
                    self.logger.info(f"正在处理: {video_file.name}")
                    self.split_video(video_file, output_path)
                    
                    # 更新进度
                    progress = ((i + 1) / total_files) * 100
                    self.root.after(0, lambda p=progress: self.progress_var.set(p))
                    
                except Exception as e:
                    self.logger.error(f"处理文件 {video_file.name} 时出错: {e}")
                    continue
            
            self.logger.info("全部任务完成！")
            self.root.after(0, lambda: messagebox.showinfo("完成", "视频分割任务已完成！"))
            
        except Exception as e:
            self.logger.error(f"处理过程中出现错误: {e}")
            self.root.after(0, lambda: messagebox.showerror("错误", f"处理过程中出现错误: {e}"))
        
        finally:
            self.root.after(0, lambda: self.processing_complete())
    
    def split_video(self, video_file, output_path):
        """分割单个视频文件"""
        try:
            # 获取视频时长
            probe = ffmpeg.probe(str(video_file))
            duration = float(probe['streams'][0]['duration'])
            
            self.logger.info(f"视频时长: {duration:.2f} 秒")
            
            # 生成分割方案
            segments = self.generate_segments(duration)
            self.logger.info(f"将分割为 {len(segments)} 个片段")
            
            # 执行分割
            for i, (start_time, segment_duration) in enumerate(segments, 1):
                # 验证片段时长
                if segment_duration < self.min_duration.get():
                    self.logger.warning(f"跳过片段 {i}：时长 {segment_duration:.2f} 秒小于最小时长 {self.min_duration.get()} 秒")
                    continue
                
                self.logger.info(f"计划分割片段 {i}: 起始时间 {start_time:.2f}s, 计划时长 {segment_duration:.2f}s")
                output_file = output_path / f"{video_file.stem}_part_{i:03d}{video_file.suffix}"
                
                try:
                    # 尝试使用流拷贝模式（快速）
                    self.split_with_copy(video_file, output_file, start_time, segment_duration)
                    
                    # 验证生成的片段时长
                    actual_duration = self.get_video_duration(output_file)
                    if actual_duration < self.min_duration.get():
                        self.logger.warning(f"删除过短片段: {output_file.name} (时长: {actual_duration:.2f} 秒)")
                        output_file.unlink()  # 删除文件
                        continue
                    
                    self.logger.info(f"生成片段: {output_file.name} (时长: {actual_duration:.2f} 秒)")
                    
                except Exception as e:
                    self.logger.warning(f"流拷贝失败，尝试重新编码: {e}")
                    try:
                        # 回退到重新编码模式
                        self.split_with_reencode(video_file, output_file, start_time, segment_duration)
                        
                        # 验证生成的片段时长
                        actual_duration = self.get_video_duration(output_file)
                        if actual_duration < self.min_duration.get():
                            self.logger.warning(f"删除过短片段: {output_file.name} (时长: {actual_duration:.2f} 秒)")
                            output_file.unlink()  # 删除文件
                            continue
                        
                        self.logger.info(f"生成片段: {output_file.name} (时长: {actual_duration:.2f} 秒)")
                    except Exception as e2:
                        self.logger.error(f"分割片段失败: {e2}")
                        continue
                        
        except Exception as e:
            self.logger.error(f"处理视频文件 {video_file.name} 失败: {e}")
            raise
    
    def generate_segments(self, total_duration):
        """生成分割方案"""
        segments = []
        current_time = 0.0
        min_dur = self.min_duration.get()
        max_dur = self.max_duration.get()
        
        while current_time < total_duration:
            # 计算剩余时间
            remaining_time = total_duration - current_time
            
            # 如果剩余时间不足最小时长，则跳过（不生成片段）
            if remaining_time < min_dur:
                self.logger.info(f"剩余时间 {remaining_time:.2f} 秒不足最小时长 {min_dur} 秒，跳过")
                break
            
            # 在最小和最大时长之间随机选择
            # 确保不超过剩余时间
            max_possible_duration = min(max_dur, remaining_time)
            
            # 如果最大可能时长小于最小时长，则跳过
            if max_possible_duration < min_dur:
                self.logger.info(f"剩余时间 {remaining_time:.2f} 秒不足以生成符合最小时长 {min_dur} 秒的片段，跳过")
                break
            
            # 生成随机时长，确保在有效范围内
            segment_duration = random.uniform(min_dur, max_possible_duration)
            
            # 再次确保片段时长至少为最小时长（双重保险）
            segment_duration = max(segment_duration, min_dur)
            
            segments.append((current_time, segment_duration))
            current_time += segment_duration
        
        return segments
    
    def split_with_copy(self, input_file, output_file, start_time, duration):
        """使用流拷贝模式分割视频（快速）"""
        end_time = start_time + duration
        (
            ffmpeg
            .input(str(input_file), ss=start_time, to=end_time)
            .output(str(output_file), c='copy')
            .overwrite_output()
            .run(quiet=True)
        )
    
    def split_with_reencode(self, input_file, output_file, start_time, duration):
        """使用重新编码模式分割视频（兼容性更好）"""
        end_time = start_time + duration
        (
            ffmpeg
            .input(str(input_file), ss=start_time, to=end_time)
            .output(str(output_file), vcodec='libx264', acodec='aac')
            .overwrite_output()
            .run(quiet=True)
        )
    
    def get_video_duration(self, video_file):
        """获取视频文件的实际时长"""
        try:
            probe = ffmpeg.probe(str(video_file))
            return float(probe['streams'][0]['duration'])
        except Exception as e:
            self.logger.error(f"获取视频时长失败 {video_file.name}: {e}")
            return 0.0
    
    def processing_complete(self):
        """处理完成后的清理工作"""
        self.is_processing = False
        self.set_ui_state(True)
        self.progress_var.set(0)
    
    def on_closing(self):
        """程序关闭时的处理"""
        if self.is_processing:
            if messagebox.askokcancel("退出", "正在处理视频，确定要退出吗？"):
                self.is_processing = False
                self.root.destroy()
        else:
            self.save_config()
            self.root.destroy()

def main():
    """主函数"""
    root = tk.Tk()
    app = VideoSplitterApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
