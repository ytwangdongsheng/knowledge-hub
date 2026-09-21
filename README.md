# Knowledge Hub

个人知识库 · 按主题分目录整理，每个主题自带图文笔记与配图。

在线阅读（GitHub Pages）：**https://ytwangdongsheng.github.io/knowledge-hub/**

---

## 主题目录

| 主题 | 内容 | 在线阅读 |
|------|------|----------|
| **RAG 工作机制详解** | 检索增强生成的完整技术流程：分片 → 索引 → 召回 → 重排 → 生成 | [阅读](https://ytwangdongsheng.github.io/knowledge-hub/rag/) |

> 更多主题持续补充中。

---

## 仓库结构

```
knowledge-hub/
├── README.md            # 本文件：总索引
├── index.html           # 门户首页（GitHub Pages 入口）
├── .nojekyll            # 关闭 Jekyll 处理
├── rag/                 # 主题：RAG 工作机制详解
│   ├── README.md        # 主题说明
│   ├── index.html       # 图文笔记正文
│   └── assets/          # 配图
└── <主题名>/            # 后续主题按同样结构新增
    ├── README.md
    ├── index.html
    └── assets/
```

## 新增主题的方式

1. 新建 `<主题名>/` 目录
2. 放入 `index.html` 与 `assets/`
3. 写一份 `README.md` 说明主题内容
4. 在上方「主题目录」表格里加一行
5. 同步更新 `index.html` 门户首页的卡片

---

## 说明

- 本仓库为公开知识库，内容基于公开资料整理与二次加工
- 笔记中保留原始来源链接，便于追溯
- 图文配图来源见各主题 `README.md`

## License

内容采用 [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/deed.zh) 许可，转载请注明出处。
