@echo off
echo ========================================
echo 视频分割工具 - GitHub 上传脚本
echo ========================================
echo.

echo 步骤 1: 请在浏览器中创建 GitHub 仓库
echo 1. 访问 https://github.com
echo 2. 点击右上角 "+" 号，选择 "New repository"
echo 3. 仓库名称: video-splitter-tool
echo 4. 描述: A Python desktop application for batch video splitting using FFmpeg and Tkinter
echo 5. 选择 Public 或 Private
echo 6. 不要勾选任何初始化选项
echo 7. 点击 "Create repository"
echo.

set /p github_username="请输入您的 GitHub 用户名: "

if "%github_username%"=="" (
    echo 错误: 用户名不能为空
    pause
    exit /b 1
)

echo.
echo 正在连接到 GitHub 仓库...
git remote add origin https://github.com/%github_username%/video-splitter-tool.git

if errorlevel 1 (
    echo 警告: 远程仓库可能已存在，尝试更新...
    git remote set-url origin https://github.com/%github_username%/video-splitter-tool.git
)

echo.
echo 正在上传代码到 GitHub...
git push -u origin main

if errorlevel 1 (
    echo.
    echo 上传失败！可能的原因：
    echo 1. 网络连接问题
    echo 2. 认证失败（需要使用 Personal Access Token）
    echo 3. 仓库不存在或权限不足
    echo.
    echo 请检查：
    echo - 确保已创建 GitHub 仓库
    echo - 确保网络连接正常
    echo - 如果提示认证，请使用 Personal Access Token 而不是密码
    echo.
    echo 获取 Personal Access Token:
    echo 1. GitHub Settings ^> Developer settings ^> Personal access tokens
    echo 2. Generate new token (classic)
    echo 3. 选择适当的权限范围
    echo 4. 复制生成的 token 作为密码使用
) else (
    echo.
    echo ========================================
    echo 上传成功！
    echo ========================================
    echo 您的项目已上传到:
    echo https://github.com/%github_username%/video-splitter-tool
    echo.
    echo 下一步:
    echo 1. 访问上述链接查看您的项目
    echo 2. 在 README.md 中添加项目截图
    echo 3. 设置仓库描述和标签
    echo 4. 分享您的项目！
)

echo.
pause
