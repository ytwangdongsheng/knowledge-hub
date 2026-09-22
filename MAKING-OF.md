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
- **当前主题**（4 个）：
  - RAG 工作机制详解（视频 · 17:01）
  - AI 编程全流程（视频 · 24:54）
  - 一文讲透 Agent Skill（PDF 文章 · 21 页）
  - 15 分钟弄懂 Token 和 Embedding（视频 · 15:17）
- **格式规范**：`STYLE.md`（含自动抽取与校验工具）
- **本地工作区**：`E:\个人知识积累`

---

## 二、技术栈与工具

### 2.1 核心工具

| 工具 | 用途 | 安装方式 |
|------|------|----------|
| **yt-dlp** | 下载 B站/YouTube 视频 | `pip install yt-dlp` |
| **ffmpeg** | 提取音频、提取关键帧 | 手动安装到 `E:\python\Scripts\` |
| **faster-whisper** | 语音转文字（本地转录） | `pip install faster-whisper` |
| **Pillow** | 生成图片、卡片 | `pip install Pillow` |
| **pymupdf** | 解析 PDF 正文与内嵌图片 | `pip install pymupdf` |
| **gh CLI** | GitHub 命令行工具 | `winget install GitHub.cli` |
| **git** | 版本控制 | 系统自带 |

### 2.2 DSH Skills 使用

| Skill | 用途 | 实际用法 |
|-------|------|----------|
| `z-video-downloader` | 视频下载 | ✅ 四篇视频全部用它下载 |
| `z-video-study-webpage-qwen` | 视频学习笔记 | ⚠️ 只借用了**流程思路**（转录 + 抽帧）；它自带的 HTML 生成器与最终样式完全不同，未使用 |
| `z-smart-xparse` | 文档解析 | ❌ 未用成：安装脚本 404，目录里也没有可执行文件，改用 pymupdf（2026-09-22 复查：`install.sh` / `install.ps1` 仍返回 404，npm 上也没有对应包，短期内无法安装） |
| `fireworks-tech-graph` | 技术图表生成 | ❌ 尝试过，最终未使用 |

> **关于 skill 与格式的关系**：knowledge-hub 的笔记格式**不是任何 skill 定义的**。`z-video-study-webpage-qwen` 目录里没有任何 HTML 模板文件，SKILL.md 里那句「沿用当前 study-summary.html 的视觉模板」是一条断掉的引用。真实来源是第一篇的成品文件，详见第四章。

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

### 阶段五：第一个文章笔记（Agent Skill）

前四篇输入都是视频，这一篇输入是一份 PDF 文章 —— **管线完全不同**。

#### 3.16 为什么需要新管线

| | 视频管线 | 文章管线 |
|---|---|---|
| 取正文 | faster-whisper 转录音频 | 直接抽取 PDF 文本层 |
| 取配图 | ffmpeg 按时间点抽帧 | 抽取 PDF 内嵌图片对象 |
| 中间产物 | `audio.wav` / `transcript.txt` | `article-text.txt` / `images/` |

视频管线要解决「把声音和画面变成文字」，文章管线要解决「把排版化的内容拆成文字和插图」。

#### 3.17 PDF 解析

用 **pymupdf**（PyMuPDF）逐页抽取文本与图片：

```python
import pymupdf
doc = pymupdf.open("article.pdf")
for page in doc:
    text = page.get_text()
    for img in page.get_images(full=True):
        pix = pymupdf.Pixmap(doc, img[0])
        pix.save(...)
```

**两个坑**：

1. `pip install pymupdf` 从 `files.pythonhosted.org` 下载超时 → 换清华镜像 `-i https://pypi.tuna.tsinghua.edu.cn/simple` 后成功
2. 提取出的图片扩展名与真实格式不符：`read_image` 报告 `image/jpeg`，但读文件头是 `89 50 4E 47`（真 PNG）→ **以文件头为准**，保留 `.png`

#### 3.18 图片筛选与重命名

原始提取 9 张图，其中 p13 / p14 / p15 是同一张三层的重复页 → 去重后保留 **8 张**，并按语义重命名：

```
p04-1.png → skill-md-metadata.png      （SKILL.md 的元数据部分）
p04-2.png → skill-md-instruction.png   （SKILL.md 的指令部分）
p06-1.png → skill-list.png
...
```

重命名的价值：HTML 里 `<img src="assets/skill-md-metadata.png">` 比 `p04-1.png` 可读得多，日后替换或排查能直接对应内容。

#### 3.19 结果

