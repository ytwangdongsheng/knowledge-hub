# 笔记格式规范（STYLE.md）

本文件是 `knowledge-hub` 里所有主题笔记 **`index.html` 的唯一格式依据**。

> **参考实装**：`token-embedding/index.html`（Template B v3，组件最齐全的一篇）
> 新增主题时，**先读它**，再照本规范写内容。

---

## 0. 为什么需要这份文件

在写这份规范之前，格式是靠「读上一篇、抄它的 CSS」在传递的 —— 没有文件化依据，结果是：

| 主题 | 模板 | 漂移情况 |
|------|------|----------|
| `rag/` | **A → B v3** | 最早的一篇，自有命名体系；2026-09-22 已迁移完成 |
| `ai-coding-workflow/` | **B v1** | 换了一套命名体系（`.wrap` / `.hero` / `.card`） |
| `agent-skill/` | **B v2** | 追加 `.compare`、`.layers` |
| `token-embedding/` | **B v3** | 追加 `.timeline`、`.overview-grid` |
| `mcp-basics/` `mcp-advanced/` `harness-engineering/` `rag-python/` `context-engineering/` | **B v3** | 新增主题，CSS 与参考实装逐字节一致 |

**Template B v3 是本规范的基准，十一个主题现已全部统一。** 详见 §7。

从本文件开始，格式不再依赖「复制上一份制品」。

---

## 1. 三条硬性约束

1. **单文件自包含**：每个主题一个 `index.html`，CSS 全部内联在 `<style>` 里。不引外部 CSS/JS/字体/CDN。
2. **不破坏既有类名**：只能向 CSS 里**追加**新组件，不得重命名或删除已有类。旧页面必须继续正常渲染。
3. **图片来源可追溯**：配图只放在主题自己的 `assets/`（或 `frames/`）目录，页脚必须保留原始来源链接与版权归属。

---

## 2. 目录结构

每个主题一个自包含目录：

```
<主题名>/
├── README.md          # 主题说明：简介、结论速览、文件说明、来源
├── index.html         # 图文笔记正文（自包含单文件）
├── assets/            # 配图（也可用 frames/，同一主题内保持一致）
│   └── frame-*.jpg
└── original/          # 【可选】原始文档（PDF 等），原样保留
    └── *.pdf          # 仅在原始资料本身是本地文件时才有
```

**关于 `original/`**：当笔记整理自一份本地文档（如 PDF 文章）时，把原文**原样**放进 `original/`，文件名用 ASCII，并在三处给出可点击链接 —— 笔记页（hero 下方高亮框 + 页脚）、主题 `README.md`、门户卡片所在行的说明。这样读者读到任何一处都能一键跳回原文。视频类主题没有这个目录。

---

## 3. 主题色板（Template B）

```css
--bg: #fafaf7;            /* 页面底色，暖白 */
--card: #ffffff;          /* 卡片 */
--accent: #2563eb;        /* 主色，蓝 */
--accent-light: #dbeafe;  /* 主色浅背景 */
--green: #059669;  --green-light: #d1fae5;
--orange: #d97706; --orange-light: #fef3c7;
--red: #dc2626;    --red-light: #fee2e2;
--purple: #7c3aed; --purple-light: #ede9fe;
--text: #1f2937;   --text-dim: #6b7280;  --text-dimmer: #9ca3af;
--border: #e5e7eb;
--shadow: 0 1px 3px rgba(0,0,0,0.08);
```

**Hero 渐变**：`linear-gradient(135deg, #1e3a5f 0%, #2563eb 100%)`（深藏青 → 主蓝）

**字体栈**：系统无衬线，中文优先 PingFang SC / Microsoft YaHei

```css
font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC",
             "Microsoft YaHei", "Helvetica Neue", sans-serif;
```

**配色语义**（不要随意换）：蓝=定义/结论 · 绿=正确做法/澄清 · 橙=注意/反直觉 · 红=风险/错误 · 紫=补充说明/提醒

---

## 4. 组件清单

