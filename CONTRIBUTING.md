# 贡献指南

感谢您对视频分割工具项目的关注！我们欢迎任何形式的贡献。

## 如何贡献

### 报告问题
如果您发现了 bug 或有功能建议，请：
1. 在 Issues 页面创建一个新的 issue
2. 详细描述问题或建议
3. 如果可能，提供复现步骤

### 提交代码
1. Fork 这个仓库
2. 创建您的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交您的更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开一个 Pull Request

## 开发环境设置

1. 克隆仓库
```bash
git clone https://github.com/your-username/video-splitter-tool.git
cd video-splitter-tool
```

2. 创建虚拟环境
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

3. 安装依赖
```bash
pip install -r requirements.txt
```

4. 安装 FFmpeg（如果尚未安装）
   - Windows: 下载并添加到 PATH
   - macOS: `brew install ffmpeg`
   - Linux: `sudo apt install ffmpeg`

## 代码规范

- 使用 Python 3.6+ 语法
- 遵循 PEP 8 代码风格
- 添加适当的注释和文档字符串
- 确保代码通过所有测试

## 测试

运行测试脚本：
```bash
python test_app.py
python test_segmentation.py
```

## 许可证

通过贡献代码，您同意您的贡献将在 MIT 许可证下发布。