21 页 PDF → 11385 字符正文 → 8 张配图 → 11 个章节 + 术语表，原文全部章节保留。

---

### 阶段六：第四个视频笔记（Token 与 Embedding）

#### 3.20 下载与转录

**目标视频**：B站 BV1oNv8BPE2m《15分钟弄懂Token和Embedding》

- 时长 15:17，1080p，33.34 MB
- 转录 **344 段**（faster-whisper base / CPU / int8，耗时约 157 秒）
- 视频自带 6 个官方章节划分 → 时间线直接照搬，不用自己猜

**踩坑**：PowerShell 里 `yt-dlp --print` 输出的中文是 GBK 乱码，且重定向到文件会写成 UTF-16LE。

解法：不用 `--print`，改用 `-J` 输出 JSON（中文是 `\uXXXX` 转义），再用 Python 读：

```python
json.load(io.open('info.json', encoding='utf-8-sig'))
```

#### 3.21 抽帧策略：宁多勿少，再筛

这一篇的抽帧方法和前几篇不同：

```
按知识点密集处先抽 39 张候选
  → 逐张 read_image 肉眼确认
  → 剔除空白帧 / 过渡帧 / 重复
  → 最终入库 24 张
```

**为什么不一次抽准**：视频的动画节奏不可预测，只凭时间点猜很容易抽到过渡帧。先多抽再筛，比反复微调时间点更省事。

未使用的 15 张在后续清理阶段删除（释放 1.5 MB）。

#### 3.22 结果

6 章 / 24 张配图 / 46 KB HTML，含 30 秒总览、视频时间线、分章正文、一页速查、术语表。

---

### 阶段七：第五个文章笔记（Agent 的概念、原理与构建模式）

上一篇 PDF 有文本层，这一篇没有 —— 16 页**全是整页图片**，文章管线要再加一层「读图」。

#### 3.23 先按 skill 走，再换工具

按 `z-smart-xparse` 的默认路径先试：`xparse-cli` 未安装 → 按 SKILL.md 给的官方安装地址下载 → `install.ps1` / `install.sh` 双双 **HTTP 404**（Azure Blob 的 `ResourceNotFound`），npm 上也没有对应包。skill 自己规定「明确无法完成时，先说明原因再换工具」，于是回到文章管线的老办法：pymupdf。

用 pymupdf 抽文本只得到 **374 字符**（全是 `===== PAGE n =====` 标记）—— 确认这是一份纯图 PDF，文字都在图里。

#### 3.24 从整页图里切出插图

| | Agent Skill（第三篇） | 本篇 |
|---|---|---|
| PDF 文本层 | 有（11385 字符） | **无**（374 字符，只剩页标记） |
| 页面形态 | 图文混排（文字 + 内嵌插图对象） | **每页一张整页图**（1224×1584，16 张） |
| 取正文 | `page.get_text()` | 逐页用视觉读图 |
| 取配图 | 抽 PDF 内嵌图片对象 | 从整页图里**按版面裁剪** |

整页图不能直接当配图（会把正文一起贴进去），所以写脚本自动找截图块：

1. **特征**：截图行的「内容区中位数」< 255（截图底色不是纯白），正文行约为 255；
2. 用这个判据做行掩码 → 取连续区段 → 容差合并（图内允许少量纯白行）；
3. **裁掉图注**：图注是浅灰小字，中位数也是 255 → 从块的上下边缘剥掉；
4. **拆相邻两图**：块内出现 ≥14 行的纯白带就切开（第 8 页正好是两图紧邻）。

**踩坑**：第一版阈值取的是「暗像素占比 > 45%」，只找到 7 张 —— 那套判据只认 B站 的深色截图，代码窗口是浅色的，整批漏掉。换成中位数判据后补齐。

**旁证**：切出来的 16 个块尺寸**全部是 854×482**（正好 16:9），数量也和原文的 图 1-1 ~ 图 11-1 一一对应 —— 尺寸如此整齐，本身就是「切对了」的证据。

#### 3.25 原始文档入仓

这次多了一个要求：**原始文档也要放到 GitHub，点一下能跳回原文**。做法：

- 原文 PDF 原样放 `<主题名>/original/`（文件名用 ASCII，避免中文与空格进 URL）；
- 三处给链接：笔记页（30 秒总览的高亮框 + 页脚）、主题 `README.md`、仓库 `README.md` 的主题目录行；
- 顺手把它写进规范：`STYLE.md` §2 说明 `original/` 是可选目录，§9 检查清单加一条「三处链接都能打开原文」。

