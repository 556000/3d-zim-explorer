# 🌌 3D ZIM Explorer — 时空导航

> 一个基于 3D 星图可视化的维基百科知识探索器，将词条之间的关系以星空连线的方式呈现，支持时空穿梭动画、LaTeX 数学公式渲染和多语言界面。

![版本](https://img.shields.io/badge/版本-0.95-blue)
![协议](https://img.shields.io/badge/协议-GPL%20v3-green)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![前端](https://img.shields.io/badge/前端-Three.js-orange)

[English Version](#english) | [简体中文](#简体中文)

---

## 🌠 项目简介

你是否曾想过，在星空中探索知识会是什么感觉？

**3D ZIM Explorer** 将维基百科词条转化为璀璨星图，中心是你正在阅读的词条，周围环绕着与之关联的知识节点，节点之间由优雅的弧线相连。当你点击跳转到另一个词条时，星空会化作光流，时空穿梭的视觉效果带你进入新的知识领域。

本项目离线运行，无需互联网连接，基于 ZIM 离线格式（由 [Kiwix](https://kiwix.org/) 提供）加载维基百科内容。

## ✨ 核心特性

| 特性 | 说明 |
|------|------|
| 🌠 **3D 知识星图** | 中心词条卡片 + 环绕关联节点 + 弧形连线 |
| 🚀 **时空穿梭动画** | 点击词条时星空加速拉丝，如同穿越虫洞 |
| 🧭 **导航面包屑** | 追踪浏览路径，随时回溯历史节点 |
| 🔢 **LaTeX 数学公式** | KaTeX 渲染，支持 `$$`、`\[...\]`、`\(...\)` 等多种格式 |
| 🔗 **维基超链接** | 正文内的链接可点击跳转，保持星图探索体验 |
| 🌐 **多语言界面** | 简体中文 / 繁体中文 / English，实时切换 |
| 📷 **词条缩略图** | 关联节点卡片展示词条配图 |
| 💡 **思路导出** | 将浏览路径导出为结构化笔记 |

## 🚀 快速开始

### 环境要求

- Python 3.10+
- [Kiwix](https://wiki.kiwix.org/wiki/Content) 下载的 Wikipedia ZIM 文件（中文维基推荐 `wikipedia_zh_all_maxi_*.zim`）

### 1. 安装依赖

```bash
pip install fastapi uvicorn libzim beautifulsoup4 zhconv
```

### 2. 配置 ZIM 文件路径

编辑 `zim-config.json`，填入你的 ZIM 文件路径：

```json
{
  "zim_path": "C:/path/to/wikipedia_zh_all_maxi_2025-04.zim"
}
```

### 3. 启动服务

```bash
python server.py
```

然后在浏览器打开 **http://localhost:8765**

或者直接双击运行：
- `启动.bat` — 一键启动服务并打开浏览器
- `start.bat` — 仅启动服务

## 🎮 操作指南

| 操作 | 效果 |
|------|------|
| 搜索 + 回车 | 搜索词条并展开知识星图 |
| 点击节点 | 查看词条摘要和关联内容 |
| 双击节点 | 以该词条为中心重新布局星图 |
| 鼠标拖拽 | 旋转视角 |
| 滚轮 | 缩放 |
| 右键拖拽 | 平移视角 |

## 🛠️ 技术栈

- **后端**：FastAPI + libzim + BeautifulSoup4
- **前端**：Three.js + OrbitControls + KaTeX
- **渲染方式**：纯 HTML/CSS/Canvas（无框架依赖）
- **数据来源**：ZIM 离线维基百科压缩包（来自 Kiwix）

## 📁 项目结构

```
3d-wiki-explorer/
├── server.py           # FastAPI 后端（ZIM 解析 + API）
├── index.html          # 单文件前端（HTML/CSS/JS）
├── three.min.js        # Three.js 3D 引擎
├── OrbitControls.js    # 相机控制
├── zim-config.json     # ZIM 文件路径配置
├── 启动.bat             # 一键启动
├── start.bat           # 仅启动服务
├── README.md           # 本说明文件
└── SPEC.md             # 设计规格文档
```

## 📜 协议

本项目采用 **GNU General Public License v3.0** 开源协议 — 详见 [LICENSE](LICENSE) 文件。

本项目使用 [libzim](https://github.com/openzim/libzim) 库访问 ZIM 文件，由 [Kiwix](https://kiwix.org/) 团队开发，特此致谢。

## 👤 作者

**陈驰 (Chen Chi)** — 来自中国·贵州·凯里

联系方式：12097652@QQ.com

GitHub：https://github.com/556000/3d-zim-explorer

Gitee：https://gitee.com/xarker/3d-zim-explorer

---

*时空导航，点亮探索之路* ✨

---

## English

**3D ZIM Explorer** is a 3D interactive Wikipedia knowledge graph explorer. Navigate the universe of knowledge with an immersive star-map visualization.

- 🌍 3D Knowledge Graph with orbiting nodes and arc connections
- 🚀 Warp-speed starfield animation during article navigation
- 🔢 KaTeX-powered LaTeX math rendering
- 🌐 Simplified Chinese / Traditional Chinese / English UI
- 📦 Offline-first: runs on ZIM files (no internet required)

### Quick Start

```bash
# Install
pip install fastapi uvicorn libzim beautifulsoup4 zhconv
python server.py
# Open http://localhost:8765
```