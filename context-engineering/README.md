# Context Engineering：概念与技术实现深度解析

> Context 是什么、Context Engineering 解决什么问题、又是怎么解决的

**在线阅读**：https://ytwangdongsheng.github.io/knowledge-hub/context-engineering/

---

## 主题简介

Context Engineering（上下文工程）是继 Prompt Engineering 之后的新概念。本期视频把它讲透：

- **Context 与 Context Window** —— 模型的输入 vs 输入的容量上限；Token 换算；主流模型窗口对比
- **三大现实问题** —— 为什么不能把所有资料一股脑丢给模型
- **Context Engineering 的定义** —— 核心思想：不改变模型的结构，只改变模型看到什么
- **为什么现在才火** —— 模型已足够强大 + Agent 兴起
- **四类实现方法** —— 保存 Context、选择 Context、压缩 Context、隔离 Context

## 结论速览

| 问题 | 结论 |
|------|------|
| Context | 模型的输入（用户问题、背景、资料、工具列表、工具结果、历史对话） |
| Context Window | 模型输入的容量上限，以 Token 数计 |
| Token 换算 | 1 Token ≈ 0.75 个单词 ≈ 1.5 个汉字 |
| 超限后果 | 前面的内容被丢弃，只保留最后 N 个 Token |
| 主流窗口 | Gemini 2.5 Pro 100 万 · GPT-5 40 万 · Claude 4 20 万 · Deepseek V3 12.8 万 |
| 三大问题 | 窗口有限 · 输入杂乱干扰理解 · 输入越多成本越高 |
| 核心思想 | 不改变模型的结构，只改变模型看到什么 |
| 为何现在火 | 模型够强了 + Agent 兴起（工具结果会占满窗口） |
| 四类方法 | 保存 · 选择 · 压缩 · 隔离 |
| 保存 | 筛选总结后落盘，需要时再注入；例：ChatGPT 记忆库 |
| 选择（静态） | 永远重要的信息每次全放；例：Cursor Rules、CLAUDE.md |
| 选择（动态） | 按问题挑最相关的；最著名的实现是 RAG |
| 压缩 | Claude Code 用量超 95% 触发 Auto Compact；可在 CLAUDE.md 自定义方案 |
| 隔离 | 不同模块 Context 互不干扰；例：Multi-Agent 的 Lead Agent 与 SubAgent |
| 定位 | 不是某一项具体技术，而是某一类技术的统称 |

## 文件说明

| 文件 | 说明 |
|------|------|
| `index.html` | 图文笔记正文（Template B v3） |
| `assets/` | 配图（19 张关键帧，截取自视频原片） |

## 来源与作者

- **原始视频**：[B站 BV11zbPzVEUe](https://www.bilibili.com/video/BV11zbPzVEUe) · 《Context Engineering：概念与技术实现深度解析》
- **UP主**：马克的技术工作坊（B站 UID：1815948385）
- **视频时长**：15:15
- **发布日期**：2025-08-10

### 视频中推荐的延伸阅读

| 文章 | 链接 |
|------|------|
| LangChain《Context Engineering》 | https://blog.langchain.com/context-engineering-for-agents/ |
| Cognition《Don't Build Multi-Agents》 | https://cognition.ai/blog/dont-build-multi-agents |

> 本笔记为学习用途的二次整理，配图截取自视频原片，内容版权归原作者所有。

## 相关主题

- [Harness Engineering 到底是什么？](../harness-engineering/) —— 同一作者的后续话题，文中提到「从 Prompt 到 Context 到 Harness」的层层递进
- [RAG 工作机制详解](../rag/) —— 动态选择最著名的实现方式
- [使用 Python 构建 RAG 系统](../rag-python/) —— RAG 的实战编码篇