#### 3.26 结果

16 页纯图 PDF → 16 张配图（854×482 jpg，合计 1.0 MB）→ 13 个章节 + 一页速查 + 术语表，原文 11 个章节全部保留；CSS 仍是从 `token-embedding/index.html` 原样注入，`verify_style_spec.py` 输出 `identical : True`。

**版式自查**（`STYLE.md` §9 那条「桌面与手机各看一遍」这次做成了可复现的）：

- 用 headless Chrome 渲染整页，900px 与 390px 各切图肉眼过一遍；
- 390px 用一个 390px 宽的 iframe 包住页面来测（Chrome 的 `--window-size` 有最小窗口宽度，直接设 390 会得到一个 500px 的布局再裁掉右边，看起来像「内容被切掉」，其实是假象）；
- 在 iframe 里读 `documentElement.scrollWidth` 与 `clientWidth`：`375 / 375`，**overflow = false**，无横向滚动条。

---

## 四、格式规范体系（STYLE.md）

### 4.1 问题的由来

做到第三个主题时暴露了一个问题：**「格式统一」其实是假的**。

四篇笔记的实测配色与类名：

| 主题 | 模板 | 底色 / 主色 | 关键类名 |
|------|------|-------------|----------|
| `rag/` | Template A | `#f5f0e8` / `#2b6cb0` | `.container` `.header` `.section` |
| `ai-coding-workflow/` | B v1 | `#fafaf7` / `#2563eb` | `.wrap` `.hero` `.card` |
| `agent-skill/` | B v2 | 同 B | + `.compare` `.layers` |
| `token-embedding/` | B v3 | 同 B | + `.timeline` `.overview-grid` |

**根因**：格式从来没有被写成规范。真实机制是「读上一篇 → 抄它的 CSS → 换内容」——靠**制品复制**传递，而不是靠文档约定。

顺便排除一个误判：`z-video-study-webpage-qwen` 这个 skill **并没有**提供模板。它的目录里没有任何 HTML 文件，SKILL.md 里那句「沿用当前 `study-summary.html` 的视觉模板」是一条**断掉的引用**；它脚本自带生成器的 CSS 是宋体米色纸张风（`--paper:#f7f2ea` / `--ochre:#c4862f`），与实际发布的四篇一篇都对不上。

### 4.2 解决方案

新增 `STYLE.md`，把格式写成可执行的契约：

| 章节 | 内容 |
|------|------|
| §1 | 三条硬性约束（单文件自包含 / 只许追加类名 / 配图可追溯） |
| §3 | 主题色板 |
| §4 | 组件清单（14 个组件，标注各自首次出现的版本） |
| §5 | 页面骨架（可直接复制的 HTML 结构） |
| §6 | 规范 CSS（363 行） |
| §7 | 模板统一状态 + A→B 历史映射 |
| §8 | 内容要求清单 |
| §9 | 发布前检查命令 |

### 4.3 关键设计：规范不能手抄

文档与代码最大的风险是各说各话。所以 §6 的 CSS **不是手写的**，而由脚本从参考实装自动抽取：

```
token-embedding/index.html   ← 唯一可信源
        │  build_style_spec.py   （正则抽取 <style> 块）
        ▼
STYLE.md §6                  ← 规范附录（自动生成）
        │  verify_style_spec.py  （逐字节比对）
        ▼
   identical : True
```

两个脚本都用 `Path(__file__).resolve().parent` 定位仓库 —— 这带来一个意外好处：**后来整个文件夹改名 + 跨磁盘移动时，脚本完全不受影响**。

`build_style_spec.py` 内置幂等保护：`STYLE.md` 里的 `<!-- CANONICAL-CSS -->` 标记已被替换时会拒绝重复运行。

### 4.4 模板统一（2026-09-22）

把 `rag/` 从 Template A 迁移到 B v3：

1. 把 `token-embedding/index.html` 的 `<style>` 块**原样注入**（不手抄，保证与规范逐字节一致）
2. 正文按组件映射改写：

   | 旧 | 新 |
   |---|---|
   | `.header` | `.hero` |
   | `.container` + `.section` | `.wrap` + `section` + `.sec-head` |
   | `.knowledge-card` | `.card` + `.img-block` |
   | `.key-point` | `.highlight.{blue,green,orange,red,purple}` |
   | `.flow-step` | `.flow-item`（`.num` + `.sub-label`） |
   | `.comparison-table` | `table` |
   | `.time` / `.content` | `.t-time` / `.t-title` / `.t-desc` |
   | `.action-list` | 普通 `ul` / `ol` |

