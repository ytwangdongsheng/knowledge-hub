# 15 分钟弄懂 Token 和 Embedding

> 详解 LLM 与 RAG 的数据处理机制

**在线阅读**：https://ytwangdongsheng.github.io/knowledge-hub/token-embedding/

---

## 主题简介

大模型明明可以直接"读"文字，为什么几乎所有 LLM 都要先把文字转成 **token**？为什么每张大模型架构图的最底部，都有一个 **Embedding** 层？而 RAG 里也有一个叫 embedding 的东西 —— 它们是一回事吗？

本期笔记沿着视频的推演链条，把这三个问题一次讲清：从**编号**到**语义**，从**预处理**到**模型内部**，从**文字接龙**到**对比学习**。

## 核心结论速览

| 问题 | 结论 |
|------|------|
| 为什么先转 token | 计算机里文字是离散字符，直接处理效率太低；用编号代表词/词片段更高效 |
| 词表大小的影响 | GPT-2 只有 50257，中文一字一 token，效率低；GPT-4o 的 `o200k_base` 有 20 万 |
| Tokenizer 是模型吗 | 不是。它是数据预处理，训练时固定不变 |
| 为什么需要 Embedding | 一维编号无法表达"既近又远"（香蕉 vs 苹果 vs Apple） |
| Embedding 能手工设计吗 | 不能。几千几万维必须训练出来，它是大模型的一部分 |
| 怎么实现的 | token → One-Hot（50257 维）→ Linear → embedding（1600 维） |
| RAG vs LLM Embedding | RAG 概括一整段话；LLM 打散一个 token。模型顶部未转化的输出≈RAG embedding |
| 训练方式差异 | LLM 是文字接龙；RAG 是对比学习（正样本拉近、负样本推远） |

## 视频章节

| 章节 | 时间 | 内容 |
|------|------|------|
| Token | 00:00 – 03:39 | 为什么转编号、词表与分词、Vocab Size 对中文的影响 |
| Token 的问题 | 03:39 – 05:42 | 大模型是连续函数，但一个编号表达不了"既近又远" |
| Embedding | 05:42 – 08:55 | 多个数描述一个词、维度与 d_model、为什么必须训练 |
| Embedding 实现 | 08:55 – 10:51 | One-Hot 编码 + 一层 Linear，以及模型末尾的逆操作 |
| RAG Embedding | 10:51 – 14:14 | 与 LLM Embedding 的区别、联系，以及对比学习 |
| 哲学 | 14:14 – 15:17 | 同一套架构，不同的经历，训练出独一无二的个体 |

## 文件说明

| 文件 | 说明 |
|------|------|
| `index.html` | 图文笔记正文，含 30 秒总览、视频时间线、六大章节、速查表、术语表 |
| `assets/` | 24 张视频关键帧配图 |

## 来源

- 原视频：B站 [BV1oNv8BPE2m](https://www.bilibili.com/video/BV1oNv8BPE2m)（时长 15:17）
- 标题：《15分钟弄懂Token和Embedding —— 详解LLM与RAG的数据处理机制》
- UP主：隔壁的程序员老王
- 笔记内容由 AI 根据视频转录（faster-whisper）整理，配图为视频关键帧截图
- 仅供学习交流，版权归原视频作者所有
