# 使用 Python 构建 RAG 系统

> 用代码还原 RAG 系统的每个细节 —— 分片、索引、召回、重排、生成

**在线阅读**：https://ytwangdongsheng.github.io/knowledge-hub/rag-python/

---

## 主题简介

这是 RAG 系列的**实战篇**。上一期（[RAG 工作机制详解](../rag/)）讲清了 RAG 的原理，
本视频则把原理图上的每个环节自己写一遍代码，全程在 Jupyter Notebook 里逐段执行。

覆盖内容：

- **RAG 原理回顾** —— 准备部分（分片 + 索引）与回答部分（召回 + 重排 + 生成）
- **项目环境搭建** —— uv 初始化、四个依赖、用 uv 启动 Jupyter
- **分片** —— `split_into_chunks`，按空行切出 10 个片段
- **索引** —— `shibing624/text2vec-base-chinese` 生成 768 维向量，存入 ChromaDB
- **召回** —— `retrieve` 按向量相似度取 top-k
- **重排** —— CrossEncoder 重新打分，把答案片段排到第一
- **生成** —— 片段拼进 prompt，交给 `gemini-2.5-flash` 产出答案

## 结论速览

| 问题 | 结论 |
|------|------|
| 代码量 | 五个环节合计不到 50 行核心代码 |
| 分片 | 一行 `split("\n\n")` 即可 |
| Embedding | `shibing624/text2vec-base-chinese`，768 维，首次需下载约 400 MB |
| 向量库 | ChromaDB；内存 `EphemeralClient` / 落盘 `PersistentClient` |
| 召回的问题 | 向量相似度排序不准，答案片段没排第一 |
| 重排的价值 | CrossEncoder 把「问题+片段」成对编码，答案片段排到了第一 |
| 生成模型 | `gemini-2.5-flash`，免费额度，需 API Key |
| 最终验证 | 模型正确答出三件秘密道具，证明整条链路真实生效 |

**核心认知**：Embedding 是把问题和片段**分别**编码后比距离，两者从未「见过面」；
CrossEncoder 是把两者**拼在一起同时**编码，能直接建模交互关系，所以打分更准 ——
代价是必须对每个候选片段单独跑一次前向计算，只能用在召回之后的少量候选上。

## 文件说明

| 文件 | 说明 |
|------|------|
| `index.html` | 图文笔记正文（Template B v3） |
| `assets/` | 配图（22 张关键帧，截取自视频原片） |

## 来源与作者

- **原始视频**：[B站 BV1wc3izUEUb](https://www.bilibili.com/video/BV1wc3izUEUb) · 《使用Python构建RAG系统 —— 用代码还原 RAG系统的每个细节》
- **UP主**：马克的技术工作坊（B站 UID：1815948385）
- **视频时长**：17:30
- **发布日期**：2025-07-06
- **示例代码仓库**：[MarkTechStation/VideoCode](https://github.com/MarkTechStation/VideoCode)（目录：`用 Python 实现 RAG 系统`）

> 本笔记为学习用途的二次整理，配图截取自视频原片，内容版权归原作者所有。

## 系列说明

这是 RAG 系列的**实战篇**，前置内容是[RAG 工作机制详解](../rag/)（原理篇）。