3. 校验：图片集合与迁移前一致（10 张）、标签全配平、CSS 逐字节相同、无 Template A 类名残留、时间线 14 项与原版一致
4. 顺带补齐了 §8 要求但原本缺失的「一页速查」

至此四个主题格式完全统一。

---

## 五、本地工作区治理

### 5.1 清理

第一次全量盘点：**673 个文件 / 421.62 MB**。分四类清理：

| 类别 | 体积 | 处理方式 |
|------|------|----------|
| ① 完全重复的副本 | ~51 MB | 删前逐个 **MD5 比对**，确认母本仍在才删 |
| ② 临时脚本与缓存 | ~5.1 MB | 含 `.wrangler/` 缓存（内有 Cloudflare account ID） |
| ③ 音频 `audio.wav` | ~104.8 MB | 转录文本已存，可一条 ffmpeg 命令重建 |
| ④ 视频 `.mp4` | ~225 MB | B站公开视频，URL 已记在笔记页脚 |

**关键做法：删前先保全证据。** 删掉下载目录前，先把 B站 `.info.json`（来源元数据）和 `download-report.md` 挪进工作目录；RAG 视频的 `.info.json` 保留（视频删除后它是本地仅存的来源记录）。

**两处刻意偏离清单**：

1. `study-qwen/deploy/assets/` 保留了 —— 它在重复清单里，但删了会让 `deploy/index.html` 的 20 张图全部断链
2. RAG 视频的 `.info.json` 保留，与 `ai-coding-workflow/video.info.json` 保持一致

**结果**：673 → 403 个文件，421.62 → 36.14 MB，**释放 385.48 MB（91.4%）**。

### 5.2 跨磁盘迁移

工作区从 `C:\Users\96122\Downloads\小红书` 改名为「个人知识积累」并移到 `E:\`。

**影响与应对**：

- 会话记录的默认工作目录失效 → 命令报 `spawn powershell.exe ENOENT`
  （不是 powershell 不见了，是工作目录不存在导致进程起不来）
- 应对：所有操作改用**显式 `workdir` + 绝对路径**
- **没有建目录联接（junction）**：那会在 Downloads 下复活一个名为「小红书」的文件夹，与改名的意图相悖

**迁移后全量验证**（8 项全部通过）：

| 检查项 | 结果 |
|--------|------|
| 四个主题配图 | 52 张引用，0 缺失 |
| git 仓库 | 工作区干净、remote 正确、HEAD 完整 |
| 规范工具链 | `identical : True`（靠 `__file__` 定位，不受移动影响） |
| skill 安装位置 | `~/.dsh/skills` 18 个完好（在用户目录，未随工作区移动） |
| 旧路径硬编码 | 无 |

**结论**：只要没有硬编码绝对路径，整个工作区可以任意改名、移动磁盘而不损坏。这也是当初把工具脚本改为 `Path(__file__).resolve().parent` 的回报。

---

## 六、关键技术决策

### 6.1 为什么选择 GitHub Pages 而不是 Cloudflare Pages？

| 对比项 | Cloudflare Pages | GitHub Pages |
|--------|------------------|--------------|
| 国内访问 | 不稳定（.pages.dev 被墙） | 相对稳定（github.io） |
| 部署便利性 | 需要 wrangler CLI | git push 自动部署 |
| 与代码仓库集成 | 需要额外配置 | 天然集成 |
| 自定义域名 | 支持 | 支持 |
| 免费额度 | 充足 | 充足 |

**结论**：GitHub Pages 更适合个人知识库场景。

### 6.2 为什么用 faster-whisper 而不是 OpenAI Whisper？

| 对比项 | OpenAI Whisper | faster-whisper |
|--------|----------------|----------------|
| 安装大小 | ~2GB（含 torch） | ~200MB |
| 转录速度 | 慢 | 快（CTranslate2 优化） |
| 内存占用 | 高 | 低 |
| 准确率 | 高 | 相近 |

**结论**：faster-whisper 更适合本地使用。

### 6.3 为什么每个主题一个目录？

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

## 七、遇到的问题与解决方案

### 7.1 视频下载问题

**问题**：yt-dlp 报错 "ffmpeg not found"

**解决**：
```bash
# 下载 ffmpeg
# https://www.gyan.dev/ffmpeg/builds/