| 类名 | 用途 | 首次出现 |
|------|------|----------|
| `.hero` | 渐变横幅：`h1` + `p` 副标题 + `.meta` 来源元信息 | B v1 |
| `.wrap` / `section` | 内容容器，`section + section` 自动加上边框分隔 | B v1 |
| `.sec-head` | 章节标题：`h2`（含 `.emoji`）+ 一句 `p` 说明 | B v1 |
| `.card` | 内容卡片，最基础的承载单元 | B v1 |
| `.highlight.{blue,green,orange,red,purple}` | 高亮框；**首个 `<strong>` 自动块级**作为小标题 | B v1 |
| `.img-block` + `.cap` | 配图 + 带 emoji 的图注 | B v1 |
| `pre` / `code` | 深色代码块（`#1e293b`）/ 行内代码（粉字浅底） | B v1 |
| `.flow` + `.flow-item` + `.flow-arrow` | 水平流程步骤图 | B v1 |
| `table` | 数据表格，`th` 浅灰底 | B v1 |
| `.compare` + `.col.{left,right}` | 左右双栏对比 | B v2 |
| `.layers` + `.layer.{l1,l2,l3}` + `.pill` | 分层结构（左色条 + 标签胶囊） | B v2 |
| `.overview-grid` + `.overview-item` | 2×2 关键信息网格 | B v3 |
| `.timeline` + `.timeline-item` | 竖向时间线（`.t-time` / `.t-title` / `.t-desc`） | B v3 |
| `footer` | 来源与版权 | B v1 |

---

## 5. 页面骨架

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>主题名 — 图文学习笔记</title>
<meta name="description" content="一句话说明本页覆盖的知识点">
<style>
  /* ← 见 §6 规范 CSS，原样粘贴 */
</style>
</head>
<body>

<div class="hero">
  <h1>🍎 主题标题</h1>
  <p>副标题：本文覆盖的范围</p>
  <div class="meta">来源：B站 BV号 · 时长 · UP主 / 作者</div>
</div>

<section class="wrap">      <!-- 30 秒总览 -->
  <div class="sec-head"><h2><span class="emoji">⚡</span> 30 秒总览</h2><p>一句话</p></div>
  <div class="card">
    <div class="highlight blue"><strong>🎯 核心问题</strong>…</div>
    <div class="overview-grid">…</div>
  </div>
</section>

<section class="wrap">      <!-- 时间线（可选） -->
<section class="wrap">      <!-- 一、… （按原文/原视频章节，逐章展开） -->
<section class="wrap">      <!-- 一页速查 -->
<section class="wrap">      <!-- 术语表 -->

<footer>
  <p>🎬 本笔记根据视频内容整理 · 配图截取自视频原片</p>
  <p>原始视频：<a href="…">B站 BV号</a> · 《标题》 · UP主：…</p>
  <p><a href="../">← 返回知识库首页</a></p>
</footer>

