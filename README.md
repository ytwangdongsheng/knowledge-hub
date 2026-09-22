# Knowledge Hub

个人知识库 · 按主题分目录整理，每个主题自带图文笔记与配图。

在线阅读（GitHub Pages）：**https://ytwangdongsheng.github.io/knowledge-hub/**

---

## 主题目录

| 主题 | 内容 | 在线阅读 |
|------|------|----------|
| **RAG 工作机制详解** | 检索增强生成的完整技术流程：分片 → 索引 → 召回 → 重排 → 生成 | [阅读](https://ytwangdongsheng.github.io/knowledge-hub/rag/) |
| **使用 Python 构建 RAG 系统** | RAG 实战篇：手写分片、Embedding 索引、ChromaDB、召回、重排、生成 | [阅读](https://ytwangdongsheng.github.io/knowledge-hub/rag-python/) |
| **AI 编程全流程** | 如何用 AI 稳定交付高质量产品：5 步工作流 + 3 个原则 | [阅读](https://ytwangdongsheng.github.io/knowledge-hub/ai-coding-workflow/) |
| **一文讲透 Agent Skill** | 定义、目录结构、原理与实战思路：渐进式披露机制 + 与 MCP 的差异 | [阅读](https://ytwangdongsheng.github.io/knowledge-hub/agent-skill/) |
| **Token 与 Embedding** | LLM 与 RAG 的数据处理机制：从编号到语义、Embedding 实现、对比学习 | [阅读](https://ytwangdongsheng.github.io/knowledge-hub/token-embedding/) |
| **MCP 终极指南（基础篇）** | Model Context Protocol 核心概念、配置流程、交互机制、uvx/npx 安装 | [阅读](https://ytwangdongsheng.github.io/knowledge-hub/mcp-basics/) |
| **MCP 终极指南（进阶篇）** | 从零构建 MCP Server、抓包分析协议、终端直接交互、协议本质 | [阅读](https://ytwangdongsheng.github.io/knowledge-hub/mcp-advanced/) |
| **Harness Engineering 到底是什么？** | 概念演进、OpenAI/Anthropic 实战案例、争议讨论：过渡期的关键技术 | [阅读](https://ytwangdongsheng.github.io/knowledge-hub/harness-engineering/) |

> 更多主题持续补充中。

---

## 仓库结构

```
knowledge-hub/
├── README.md            # 本文件：总索引
├── STYLE.md             # 📐 笔记格式规范（新增主题前必读）
├── MAKING-OF.md         # 🛠️ 制作流程文档：工具链、六阶段全过程、经验教训
├── index.html           # 门户首页（GitHub Pages 入口）
├── .nojekyll            # 关闭 Jekyll 处理
├── build_style_spec.py  # 从参考实装抽取 CSS → 注入 STYLE.md
├── verify_style_spec.py # 校验 STYLE.md 的 CSS 与实装逐字节一致
├── rag/                 # 主题：RAG 工作机制详解
│   ├── README.md        # 主题说明
│   ├── index.html       # 图文笔记正文
│   └── assets/          # 配图
├── rag-python/          # 主题：使用 Python 构建 RAG 系统
│   ├── README.md        # 主题说明
│   ├── index.html       # 图文笔记正文
│   └── assets/          # 配图
├── ai-coding-workflow/  # 主题：AI 编程全流程
│   ├── README.md        # 主题说明
│   ├── index.html       # 图文笔记正文
│   └── frames/          # 配图
├── agent-skill/         # 主题：一文讲透 Agent Skill
│   ├── README.md        # 主题说明
│   ├── index.html       # 图文笔记正文
│   └── assets/          # 配图
├── token-embedding/     # 主题：Token 与 Embedding
│   ├── README.md        # 主题说明
│   ├── index.html       # 图文笔记正文
│   └── assets/          # 配图
├── mcp-basics/          # 主题：MCP 终极指南（基础篇）
│   ├── README.md        # 主题说明
│   ├── index.html       # 图文笔记正文
│   └── assets/          # 配图
├── mcp-advanced/        # 主题：MCP 终极指南（进阶篇）
│   ├── README.md        # 主题说明
│   ├── index.html       # 图文笔记正文
│   └── assets/          # 配图
├── harness-engineering/ # 主题：Harness Engineering 到底是什么？
│   ├── README.md        # 主题说明
│   ├── index.html       # 图文笔记正文
│   └── assets/          # 配图
└── <主题名>/            # 后续主题按同样结构新增
    ├── README.md
    ├── index.html
    └── assets/
```

## 新增主题的方式

**先读 [`STYLE.md`](STYLE.md)** —— 它定义了所有笔记的格式契约（色板、组件、页面骨架、发布前检查）。参考实装是 `token-embedding/index.html`。

1. 新建 `<主题名>/` 目录
2. 照 `STYLE.md` 的骨架写 `index.html`，配图放 `assets/`
3. 写一份 `README.md` 说明主题内容（简介 / 结论速览 / 文件说明 / 来源）
4. 在上方「主题目录」表格里加一行
5. 同步更新 `index.html` 门户首页的卡片与页脚链接
6. 按 `STYLE.md` §9 跑一遍发布前检查

---

## 说明

- 本仓库为公开知识库，内容基于公开资料整理与二次加工
- 笔记中保留原始来源链接，便于追溯
- 图文配图来源见各主题 `README.md`
- **笔记格式由 [`STYLE.md`](STYLE.md) 统一约定** —— 八个主题已全部统一到 Template B v3

## 相关文档

| 文档 | 面向 | 内容 |
|------|------|------|
| [`STYLE.md`](STYLE.md) | 写笔记的人 | 格式契约：色板、组件、页面骨架、发布前检查 |
| [`MAKING-OF.md`](MAKING-OF.md) | 想复刻这套流程的人 | 工具链、六个阶段的完整制作过程、关键技术决策、踩过的坑 |

## 维护格式规范

`STYLE.md` §6 的规范 CSS 不允许手改，由脚本从参考实装自动抽取，保证规范与实装不会互相漂移：

```bash
# 改完 token-embedding/index.html 的 CSS 后，重新生成规范
python build_style_spec.py

# 校验规范与实装是否逐字节一致
python verify_style_spec.py     # 期望输出 identical : True
```

脚本内置幂等保护：`STYLE.md` 里标记已被替换时会拒绝重复运行（需手动改回 `<!-- CANONICAL-CSS -->` 标记）。

## License

内容采用 [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/deed.zh) 许可，转载请注明出处。
