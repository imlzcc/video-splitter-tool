# 部署说明

## 快速开始

### 1. 克隆仓库
```bash
git clone https://github.com/your-username/video-splitter-tool.git
cd video-splitter-tool
```

### 2. 安装 Python 依赖
```bash
pip install -r requirements.txt
```

### 3. 安装 FFmpeg

#### Windows
1. 访问 [FFmpeg 官网](https://ffmpeg.org/download.html)
2. 下载 Windows 版本
3. 解压到任意目录（如 `C:\ffmpeg`）
4. 将 `C:\ffmpeg\bin` 添加到系统 PATH 环境变量
5. 验证安装：在命令行运行 `ffmpeg -version`

#### macOS
```bash
brew install ffmpeg
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install ffmpeg
```

### 4. 运行程序

#### 方法一：直接运行
```bash
python video_splitter_app.py
```

#### 方法二：使用批处理文件（Windows）
双击 `run.bat` 文件

#### 方法三：测试功能
```bash
python test_app.py
python test_segmentation.py
```

## Docker 部署（可选）

如果您想使用 Docker 部署，可以创建以下 Dockerfile：

```dockerfile
FROM python:3.9-slim

# 安装 FFmpeg
RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*

# 设置工作目录
WORKDIR /app

# 复制依赖文件
COPY requirements.txt .

# 安装 Python 依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY . .

# 设置环境变量
ENV DISPLAY=:0

# 运行应用
CMD ["python", "video_splitter_app.py"]
```

构建和运行：
```bash
docker build -t video-splitter .
docker run -it --rm -v /path/to/videos:/app/videos video-splitter
```

## 配置说明

程序会自动创建 `config.json` 文件来保存您的设置。您也可以手动编辑这个文件：

```json
{
  "source_folder": "C:\\Users\\用户名\\Videos\\源视频",
  "output_folder": "C:\\Users\\用户名\\Videos\\分割片段",
  "min_duration": 5,
  "max_duration": 15
}
```

## 故障排除

### 常见问题

1. **"FFmpeg not found" 错误**
   - 确保 FFmpeg 已正确安装并添加到 PATH
   - 重启命令行或 IDE

2. **权限错误**
   - 确保对源文件夹和输出文件夹有读写权限
   - 以管理员身份运行程序（如果需要）

3. **视频无法分割**
   - 检查视频文件是否损坏
   - 尝试使用其他视频格式
   - 查看日志了解详细错误信息

4. **程序无响应**
   - 处理大文件时请耐心等待
   - 检查系统资源使用情况
   - 查看任务管理器确认程序正在运行

### 日志文件

程序会在界面中显示详细的操作日志，包括：
- 处理的文件列表
- 分割进度
- 错误信息
- 生成的片段信息

## 性能优化建议

1. **使用 SSD 硬盘**：提高文件读写速度
2. **充足的内存**：建议至少 4GB RAM
3. **关闭其他程序**：释放系统资源
4. **选择合适的输出格式**：MP4 通常是最佳选择

## 支持

如果您遇到问题或有建议，请：
1. 查看 [README.md](README.md) 中的常见问题
2. 在 GitHub Issues 中搜索相关问题
3. 创建新的 Issue 描述您的问题
4. 查看 [CONTRIBUTING.md](CONTRIBUTING.md) 了解如何贡献代码