</body>
</html>
```

**章节顺序固定为**：30 秒总览 → 视频/文章时间线（可选）→ 分章正文 → 一页速查 → 术语表 → 页脚

---

## 6. 规范 CSS（Template B v3）

> 本段由 `build_style_spec.py` 从 `token-embedding/index.html` **自动抽取**，与实装逐字节一致。修改规范时改源文件再重跑脚本，不要手改这里。

```css
  :root {
    --bg: #fafaf7;
    --card: #ffffff;
    --accent: #2563eb;
    --accent-light: #dbeafe;
    --green: #059669;
    --green-light: #d1fae5;
    --orange: #d97706;
    --orange-light: #fef3c7;
    --red: #dc2626;
    --red-light: #fee2e2;
    --purple: #7c3aed;
    --purple-light: #ede9fe;
    --text: #1f2937;
    --text-dim: #6b7280;
    --text-dimmer: #9ca3af;
    --border: #e5e7eb;
    --shadow: 0 1px 3px rgba(0,0,0,0.08);
  }
  * { box-sizing: border-box; margin: 0; padding: 0; }
  html { scroll-behavior: smooth; }
  body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC",
                 "Microsoft YaHei", "Helvetica Neue", sans-serif;
    background: var(--bg);
    color: var(--text);
    line-height: 1.8;
    -webkit-font-smoothing: antialiased;
  }

  /* Hero */
  .hero {
    background: linear-gradient(135deg, #1e3a5f 0%, #2563eb 100%);
    color: white;
    padding: 60px 24px 50px;
    text-align: center;
  }
  .hero h1 {
    font-size: clamp(26px, 4.6vw, 40px);
    font-weight: 800;
    margin-bottom: 16px;
    letter-spacing: -0.5px;
  }
  .hero p {
    font-size: clamp(15px, 2.5vw, 18px);
    opacity: 0.9;
    max-width: 640px;
    margin: 0 auto;
  }
  .hero .meta {
    margin-top: 20px;
    font-size: 14px;
    opacity: 0.75;
  }

  /* Layout */
  .wrap { max-width: 820px; margin: 0 auto; padding: 0 20px; }
  section { padding: 48px 0; }
  section + section { border-top: 1px solid var(--border); }

  /* Section headers */
  .sec-head { margin-bottom: 28px; }
  .sec-head h2 {
    font-size: clamp(22px, 4vw, 28px);
    font-weight: 700;
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 8px;
  }
  .sec-head h2 .emoji { font-size: 1.2em; }
  .sec-head p { color: var(--text-dim); font-size: 15px; }

  /* Sub heading */
  h3.sub {
    font-size: 18px;
    font-weight: 700;
    margin: 26px 0 12px;
    display: flex;
    align-items: center;
    gap: 8px;
  }

  /* Cards */
  .card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 24px;
    margin-bottom: 20px;
    box-shadow: var(--shadow);
  }
  .card h3 {
    font-size: 18px;
    font-weight: 700;
    margin-bottom: 12px;
    display: flex;
    align-items: center;
    gap: 8px;
  }
  .card p, .card li { font-size: 15px; color: var(--text); }
  .card p + p { margin-top: 10px; }
  .card ul, .card ol { padding-left: 22px; margin-top: 10px; }
  .card li + li { margin-top: 6px; }

  /* Highlight boxes */
  .highlight {
    border-radius: 12px;
    padding: 18px 22px;
    margin: 16px 0;
  }
  .highlight.blue { background: var(--accent-light); border-left: 4px solid var(--accent); }
  .highlight.green { background: var(--green-light); border-left: 4px solid var(--green); }
  .highlight.orange { background: var(--orange-light); border-left: 4px solid var(--orange); }
  .highlight.red { background: var(--red-light); border-left: 4px solid var(--red); }
  .highlight.purple { background: var(--purple-light); border-left: 4px solid var(--purple); }
  .highlight > strong:first-child { display: block; margin-bottom: 6px; }
  .highlight ul { margin-top: 6px; }

  /* Code blocks */
  pre {
    background: #1e293b;
    color: #e2e8f0;
    border-radius: 10px;
    padding: 18px 20px;
    overflow-x: auto;
    font-family: ui-monospace, "SF Mono", Menlo, Consolas, monospace;
    font-size: 13.5px;
    line-height: 1.7;
    margin: 16px 0;
  }
  pre code { color: inherit; background: none; padding: 0; }
  code {
    background: #f1f5f9;
    color: #db2777;
    padding: 2px 6px;
    border-radius: 5px;
    font-family: ui-monospace, "SF Mono", Menlo, Consolas, monospace;
    font-size: 0.9em;
  }

  /* Images */
  .img-block {
    margin: 20px 0;
    border-radius: 12px;
    overflow: hidden;
    border: 1px solid var(--border);
    box-shadow: var(--shadow);
    background: #fff;
  }
  .img-block img {
    width: 100%;
    display: block;
  }
  .img-block .cap {
    padding: 10px 14px;
    font-size: 13px;
    color: var(--text-dim);
    background: #f9fafb;
    border-top: 1px solid var(--border);
  }

  /* Flow diagram */
  .flow {
    display: flex;
    flex-wrap: wrap;
    gap: 12px;
    justify-content: center;
    align-items: center;
    margin: 24px 0;
  }
  .flow-item {
    background: var(--card);
    border: 2px solid var(--accent);
    border-radius: 12px;
    padding: 14px 20px;
    text-align: center;
    min-width: 110px;
    box-shadow: var(--shadow);
  }
  .flow-item .num {
    display: inline-block;
    width: 28px; height: 28px;
    line-height: 28px;
    border-radius: 50%;
    background: var(--accent);
    color: white;
    font-weight: 700;
    font-size: 14px;
    margin-bottom: 8px;
  }
  .flow-item .label {
    font-size: 14px;
    font-weight: 600;
  }
  .flow-item .sub-label {
    font-size: 12px;
    color: var(--text-dim);
    margin-top: 2px;
  }
  .flow-arrow {
    display: flex;
    align-items: center;
    color: var(--text-dimmer);
    font-size: 20px;
  }

  /* Overview grid */
  .overview-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 14px;
    margin: 18px 0;
  }
  .overview-item {
    background: var(--accent-light);
    border-radius: 12px;
    padding: 16px 18px;
    border-left: 4px solid var(--accent);
  }
  .overview-item .label {
    font-size: 12px;
    color: var(--text-dim);
    letter-spacing: 0.4px;
  }
  .overview-item .value {
    font-size: 15px;
    font-weight: 600;
    margin-top: 4px;
  }

  /* Layers */
  .layers { margin: 22px 0; }
  .layer {
    border-radius: 12px;
    padding: 18px 20px;
    margin-bottom: 14px;
    border-left: 5px solid;
    background: var(--card);
    box-shadow: var(--shadow);
  }
  .layer.l1 { border-left-color: #f59e0b; }
  .layer.l2 { border-left-color: var(--accent); }
  .layer.l3 { border-left-color: var(--green); }
  .layer .layer-title {
    font-weight: 700;
    font-size: 16px;
    margin-bottom: 6px;
    display: flex;
    align-items: center;
    gap: 10px;
    flex-wrap: wrap;
  }
  .layer .pill {
    font-size: 11.5px;
    font-weight: 600;
    padding: 2px 10px;
    border-radius: 999px;
    background: #f1f5f9;
    color: var(--text-dim);
  }
  .layer p { font-size: 14.5px; color: var(--text-dim); }

  /* Table */
  table {
    width: 100%;
    border-collapse: collapse;
    margin: 16px 0;
    font-size: 14px;
  }
  th, td {
    padding: 12px 14px;
    text-align: left;
    border-bottom: 1px solid var(--border);
    vertical-align: top;
  }
  th {
    background: #f9fafb;
    font-weight: 600;
    color: var(--text-dim);
    font-size: 13px;
    letter-spacing: 0.3px;
  }
  tr:hover td { background: #fafafa; }

  /* Two column compare */
  .compare {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 16px;
    margin: 20px 0;
  }
  .compare .col {
    border-radius: 12px;
    padding: 18px 20px;
    border: 1px solid var(--border);
    background: var(--card);
  }
  .compare .col h4 {
    font-size: 16px;
    font-weight: 700;
    margin-bottom: 10px;
    display: flex;
    align-items: center;
    gap: 8px;
  }
  .compare .col.left { border-top: 3px solid var(--purple); }
  .compare .col.right { border-top: 3px solid var(--green); }
  .compare .col ul { padding-left: 20px; }
  .compare .col li { font-size: 14px; margin-bottom: 5px; }

  /* Timeline */
  .timeline { position: relative; margin: 22px 0; padding-left: 26px; }
  .timeline::before {
    content: '';
    position: absolute;
    left: 5px; top: 6px; bottom: 6px;
    width: 2px;
    background: var(--border);
  }
  .timeline-item {
    position: relative;
    margin-bottom: 16px;
  }
  .timeline-item::before {
    content: '';
    position: absolute;
    left: -26px; top: 9px;
    width: 12px; height: 12px;
    border-radius: 50%;
    background: var(--accent);
    border: 2px solid var(--bg);
  }
  .timeline-item .t-time {
    font-size: 12.5px;
    font-weight: 700;
    color: var(--accent);
    font-family: ui-monospace, Menlo, Consolas, monospace;
  }
  .timeline-item .t-title { font-size: 15px; font-weight: 600; }
  .timeline-item .t-desc { font-size: 14px; color: var(--text-dim); }

  /* Footer */
  footer {
    border-top: 1px solid var(--border);
    padding: 32px 20px;
    text-align: center;
    color: var(--text-dimmer);
    font-size: 13px;
  }
  footer a { color: var(--accent); text-decoration: none; }
  footer p + p { margin-top: 6px; }

  @media (max-width: 640px) {
    .hero { padding: 40px 16px 36px; }
    section { padding: 32px 0; }
    .card { padding: 18px; }
    .flow { flex-direction: column; }
    .flow-arrow { transform: rotate(90deg); }
    .compare { grid-template-columns: 1fr; }
    .overview-grid { grid-template-columns: 1fr; }
    pre { font-size: 12.5px; padding: 14px; }
  }
```

---

## 7. 模板统一状态

**十一个主题已全部统一到 Template B v3**，不再存在偏差：

| 主题 | 状态 |
|------|------|
| `rag/` | ✅ 2026-09-22 从 Template A 迁移完成 |
| `ai-coding-workflow/` | ✅ B v1 起即符合 |
| `agent-skill/` | ✅ B v2 |
| `token-embedding/` | ✅ B v3（参考实装） |
| `mcp-basics/` | ✅ B v3 |
| `mcp-advanced/` | ✅ B v3 |
| `harness-engineering/` | ✅ B v3 |
| `rag-python/` | ✅ B v3 |
| `context-engineering/` | ✅ B v3 |
| `agent-from-scratch/` | ✅ B v3（含可选 `original/` 原始文档） |
| `claude-code-skill-guide/` | ✅ B v3（含可选 `original/` 原始文档） |

迁移方式：把 `token-embedding/index.html` 的 `<style>` 块**原样注入**（保证与规范逐字节一致），正文按下面的映射改写。

<details>
<summary>Template A → B 的历史映射（仅供理解旧版本，现行不再使用）</summary>

| | Template A（旧 `rag/`） | Template B v3（现行基准） |
|---|---|---|
| 容器 | `.container`（max 960px） | `.wrap`（max 820px） |
| 横幅 | `.header`，圆角底部 | `.hero`，通栏 |
| 章节 | `.section` 独立卡片 | `.wrap` + `section` 边框分隔 |
| 底色 / 主色 | `#f5f0e8` / `#2b6cb0` | `#fafaf7` / `#2563eb` |
| Hero 渐变 | `#2b6cb0 → #4c51bf` | `#1e3a5f → #2563eb` |
| 知识点卡 | `.knowledge-card` | `.card` + `.img-block` |
| 流程步骤 | `.flow-step`（绿/橙分类） | `.flow-item`（`.num` + `.sub-label`） |
| 要点框 | `.key-point` | `.highlight.{blue,green,orange,red,purple}` |
| 表格 | `.comparison-table` | `table` |
| 时间线 | `.time` / `.content` | `.t-time` / `.t-title` / `.t-desc` |
| 清单 | `.action-list` | 普通 `ul` / `ol` |

</details>

新增主题一律按 Template B v3。

---

## 8. 内容要求

一份合格的笔记必须：

- [ ] 覆盖原文/原视频的**全部章节**，不丢主要内容；章节标题与原文可对应
- [ ] 有 **30 秒总览**，让人不读全文也知道讲了什么
- [ ] 有关键配图，且每张图与所在段落的知识点**语义对应**（不做装饰性插图）
- [ ] 有**术语表**，覆盖文中的关键概念
- [ ] 有一页速查表（问题 → 结论），可独立使用
- [ ] 页脚保留**原始来源链接**与版权归属
- [ ] 不确定的内容标注「待核验」，不伪装成事实

**不要**：只根据标题泛泛总结；只截几张图写空泛结论；为了排版好看而丢内容。

---

## 9. 发布前检查

```powershell
cd knowledge-hub/<主题名>

# 1. 所有图片引用都能解析，且没有未使用的图
$html = Get-Content index.html -Raw -Encoding UTF8
$refs = [regex]::Matches($html, 'src="(assets/[^"]+)"') |
        ForEach-Object { $_.Groups[1].Value } | Sort-Object -Unique
foreach ($r in $refs) { if (-not (Test-Path $r)) { "MISSING: $r" } }
Get-ChildItem assets -Filter *.jpg |
  Where-Object { $refs -notcontains "assets/$($_.Name)" } |
  ForEach-Object { "UNUSED: $($_.Name)" }

# 2. 标签配平
foreach ($t in @('section','div','table','ul','pre','footer')) {
  $o = ([regex]::Matches($html, "<$t[ >]")).Count
  $c = ([regex]::Matches($html, "</$t>")).Count
  "$t : $o / $c"      # 两个数必须相等
}
```

再加三项人工核对：

- [ ] 已在门户 `index.html` 加卡片、在 `README.md` 主题目录表加一行、页脚链接加一项
- [ ] 桌面（900px）与手机（390px）各看一遍，无横向滚动条
- [ ] 若主题带 `original/`：笔记页与页脚的原文档链接、主题 README 链接、仓库 README 链接三处都能打开原文

确认后：

```powershell
git add -A
git commit -m "docs: 新增 <主题名> 主题笔记"
git push
gh api repos/ytwangdongsheng/knowledge-hub/pages/builds/latest --jq '{status,error}'
```
