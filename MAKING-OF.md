# Knowledge Hub 制作流程文档

> 本文档记录了 knowledge-hub 知识库从 0 到 1 的完整制作过程，包括使用的工具、技术选型、遇到的问题和解决方案。

---

## 一、项目概述

### 1.1 目标

创建一个个人知识库，用于：
- 整理和分享视频学习笔记
- 按主题分类管理知识内容
- 通过 GitHub Pages 提供在线阅读

### 1.2 最终成果

- **GitHub 仓库**：https://github.com/ytwangdongsheng/knowledge-hub
- **在线阅读**：https://ytwangdongsheng.github.io/knowledge-hub/
- **当前主题**：
  - RAG 工作机制详解
  - AI 编程全流程

---

## 二、技术栈与工具

### 2.1 核心工具

| 工具 | 用途 | 安装方式 |
|------|------|----------|
| **yt-dlp** | 下载 B站/YouTube 视频 | `pip install yt-dlp` |
| **ffmpeg** | 提取音频、提取关键帧 | 手动安装到 `E:\python\Scripts\` |
| **faster-whisper** | 语音转文字（本地转录） | `pip install faster-whisper` |
| **Pillow** | 生成图片、卡片 | `pip install Pillow` |
| **gh CLI** | GitHub 命令行工具 | `winget install GitHub.cli` |
| **git** | 版本控制 | 系统自带 |

### 2.2 DSH Skills 使用

| Skill | 用途 |
|-------|------|
| `z-video-downloader` | 视频下载 |
| `z-video-study-webpage-qwen` | 视频学习笔记生成 |
| `fireworks-tech-graph` | 技术图表生成（尝试过，最终未使用） |

### 2.3 部署工具

| 工具 | 用途 | 状态 |
|------|------|------|
| **Cloudflare Pages** | 初始部署方案 | 已弃用 |
| **GitHub Pages** | 最终部署方案 | ✅ 使用中 |

---

## 三、制作流程详解

### 阶段一：第一个视频笔记（RAG）

#### 3.1 视频下载

**目标视频**：B站 BV1JLN2z4EZQ《RAG 工作机制详解》

**步骤**：
```bash
# 1. 获取视频信息
yt-dlp --print title --no-download "https://www.bilibili.com/video/BV1JLN2z4EZQ"

# 2. 下载视频
yt-dlp -o "Video/Downloads/study-qwen/video.mp4" \
  --write-info-json \
  "https://www.bilibili.com/video/BV1JLN2z4EZQ"
```

**遇到的问题**：
- yt-dlp 未安装 → `pip install yt-dlp`
- ffmpeg 不在 PATH → 手动复制到 `E:\python\Scripts\ffmpeg.exe`

**结果**：
- 视频文件：123.6 MB
- 时长：17:01
- 分辨率：1920×1080

#### 3.2 音频提取与转录

**步骤**：
```bash
# 1. 提取音频（16kHz 单声道，适合 whisper）
ffmpeg -i video.mp4 -vn -acodec pcm_s16le -ar 16000 -ac 1 audio.wav

# 2. 使用 faster-whisper 转录
python transcribe.py
```

**transcribe.py 核心代码**：
```python
from faster_whisper import WhisperModel

model = WhisperModel("base", device="cpu", compute_type="int8")
segments, info = model.transcribe("audio.wav", language="zh", beam_size=5)

for seg in segments:
    print(f"[{seg.start:.1f}s - {seg.end:.1f}s] {seg.text}")
```

**遇到的问题**：
- torch 安装超时（太大）→ 改用 `faster-whisper`（轻量级）
- 转录有错别字 → 手动修正专业术语（RAG、Embedding、Cross-Encoder 等）

**结果**：
- 转录文本：507 行
- 耗时：约 4 分钟（CPU）

#### 3.3 关键帧提取

**步骤**：
```python
import subprocess

timestamps = [
    (0, "00-intro"),
    (30, "01-why-rag"),
    (180, "02-vector"),
    # ... 根据视频内容选择关键时间点
]

for ts, name in timestamps:
    subprocess.run([
        "ffmpeg", "-ss", str(ts),
        "-i", "video.mp4",
        "-vframes", "1",
        "-q:v", "2",
        f"frame-{name}.jpg"
    ])
```

**结果**：提取 20 张关键帧

#### 3.4 生成图文笔记 HTML

**设计思路**：
- 参考学习网站风格（卡片式布局）
- 每个知识点配图
- 包含时间线索引
- 响应式设计（手机/电脑都能看）

**HTML 结构**：
```html
<!-- Hero 区域 -->
<div class="hero">
  <h1>RAG 工作机制详解</h1>
  <p>一个高质量知识库背后的技术全流程</p>
