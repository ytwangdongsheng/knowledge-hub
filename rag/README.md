# RAG 工作机制详解

> 一个高质量知识库背后的技术全流程

**在线阅读**：https://ytwangdongsheng.github.io/knowledge-hub/rag/

---

## 主题简介

RAG（Retrieval Augmented Generation，检索增强生成）是目前最常用的 AI 问答方案之一。核心思想是 **先从知识库中检索相关内容，再基于这些内容生成答案** —— 即「先检索，再生成」。

企业内的知识助手、智能客服大多基于这项技术。

## 内容大纲

| 阶段 | 环节 | 说明 |
|------|------|------|
| 提问前 | ① 分片 Chunking | 把整份文档切成多个小片段 |
| 提问前 | ② 索引 Indexing | 片段经 Embedding 转成向量，连同原文写入向量数据库 |
| 提问后 | ③ 召回 Retrieval | 问题转成向量，用相似度粗筛出 Top 10 片段 |
| 提问后 | ④ 重排 Reranking | 用 Cross-Encoder 从 Top 10 精选出 Top 3 |
| 提问后 | ⑤ 生成 Generation | Top 3 片段 + 问题交给大模型，产出答案 |

## 核心概念

- **向量（Vector）**：一组数字，代表有大小有方向的量；维度 = 数字个数
- **Embedding**：把文本转换为向量的过程；语义相近 → 向量相近
- **向量数据库**：专门存储和查询向量，同时保存原始文本
- **向量相似度**：余弦相似度、欧氏距离、点积
- **Cross-Encoder**：重排阶段使用的高精度模型

## 文件说明

| 文件 | 说明 |
|------|------|
| `index.html` | 图文笔记正文，含 30 秒总览、核心概念、流程拆解、时间线、复盘问题、术语表 |
| `assets/` | 20 张视频关键帧配图 |

## 来源

- 原视频：B站 [BV1JLN2z4EZQ](https://www.bilibili.com/video/BV1JLN2z4EZQ)（时长 17:01）
- 笔记内容由 AI 根据视频转录整理，配图为视频关键帧截图
- 仅供学习交流，版权归原视频作者所有

## 相关术语速查

| 术语 | 英文 | 解释 |
|------|------|------|
| RAG | Retrieval Augmented Generation | 检索增强生成 |
| 分片 | Chunking | 文档切分为小片段 |
| 召回 | Retrieval | 粗筛出 Top K 相关片段 |
| 重排 | Reranking | 用精确模型精选 |
| Cross-Encoder | Cross-Encoder | 重排用的高准确率模型 |
| MTEB | Massive Text Embedding Benchmark | Embedding 模型评测排行榜 |
| 上下文窗口 | Context Window | 模型一次能处理的最大 Token 数 |
