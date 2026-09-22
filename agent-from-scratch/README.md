# Agent 的概念、原理与构建模式 —— 从零打造一个简化版的 Claude Code

> 大模型为什么需要 Agent？ReAct 循环、系统提示词、以及从零写一个能自己读写文件的 Agent

**在线阅读**：https://ytwangdongsheng.github.io/knowledge-hub/agent-from-scratch/

**原始文档**：https://ytwangdongsheng.github.io/knowledge-hub/agent-from-scratch/original/agent-concepts-and-building-patterns.pdf

---

## 主题简介

本篇是 PDF 文章《Agent 的概念、原理与构建模式 —— 从零打造一个简化版的 Claude Code》（16 页）的图文整理笔记，原文由 B站「马克的技术工作坊」的视频教程整理而来。

内容从「大模型的能力边界」出发，一路讲到亲手写一个可用的 ReAct Agent：

- **能力边界** —— 大模型能写代码，却查不到文件、写不了文件、改不了外部环境
- **Agent 是什么** —— 大模型 + 一堆工具 + 自动运行；工具是「感官与四肢」
- **常见类型** —— 编程类（Cursor）、PPT 类、深度搜索类（Manus），内核一致
- **ReAct 运行模式** —— Thought → Action → Observation →（循环）→ Final Answer
- **ReAct 的奥秘** —— 不是专门训练，而是系统提示词「安排剧本」；含五个组成部分
- **实战模拟** —— 用 DeepSeek 人工扮演工具，跑通一次 ReAct
- **动手实现** —— 逐行读懂简化版 Claude Code：`main()` / `ReActAgent` / `run()` 主循环
- **架构全景** —— 用户 / 主程序 / 模型 / 工具 四方如何协作
- **Plan & Execute** —— 另一种运行模式：先规划、再执行、动态 Replan
- **两种模式对比** —— 规划方式、适用场景、灵活性、典型产品

## 结论速览

| 问题 | 结论 |
|------|------|
| 大模型最大的限制 | 无法感知外界环境，也无法改变外部环境 |
| Agent 是什么 | 把大模型和一堆工具组装起来、能感知并改变外界环境的智能程序 |
| 三个基础工具 | 读写文件内容 · 查看文件列表 · 运行终端命令 |
| 不同 Agent 的共同点 | 大模型 + 工具 + 自动运行 |
| ReAct | Reasoning + Acting（思考与行动），2022 年 10 月论文提出，至今最广泛使用 |
| ReAct 四要素 | Thought（思考）→ Action（行动）→ Observation（观察）→ Final Answer（最终答案） |
| 谁在「先思考再行动」 | 系统提示词，不是模型被专门训练 |
| 系统提示词五部分 | 职责描述 · 示例 · 可用工具 · 注意事项 · 环境信息 |
| 工具是谁执行的 | 大模型只能「请求」调用，真正执行的是 Agent 的工具调用组件 |
| run() 主循环 | 请求模型 → 提取 thought → 检测 final answer → 解析并执行 action → 回填 observation → 循环 |
| Agent 的三个部分 | 模型（大脑）· 工具（四肢）· Agent 主程序（串联流程） |
| Plan & Execute 的四个模块 | Plan 模型 · Replan 模型 · 执行 Agent · Agent 主程序 |
| Replan 返回什么 | 「新的执行计划」或「最终答案」二选一 |
| 两种模式怎么选 | 步骤不固定、边做边看选 ReAct；目标清晰、可预先拆解选 Plan & Execute |

## 文件说明

| 文件 | 说明 |
|------|------|
| `index.html` | 图文笔记正文（Template B v3，CSS 与 `token-embedding/index.html` 逐字节一致） |
| `assets/` | 配图 16 张，对应原文 图 1-1 ~ 图 11-1，取自 PDF 原文插图 |
| `original/agent-concepts-and-building-patterns.pdf` | **原始文档**（PDF · 16 页 · 6.2 MB，原样保留） |

## 来源与作者

- **原始文档**：[Agent 的概念、原理与构建模式 —— 从零打造一个简化版的 Claude Code](original/agent-concepts-and-building-patterns.pdf)（本地 PDF，16 页）
- **原文整理自**：B站「马克的技术工作坊」视频教程（B站 UID：1815948385）
- **视频链接**：原文未给出对应的 B站 BV 号，此处留待补充（待核验）

> 本笔记为学习用途的二次整理，配图取自原文，内容版权归原作者所有。

## 相关主题

- [一文讲透 Agent Skill](../agent-skill/) —— Agent 的能力扩展方式：SKILL.md 与渐进式披露
- [Context Engineering 深度解析](../context-engineering/) —— 同一作者：Agent 该「看到什么」
- [Harness Engineering 到底是什么？](../harness-engineering/) —— 从 Prompt 到 Context 再到 Harness 的演进
- [AI 编程全流程](../ai-coding-workflow/) —— 用 AI 稳定交付产品的工作流