</div>

<!-- 内容区域 -->
<section class="wrap">
  <div class="card">
    <h3>为什么需要 RAG？</h3>
    <img src="assets/frame-003.jpg" alt="视频画面">
    <p>直接发文档给大模型的问题...</p>
  </div>
</section>
```

**CSS 样式要点**：
- 浅色背景（#fafaf7）
- 卡片阴影（box-shadow）
- 圆角边框（border-radius: 14px）
- 响应式布局（media query）

#### 3.5 首次部署（Cloudflare Pages）

**步骤**：
```bash
# 1. 登录 Cloudflare
wrangler login

# 2. 创建项目
wrangler pages project create rag-study-notes --production-branch main

# 3. 部署
wrangler pages deploy deploy/ --project-name rag-study-notes
```

**遇到的问题**：
- Cloudflare Pages 在国内访问不稳定
- `.pages.dev` 域名在部分地区被墙

**结果**：
- 部署成功：https://rag-study-notes.pages.dev
- 但国内访问体验不佳

---

### 阶段二：小红书版本尝试

#### 3.6 生成小红书风格图片

**需求**：
- 1080×1440 尺寸（3:4 比例）
- 适合小红书发布
- 避免版权问题（不用视频截图）

**实现**：
```python
from PIL import Image, ImageDraw, ImageFont

def create_slide(title, content, image_path):
    img = Image.new('RGB', (1080, 1440), '#0f172a')
    draw = ImageDraw.Draw(img)
    
    # 绘制标题
    font = ImageFont.truetype("msyh.ttc", 48)
    draw.text((60, 80), title, fill='#f8fafc', font=font)
    
    # 绘制内容卡片
    # ...
    
    img.save(f"slide-{title}.png")
```

**生成的 10 张卡片**：
1. 封面
2. 为什么需要 RAG
3. RAG 完整流程
4. 向量概念
5. Embedding 概念
6. 向量数据库
7. 分片+索引
8. 召回
9. 重排+生成
10. 总结

**遇到的问题**：
- 图片质量不够精美
- 用户反馈"有点丑"
- 尝试使用 `fireworks-tech-graph` skill 改进，但 SVG 转 PNG 工具安装失败

**结果**：
- 生成了 10 张卡片
- 但未达到预期效果
- 最终决定不使用小红书版本

#### 3.7 清理与简化

**决策**：
- 删除小红书版本
- 只保留初版 HTML（视频截图版）
- 简化部署结构

**操作**：
```bash
# 删除小红书相关文件
rm deploy/xiaohongshu.html
rm deploy/generate_images.py
rm -rf deploy/assets-new
rm -rf deploy/slides

# 恢复初版
mv deploy/original.html deploy/index.html
```

---

### 阶段三：迁移到 GitHub

#### 3.8 安装 gh CLI

**步骤**：
```bash
# Windows 使用 winget 安装
winget install GitHub.cli

# 验证安装
gh --version
# gh version 2.101.0
```

#### 3.9 GitHub 认证

**步骤**：
```bash
# 1. 启动登录流程
gh auth login --hostname github.com --git-protocol https --web

# 2. 浏览器打开 https://github.com/login/device
# 3. 输入一次性验证码
# 4. 授权完成
```

**遇到的问题**：
- 需要浏览器交互
- 验证码需要手动输入

**结果**：
- 登录账号：ytwangdongsheng
- Token 保存在 Windows 凭据管理器

#### 3.10 创建知识库仓库

**仓库结构设计**：
```
knowledge-hub/
├── README.md              # 总索引
├── index.html             # 门户首页
├── .nojekyll              # 关闭 Jekyll
├── rag/                   # 主题 1
│   ├── README.md
│   ├── index.html
│   └── assets/
└── <后续主题>/
```

**创建步骤**：
```bash
# 1. 创建本地目录
mkdir knowledge-hub
cd knowledge-hub

# 2. 初始化 git
git init -b main

# 3. 创建 GitHub 仓库
gh repo create knowledge-hub --public --source=. --push

# 4. 开启 GitHub Pages
gh api --method POST /repos/ytwangdongsheng/knowledge-hub/pages \
  -f "source[branch]=main" \
  -f "source[path]=/"
```

#### 3.11 配置 Git 身份

```bash
# 获取用户 ID
USER_ID=$(gh api user --jq .id)

