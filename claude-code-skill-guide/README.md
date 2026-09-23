# Claude Code Skill 完全指南

> 手把手教你在 Claude Code 中安装和使用 Skill 技能

**在线阅读**：https://ytwangdongsheng.github.io/knowledge-hub/claude-code-skill-guide/

**原始文档**：https://ytwangdongsheng.github.io/knowledge-hub/claude-code-skill-guide/original/claude-code-skill-guide.pdf

---

## 主题简介

本篇是 PDF 文章《Claude Code Skill 完全指南》（32 页）的图文整理笔记，作者 @我是阿众，2026 年 4 月发布。

内容从 Skill 的基本概念出发，全面覆盖了安装、创建、触发、管理和生态：

- **Skill 是什么** —— 可复用的指令模板，把 Claude Code 从通用助手变成领域专家
- **核心特点** —— 可复用 · 可分享 · 自动触发
- **与 Plugin、MCP 的区别** —— Skill 定义流程，Plugin 是容器，MCP 定义连接
- **安装方式** —— 四层目录结构（企业级/用户级/项目级/插件级）、三种安装方法
- **创建自己的 Skill** —— SKILL.md 文件结构、Frontmatter 字段详解、正文编写指南
- **触发机制** —— 自动匹配（依赖 description）、手动斜杠命令、控制触发行为
- **管理方法** —— 查看已安装 Skill、优先级规则、临时停用
- **生态资源** —— 官方市场、第三方平台（skills.sh、agentskill.sh、Lobehub）、GitHub 社区
- **附录** —— Frontmatter 完整字段参考、内置斜杠命令速查、FAQ（10 个常见问题）

## 结论速览

| 问题 | 结论 |
|------|------|
| Skill 是什么 | 包含 SKILL.md 的目录，定义"怎么做"的可复用指令模板 |
| Skill 的核心特点 | 可复用 · 可分享 · 自动触发 |
| Skill 和 Plugin 的区别 | Skill 是单一能力模块，Plugin 是包含多个 Skill 的容器 |
| Skill 和 MCP 的区别 | Skill 定义流程/知识层，MCP 定义外部连接层 |
| Skill 文件放在哪 | 四层：企业级 > 用户级（~/.claude/skills/）> 项目级（.claude/skills/）> 插件级 |
| 怎么安装别人的 Skill | 三种方式：手动复制、npx skills 一键安装、安装插件 |
| 怎么创建自己的 Skill | 三种方式：手动编写 SKILL.md、让 Claude 生成、使用 /skill-creator |
| SKILL.md 的核心字段 | description（决定自动触发准确率，前 1536 字符有效） |
| 怎么触发 Skill | 自动匹配（依赖 description）+ 手动斜杠命令（/技能名） |
| 怎么控制触发行为 | disable-model-invocation: true（禁止自动）/ user-invocable: false（仅自动） |
| 去哪找更多 Skill | 官方市场、skills.sh、agentskill.sh、Lobehub、GitHub |
| 推荐的热门 Skill | find-skills、caveman、vercel-react-best-practices、document-skills |
| 怎么监控 token 消耗 | /cost 查看，精简 description，使用 caveman，清理不用的 Skill |

## 文件说明

| 文件 | 说明 |
|------|------|
| `index.html` | 图文笔记正文（Template B v3，CSS 与 `token-embedding/index.html` 逐字节一致） |
| `original/claude-code-skill-guide.pdf` | **原始文档**（PDF · 32 页 · 4.8 MB，原样保留） |

## 来源与作者

- **原始文档**：[Claude Code Skill 完全指南](original/claude-code-skill-guide.pdf)（本地 PDF，32 页）
- **作者**：@我是阿众（全网同名）
- **发布时间**：2026 年 4 月

> 本笔记为学习用途的二次整理，内容版权归原作者所有。

## 相关主题

- [一文讲透 Agent Skill](../agent-skill/) —— Agent 的能力扩展方式：SKILL.md 与渐进式披露
- [Agent 的概念、原理与构建模式](../agent-from-scratch/) —— 从零打造一个简化版 Claude Code
- [Context Engineering 深度解析](../context-engineering/) —— 同一作者：Agent 该「看到什么」
- [Harness Engineering 到底是什么？](../harness-engineering/) —— 从 Prompt 到 Context 再到 Harness 的演进
