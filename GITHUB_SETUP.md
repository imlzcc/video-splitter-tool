# GitHub 上传指南

## 步骤 1: 在 GitHub 上创建新仓库

1. 访问 [GitHub.com](https://github.com) 并登录您的账户
2. 点击右上角的 "+" 号，选择 "New repository"
3. 填写仓库信息：
   - **Repository name**: `video-splitter-tool` 或您喜欢的名称
   - **Description**: `A Python desktop application for batch video splitting using FFmpeg and Tkinter`
   - **Visibility**: 选择 Public（公开）或 Private（私有）
   - **不要**勾选 "Add a README file"（我们已经有了）
   - **不要**勾选 "Add .gitignore"（我们已经有了）
   - **不要**勾选 "Choose a license"（我们已经有了）
4. 点击 "Create repository"

## 步骤 2: 连接本地仓库到 GitHub

在命令行中运行以下命令（将 `your-username` 替换为您的 GitHub 用户名）：

```bash
# 添加远程仓库
git remote add origin https://github.com/your-username/video-splitter-tool.git

# 设置默认分支为 main
git branch -M main

# 推送到 GitHub
git push -u origin main
```

## 步骤 3: 验证上传

1. 刷新您的 GitHub 仓库页面
2. 确认所有文件都已上传
3. 检查 README.md 是否正确显示

## 步骤 4: 配置仓库设置（可选）

### 添加仓库描述和标签
1. 在仓库页面点击 "Settings"
2. 在 "About" 部分添加：
   - 描述：`A Python desktop application for batch video splitting using FFmpeg and Tkinter`
   - 网站：如果有的话
   - 标签：`python`, `video`, `ffmpeg`, `tkinter`, `desktop-app`, `video-processing`

### 启用 Issues 和 Wiki
1. 在 Settings 中确保 "Features" 部分启用了：
   - Issues
   - Wiki（如果需要）

### 设置分支保护（可选）
1. 在 Settings > Branches 中
2. 添加规则保护 main 分支
3. 要求 Pull Request 审查

## 步骤 5: 创建 Release（可选）

1. 在仓库页面点击 "Releases"
2. 点击 "Create a new release"
3. 填写版本信息：
   - Tag version: `v1.0.0`
   - Release title: `Video Splitter Tool v1.0.0`
   - Description: 描述这个版本的功能
4. 点击 "Publish release"

## 步骤 6: 分享您的项目

### 创建项目徽章
在 README.md 顶部添加徽章：

```markdown
![Python](https://img.shields.io/badge/python-3.6+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![FFmpeg](https://img.shields.io/badge/FFmpeg-required-red.svg)
```

### 添加截图
1. 运行程序并截图
2. 将截图保存为 `screenshot.png`
3. 在 README.md 中添加：
```markdown
![Screenshot](screenshot.png)
```

## 常见问题

### Q: 推送时提示认证失败
A: 使用 Personal Access Token 而不是密码：
1. GitHub Settings > Developer settings > Personal access tokens
2. 生成新的 token
3. 使用 token 作为密码

### Q: 如何更新仓库
A: 修改代码后运行：
```bash
git add .
git commit -m "描述您的更改"
git push
```

### Q: 如何邀请协作者
A: 在仓库 Settings > Manage access > Invite a collaborator

## 下一步

1. 在社交媒体上分享您的项目
2. 在相关论坛和社区发布
3. 收集用户反馈并持续改进
4. 考虑添加更多功能

祝您的项目成功！🎉