# 配置 git（使用 GitHub noreply 邮箱）
git config --global user.name "ytwangdongsheng"
git config --global user.email "$USER_ID+ytwangdongsheng@users.noreply.github.com"
```

#### 3.12 部署第一个主题（RAG）

**步骤**：
```bash
# 1. 复制文件
cp -r Video/Downloads/study-qwen/deploy/* knowledge-hub/rag/

# 2. 创建主题 README
cat > knowledge-hub/rag/README.md << 'EOF'
# RAG 工作机制详解

检索增强生成的完整技术流程...
EOF

# 3. 更新门户首页
# 编辑 knowledge-hub/index.html，添加 RAG 卡片

# 4. 提交并推送
git add -A
git commit -m "docs: 初始化 knowledge-hub，新增 RAG 主题"
git push
```

**验证**：
- 等待 GitHub Pages 构建（约 1 分钟）
- 访问 https://ytwangdongsheng.github.io/knowledge-hub/rag/
- 确认页面正常显示

---

### 阶段四：第二个视频笔记（AI 编程）

#### 3.13 视频下载与转录

**目标视频**：B站 BV154426xEha《我的 AI 编程全流程》

**流程**：
1. 下载视频（68MB，24:54）
2. 提取音频
3. 转录（832 行）
4. 提取 11 张关键帧

**改进点**：
- 转录速度更快（faster-whisper 优化）
- 关键帧提取更精准（根据内容选择时间点）

#### 3.14 生成图文笔记

**内容结构**：
- 30 秒总览
- 选择编程助手
- 环境搭建（Git + agents.md）
- 产品设计（MVP 思维）
- 技术设计
- 产品实现
- 人工验证
- 总结回顾（5 步流程 + 3 个原则）
- 视频时间线
- 术语表

**HTML 特点**：
- 流程图展示 5 步工作流
- 表格对比不同工具
- 高亮框展示核心原则
- 时间线快速导航

#### 3.15 添加到知识库

**步骤**：
```bash
# 1. 创建主题目录
mkdir -p knowledge-hub/ai-coding-workflow/frames

# 2. 复制文件
cp study-notes.html knowledge-hub/ai-coding-workflow/index.html
cp frames/*.jpg knowledge-hub/ai-coding-workflow/frames/

# 3. 创建 README
cat > knowledge-hub/ai-coding-workflow/README.md << 'EOF'
# AI 编程全流程

如何用 AI 稳定交付高质量产品...
EOF

# 4. 更新门户
# 编辑 index.html，添加 AI 编程卡片

# 5. 更新总索引
# 编辑 README.md，添加新主题链接

# 6. 提交推送
git add -A
git commit -m "docs: 新增 AI 编程全流程主题"
git push
```

---

## 四、关键技术决策

### 4.1 为什么选择 GitHub Pages 而不是 Cloudflare Pages？

| 对比项 | Cloudflare Pages | GitHub Pages |
|--------|------------------|--------------|
| 国内访问 | 不稳定（.pages.dev 被墙） | 相对稳定（github.io） |
| 部署便利性 | 需要 wrangler CLI | git push 自动部署 |
| 与代码仓库集成 | 需要额外配置 | 天然集成 |
| 自定义域名 | 支持 | 支持 |
| 免费额度 | 充足 | 充足 |

**结论**：GitHub Pages 更适合个人知识库场景。

### 4.2 为什么用 faster-whisper 而不是 OpenAI Whisper？

| 对比项 | OpenAI Whisper | faster-whisper |
|--------|----------------|----------------|
| 安装大小 | ~2GB（含 torch） | ~200MB |
| 转录速度 | 慢 | 快（CTranslate2 优化） |
| 内存占用 | 高 | 低 |
| 准确率 | 高 | 相近 |

**结论**：faster-whisper 更适合本地使用。

### 4.3 为什么每个主题一个目录？

**优点**：
- 自包含：每个主题独立，互不干扰
- 易扩展：新增主题只需复制模板
- 易维护：修改某个主题不影响其他
- 易分享：可以单独分享某个主题的链接

**结构**：
```
主题目录/
├── README.md      # GitHub 上显示的说明
├── index.html     # 图文笔记正文
└── assets/        # 配图
```

---

## 五、遇到的问题与解决方案

### 5.1 视频下载问题

**问题**：yt-dlp 报错 "ffmpeg not found"

**解决**：
```bash
# 下载 ffmpeg
# https://www.gyan.dev/ffmpeg/builds/

# 放到 PATH 目录
cp ffmpeg.exe E:\python\Scripts\
```

### 5.2 转录质量问题

**问题**：whisper 转录有错别字（专业术语识别错误）

**解决**：
- 手动修正关键术语
- 使用正则表达式批量替换
- 建立术语表供后续使用

### 5.3 GitHub 认证问题

**问题**：git push 报错 "Authentication failed"

**解决**：
```bash
# 配置 gh 作为 git 凭证助手
gh auth setup-git

# 之后 git push 会自动使用 gh 的 token
```

### 5.4 GitHub Pages 构建问题

**问题**：推送后页面没有更新

**解决**：
- 检查 Actions 标签页，查看构建日志
- 确保 `.nojekyll` 文件存在（避免 Jekyll 处理）
- 等待构建完成（通常 1-2 分钟）

---

## 六、经验总结

### 6.1 工具选择原则

1. **优先选择轻量级工具**：faster-whisper > OpenAI Whisper
2. **优先选择集成度高的方案**：GitHub Pages > Cloudflare Pages
3. **优先选择标准化方案**：git + GitHub > 私有方案

### 6.2 内容组织原则

1. **一个主题一个目录**：便于管理和分享
2. **每个主题自包含**：HTML + 图片 + README
3. **统一的结构**：便于后续自动化处理

### 6.3 部署流程优化

**当前流程**：
```
本地编辑 → git commit → git push → GitHub Pages 自动构建
```

**优点**：
- 简单：只需 git 操作
- 自动：推送即部署
- 可追溯：所有变更都有记录

### 6.4 后续改进方向

1. **自动化生成**：
   - 输入视频链接 → 自动生成笔记
   - 使用 AI 辅助内容整理

2. **搜索功能**：
   - 添加全文搜索
   - 支持标签过滤

3. **多格式导出**：
   - 导出为 PDF
   - 导出为 Markdown

4. **评论系统**：
   - 集成 GitHub Discussions
   - 或第三方评论服务

---

## 七、附录

### 7.1 完整命令清单

```bash
# 视频下载
yt-dlp -o "video.mp4" --write-info-json "VIDEO_URL"

# 音频提取
ffmpeg -i video.mp4 -vn -acodec pcm_s16le -ar 16000 -ac 1 audio.wav

# 转录
python -c "
from faster_whisper import WhisperModel
model = WhisperModel('base', device='cpu', compute_type='int8')
segments, _ = model.transcribe('audio.wav', language='zh')
for seg in segments:
    print(f'[{seg.start:.1f}s - {seg.end:.1f}s] {seg.text}')
"

# 关键帧提取
ffmpeg -ss 30 -i video.mp4 -vframes 1 -q:v 2 frame.jpg

# GitHub 操作
gh auth login --web
gh repo create knowledge-hub --public
gh api --method POST /repos/USER/REPO/pages -f "source[branch]=main" -f "source[path]=/"

# Git 操作
git init -b main
git add -A
git commit -m "docs: 新增主题"
git push
```

### 7.2 文件模板

**主题 README.md 模板**：
```markdown
# 主题名称

> 一句话描述

**在线阅读**：https://ytwangdongsheng.github.io/knowledge-hub/THEME/

---

## 主题简介

...

## 文件说明

| 文件 | 说明 |
|------|------|
| `index.html` | 图文笔记正文 |
| `assets/` | 配图 |

## 来源

- 原视频：[链接]
- UP主：xxx
```

**门户卡片模板**：
```html
<a class="topic" href="THEME/" style="--tone:#COLOR">
  <div class="ico">EMOJI</div>
  <h3>主题名称</h3>
  <p class="desc">描述文字</p>
  <div class="tags">
    <span>标签1</span>
    <span>标签2</span>
  </div>
  <div class="go">阅读笔记 →</div>
</a>
```

### 7.3 参考资源

- [yt-dlp 文档](https://github.com/yt-dlp/yt-dlp)
- [faster-whisper 文档](https://github.com/guillaumekln/faster-whisper)
- [GitHub Pages 文档](https://docs.github.com/en/pages)
- [gh CLI 文档](https://cli.github.com/manual/)

---

## 八、结语

这个 knowledge-hub 项目从 0 到 1 经历了：
1. 视频下载与转录
2. 图文笔记生成
3. 部署方案探索（Cloudflare → GitHub）
4. 知识库结构设计
5. 第二个主题添加

整个过程使用了多种工具和技能，遇到了各种问题，但也积累了宝贵的经验。

希望这份文档能帮助到想要搭建类似知识库的朋友。

---

**文档版本**：v1.0  
**最后更新**：2026-09-21  
**作者**：AI 助手（基于用户操作记录整理）