# 放到 PATH 目录
cp ffmpeg.exe E:\python\Scripts\
```

### 7.2 转录质量问题

**问题**：whisper 转录有错别字（专业术语识别错误）

**解决**：
- 手动修正关键术语
- 使用正则表达式批量替换
- 建立术语表供后续使用

### 7.3 GitHub 认证问题

**问题**：git push 报错 "Authentication failed"

**解决**：
```bash
# 配置 gh 作为 git 凭证助手
gh auth setup-git

# 之后 git push 会自动使用 gh 的 token
```

### 7.4 GitHub Pages 构建问题

**问题**：推送后页面没有更新

**解决**：
- 检查 Actions 标签页，查看构建日志
- 确保 `.nojekyll` 文件存在（避免 Jekyll 处理）
- 等待构建完成（通常 1-2 分钟）

---

## 八、经验总结

### 8.1 工具选择原则

1. **优先选择轻量级工具**：faster-whisper > OpenAI Whisper
2. **优先选择集成度高的方案**：GitHub Pages > Cloudflare Pages
3. **优先选择标准化方案**：git + GitHub > 私有方案

### 8.2 内容组织原则

1. **一个主题一个目录**：便于管理和分享
2. **每个主题自包含**：HTML + 图片 + README
3. **统一的结构**：便于后续自动化处理

### 8.3 部署流程优化

**当前流程**：
```
本地编辑 → git commit → git push → GitHub Pages 自动构建
```

**优点**：
- 简单：只需 git 操作
- 自动：推送即部署
- 可追溯：所有变更都有记录

### 8.4 后续改进方向

1. **自动化生成**：🟡 部分实现
   - ✅ 输入链接 → 下载 → 转录 → 抽帧 → 生成笔记，流程已跑通 4 次
   - ✅ 格式已固化为 `STYLE.md`，不再靠「抄上一篇」
   - ⬜ 仍未脚本化：抽帧时间点、图片筛选、正文撰写目前靠人工判断

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

## 九、附录

### 9.1 完整命令清单

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

# PDF 解析（文章管线）
pip install pymupdf -i https://pypi.tuna.tsinghua.edu.cn/simple
python -c "
import pymupdf
doc = pymupdf.open('article.pdf')
for page in doc:
    print(page.get_text())
    for img in page.get_images(full=True):
        pix = pymupdf.Pixmap(doc, img[0])
        pix.save(f'images/p{page.number+1}.png')
"

# 获取视频元数据（避免 PowerShell 中文乱码：用 -J 输出 JSON）
yt-dlp -J "VIDEO_URL" > info.json
python -c "
import json,io
d = json.load(io.open('info.json', encoding='utf-8-sig'))
print(d['title'], d['duration'], d.get('chapters'))
"

# 格式规范维护
python build_style_spec.py    # 从参考实装重新生成 STYLE.md 的 CSS 附录
python verify_style_spec.py   # 期望输出 identical : True
```

### 9.2 文件模板

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

### 9.3 参考资源

- [yt-dlp 文档](https://github.com/yt-dlp/yt-dlp)
- [faster-whisper 文档](https://github.com/guillaumekln/faster-whisper)
- [GitHub Pages 文档](https://docs.github.com/en/pages)
- [gh CLI 文档](https://cli.github.com/manual/)

---

## 十、结语

这个 knowledge-hub 项目从 0 到 1 经历了：
1. 视频下载与转录
2. 图文笔记生成
3. 部署方案探索（Cloudflare → GitHub）
4. 知识库结构设计
5. 第二、三、四个主题添加（含一条完全不同的 PDF 文章管线）
6. 格式规范固化（`STYLE.md` + 自动抽取校验工具）
7. 四个主题模板统一
8. 本地工作区清理与跨磁盘迁移

整个过程使用了多种工具和技能，遇到了各种问题，但也积累了宝贵的经验。

**最大的教训**：「格式统一」如果只靠约定俗成、靠复制上一份制品，它一定会漂。只有把规范写成文件、并且让规范与实装之间有**自动校验**，才算真的固定下来。

希望这份文档能帮助到想要搭建类似知识库的朋友。

---

**文档版本**：v2.1  
**最后更新**：2026-09-22  
**作者**：AI 助手（基于用户操作记录整理）

**v2.1 变更**：新增「阶段七：第五个文章笔记（Agent 的概念、原理与构建模式）」；补充 z-smart-xparse 安装源复查结论；记录纯图 PDF 的切图方法与 `original/` 原始文档约定。  
**v2.0 变更**：补齐第 3、4 个主题；新增「格式规范体系」与「本地工作区治理」两章；更新命令清单与结语。
