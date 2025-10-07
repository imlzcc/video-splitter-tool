# 视频批量分割工具

一个基于 Python 和 FFmpeg 的桌面应用程序，用于批量分割视频文件。

## 功能特点

- 🎬 支持多种视频格式（MP4, AVI, MOV, MKV, WMV, FLV, WebM, M4V）
- ⚡ 使用 FFmpeg 流拷贝模式，分割速度快
- 🎯 随机时长分割，避免重复模式
- 🔄 多线程处理，界面不卡顿
- 💾 自动保存和加载配置
- 📊 实时进度显示和日志记录
- 🛡️ 强大的错误处理机制

## 安装要求

### 1. Python 环境
- Python 3.6 或更高版本

### 2. FFmpeg
在运行程序之前，您需要安装 FFmpeg：

**Windows:**
1. 下载 FFmpeg: https://ffmpeg.org/download.html
2. 解压到任意目录（如 `C:\ffmpeg`）
3. 将 FFmpeg 的 `bin` 目录添加到系统 PATH 环境变量中

**macOS:**
```bash
brew install ffmpeg
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install ffmpeg
```

### 3. Python 依赖
```bash
pip install -r requirements.txt
```

## 使用方法

1. 运行程序：
```bash
python video_splitter_app.py
```

2. 选择视频源文件夹（包含要分割的视频文件）

3. 选择片段保存文件夹（分割后的视频将保存到这里）

4. 设置分割参数：
   - 最小片段时长（秒）
   - 最大片段时长（秒）

5. 点击"开始分割"按钮

6. 等待处理完成，查看日志了解进度

## 分割逻辑

- 程序会随机生成每个片段的时长，在您设定的最小和最大时长范围内
- 使用 FFmpeg 的流拷贝模式进行分割，速度极快
- 如果流拷贝失败，会自动回退到重新编码模式
- 生成的片段文件命名格式：`原文件名_part_001.扩展名`

## 配置文件

程序会自动创建 `config.json` 文件来保存您的设置：
- 源文件夹路径
- 输出文件夹路径
- 最小/最大片段时长

## 注意事项

- 确保有足够的磁盘空间存储分割后的视频片段
- 处理大量视频时请耐心等待
- 如果遇到错误，请查看日志了解详细信息
- 建议在处理重要视频前先备份原文件

## 技术实现

- **GUI框架**: Tkinter
- **视频处理**: FFmpeg (通过 ffmpeg-python)
- **多线程**: Python threading 模块
- **配置管理**: JSON 文件
- **日志系统**: Python logging 模块

## 故障排除

### 常见问题

1. **"FFmpeg not found" 错误**
   - 确保 FFmpeg 已正确安装并添加到 PATH 环境变量

2. **"Permission denied" 错误**
   - 确保对源文件夹和输出文件夹有读写权限

3. **视频无法分割**
   - 检查视频文件是否损坏
   - 尝试使用其他视频格式

4. **程序无响应**
   - 处理大文件时请耐心等待
   - 检查系统资源使用情况

## 许可证

本项目采用 MIT 许可证。
