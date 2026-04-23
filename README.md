# 🌌 3D ZIM Explorer — 时空导航

<p align="center">
  <strong>在星空中探索知识 — 维基百科 3D 可视化知识图谱</strong>
</p>

<p align="center">
  <a href="#-预览">预览</a> •
  <a href="#-核心特性">特性</a> •
  <a href="#-快速开始">快速开始</a> •
  <a href="#-技术栈">技术栈</a> •
  <a href="#english">English</a>
</p>

<p align="center">
  <img src="screenshots/welcome.png" alt="欢迎页" width="800">
</p>

---

## 🖼️ 预览

### 🌠 3D 知识星图

搜索任意词条，即刻展开璀璨的知识星空。中心卡片展示当前词条，周围环绕着关联知识节点，弧线勾勒出概念之间的内在联系。

<p align="center">
  <img src="screenshots/starmap.png" alt="3D 知识星图" width="900">
</p>

### 📄 词条详情与公式渲染

点击节点或展开全文，查看完整词条内容。LaTeX 数学公式自动渲染，维基超链接保持可交互。

<p align="center">
  <img src="screenshots/article.png" alt="词条详情与公式渲染" width="700">
</p>

> 💡 **时空穿梭**：点击任意关联节点，星空化作光流拉丝，如同穿越虫洞般进入新的知识领域。

---

## ✨ 核心特性

| 特性 | 说明 |
|------|------|
| 🌠 **3D 知识星图** | 中心词条卡片 + 环绕关联节点（带缩略图）+ 弧形连线 |
| 🚀 **时空穿梭动画** | 点击跳转时星空加速拉丝，沉浸式虫洞穿越体验 |
| 🔢 **LaTeX 数学公式** | KaTeX 渲染，支持 `$$`、`\[...\]`、`\(...\)`、`{\displaystyle}` 等 |
| 🔗 **维基超链接** | 正文内链接可点击跳转，无缝衔接星图探索 |
| 🧭 **导航面包屑** | 追踪浏览路径，随时回溯历史节点 |
| 🌐 **多语言界面** | 简体中文 / 繁体中文 / English 一键切换 |
| 💡 **思路导出** | 将浏览路径导出为 Markdown 结构化笔记 |
| 📦 **完全离线** | 基于 ZIM 文件运行，无需互联网连接 |

---

## 🚀 快速开始

### 环境要求

- Python 3.10+
- [Kiwix Wikipedia ZIM 文件](https://wiki.kiwix.org/wiki/Content)（中文推荐 `wikipedia_zh_all_maxi_*.zim`）

### 安装 & 启动（三步）

```bash
# 1. 克隆项目
git clone https://github.com/556000/3d-zim-explorer.git
cd 3d-zim-explorer

# 2. 安装依赖
pip install fastapi uvicorn libzim beautifulsoup4 zhconv

# 3. 配置 ZIM 文件路径
# 编辑 zim-config.json，填入你的 ZIM 文件路径

# 4. 启动
python server.py
# 浏览器打开 http://localhost:8765
```

> 💡 Windows 用户可直接双击 `启动.bat` 一键启动。

### 操作指南

| 操作 | 效果 |
|------|------|
| 🔍 搜索 + 回车 | 搜索词条并展开知识星图 |
| 👆 单击节点 | 查看词条摘要和关联内容 |
| 👆👆 双击节点 | 以该词条为中心重新布局星图 |
| 🖱️ 鼠标拖拽 | 旋转 3D 视角 |
| 🔄 滚轮 | 缩放 |
| ➡️ 右键拖拽 | 平移视角 |

---

## 🛠️ 技术栈

| 层级 | 技术 |
|------|------|
| **后端** | FastAPI + libzim + BeautifulSoup4 + zhconv |
| **3D 引擎** | Three.js (Canvas 星空背景) |
| **前端** | 原生 HTML/CSS/JS（无框架依赖） |
| **数学渲染** | KaTeX |
| **数据源** | ZIM 离线维基百科（来自 [Kiwix](https://kiwix.org/)） |

```
3d-wiki-explorer/
├── server.py           # FastAPI 后端（ZIM 解析 + API）
├── index.html          # 单文件前端（HTML/CSS/JS 全合一）
├── three.min.js        # Three.js 3D 引擎
├── OrbitControls.js    # 相机控制
├── zim-config.json     # ZIM 文件路径配置
├── 启动.bat             # Windows 一键启动
└── start.bat           # Windows 仅启动服务
```

---

## 📋 更新日志

### v0.952 (2026-04-23)

- 🔧 **修复 PyInstaller zhconv 数据文件缺失**：spec 文件添加 `zhconv` 数据文件打包
- 📦 **EXE 打包完善**：移除 tkinter 依赖，简化为纯路径输入 + ZIM 路径预填
- 📝 **输入框 UX 优化**：ZIM 输入窗口从 480px 增大至 680px，字体提升至 15px
- 🧩 **打包体验提升**：自动打开浏览器，内置默认路径提示，开箱即用

### v0.951 (2026-04-22)

- 🔧 **修复 renderMath 链路丢失**：TOKEN 占位符机制，KaTeX 不再破坏 `.wiki-link` DOM
- ⚡ **物理引擎重构**：空间哈希网格 O(n) 碰撞检测，能量阈值提前终止
- 🧹 **内存管理完善**：缩略图请求 stale 检测 + one-shot 回调防 DOM 泄漏
- 🎨 **动态连线**：SVG 路径池每帧仅更新 `d` 属性，零 DOM 删建
- 🪟 **响应式布局**：resize 时 lerp 平滑过渡，无位置跳变

### v0.95 (2026-04-22)

- 🎉 初始发布：3D 知识星图 + 时空穿梭动画 + KaTeX 公式 + 多语言 + 面包屑导航 + 思路导出

---

## 📜 协议

[GNU GPL v3.0](LICENSE) · 使用 [libzim](https://github.com/openzim/libzim) 库 · 致谢 [Kiwix](https://kiwix.org/)

## 👤 作者

**陈驰 (Xarker)** — 中国·贵州·凯里

📧 12097652@QQ.com · [GitHub](https://github.com/556000/3d-zim-explorer) · [Gitee](https://gitee.com/xarker/3d-zim-explorer)

---

*时空导航，点亮探索之路* ✨

---

---

## English

# 🌌 3D ZIM Explorer — Knowledge Navigator

<p align="center">
  <strong>Explore knowledge among the stars — 3D Wikipedia visualization</strong>
</p>

<p align="center">
  <a href="#preview">Preview</a> •
  <a href="#features">Features</a> •
  <a href="#quick-start">Quick Start</a> •
  <a href="#tech-stack">Tech Stack</a>
</p>

<p align="center">
  <img src="screenshots/welcome.png" alt="Welcome Page" width="800">
</p>

---

## 🖼️ Preview

### 🌠 3D Knowledge Star Map
Search for any topic and instantly unfold a brilliant knowledge starfield. The central card shows the current article, surrounded by related nodes with curved connections linking concepts.

<p align="center">
  <img src="screenshots/starmap.png" alt="3D Knowledge Star Map" width="900">
</p>

### 📄 Article Details & Math Rendering
Click nodes or expand full text to view complete article content. LaTeX math formulas render automatically, and Wikipedia hyperlinks remain interactive.

<p align="center">
  <img src="screenshots/article.png" alt="Article Details & Math Rendering" width="700">
</p>

> 💡 **Warp Navigation**: Click any related node and the starfield stretches into light streams, like traversing a wormhole into a new knowledge domain.

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🌠 **3D Knowledge Graph** | Central article card + orbiting related nodes (with thumbnails) + arc connections |
| 🚀 **Warp Animation** | Starfield accelerates into light streaks when jumping for immersive wormhole experience |
| 🔢 **KaTeX Math** | Full LaTeX support: `$$`, `\[...\]`, `\(...\)`, `{\displaystyle}`, `{\textstyle}` |
| 🔗 **Clickable Wiki Links** | In-text links trigger seamless star-map transitions |
| 🧭 **Breadcrumb Nav** | Track your exploration path, revisit historical nodes anytime |
| 🌐 **Multi-language** | Simplified Chinese / Traditional Chinese / English one-click toggle |
| 💡 **Idea Export** | Export browsing path as structured Markdown notes |
| 📦 **Full Offline** | Runs entirely on ZIM files, no internet required |
| 🖥️ **EXE Distribution** | Standalone Windows EXE with auto browser open (v0.952+) |

---

## 🚀 Quick Start

### Option 1: EXE (Windows Only, v0.952+)
1. Download latest `3D-ZIM-Explorer-v0.952.zip` from Releases
2. Extract anywhere
3. Double-click `3D-ZIM-Explorer.exe`
4. Paste your ZIM file path (default pre-filled for convenience)
5. Click "Load" and start exploring

### Option 2: Source (All Platforms)

#### Requirements
- Python 3.10+
- [Kiwix Wikipedia ZIM file](https://wiki.kiwix.org/wiki/Content) (for Chinese, try `wikipedia_zh_all_maxi_*.zim`)

#### Installation & Launch (4 Steps)

```bash
# 1. Clone repo
git clone https://github.com/556000/3d-zim-explorer.git
cd 3d-zim-explorer

# 2. Install dependencies
pip install fastapi uvicorn libzim beautifulsoup4 zhconv

# 3. Configure ZIM path (optional)
# Edit zim-config.json with your ZIM file path

# 4. Launch
python server.py
# Then open http://localhost:8765 in your browser
```

> 💡 Windows users can double-click `启动.bat` for one-click startup.

### Controls

| Action | Effect |
|--------|--------|
| 🔍 Search + Enter | Search article and unfold knowledge graph |
| 👆 Click node | View article summary and related content |
| 👆👆 Double-click | Re-center graph on that article |
| 🖱️ Drag | Rotate 3D view |
| 🔄 Scroll wheel | Zoom in/out |
| ➡️ Right drag | Pan view |

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|------------|
| **Backend** | FastAPI + libzim + BeautifulSoup4 + zhconv |
| **3D Engine** | Three.js (Canvas starfield background) |
| **Frontend** | Vanilla HTML/CSS/JS (no framework dependencies) |
| **Math Rendering** | KaTeX |
| **Data Source** | ZIM offline Wikipedia (from [Kiwix](https://kiwix.org/)) |

```
3d-wiki-explorer/
├── server.py           # FastAPI backend (ZIM parsing + APIs)
├── index.html          # Single-file frontend (HTML/CSS/JS all-in-one)
├── three.min.js        # Three.js 3D engine
├── OrbitControls.js    # Camera controls
├── zim-config.json     # ZIM file path config (for source mode)
├── 启动.bat             # Windows one-click start
└── start.bat           # Windows service-only start
```

---

## 📋 Changelog

### v0.952 (2026-04-23)
- 🔧 **Fixed zhconv data files missing** in PyInstaller bundles
- 📦 **EXE packaging improved** — removed tkinter, simplified to path input with pre-filled default
- 📝 **UX optimized** — ZIM input dialog enlarged from 480px to 680px, font size increased to 15px
- 🧩 **Out-of-box experience** — auto browser open, built-in default path for convenience

### v0.951 (2026-04-22)
- 🔧 **Fixed renderMath link breakage** with TOKEN placeholder system
- ⚡ **Physics engine re-architected** with spatial hash grid for O(n) collision detection
- 🧹 **Memory management improved** with stale thumbnail request detection
- 🎨 **Dynamic connections** using SVG path pool with only `d` attribute updates
- 🪟 **Responsive layout** with smooth lerp transitions on resize

### v0.95 (2026-04-22)
- 🎉 Initial release: 3D knowledge star-map + warp animations + KaTeX + multi-language + breadcrumbs + idea export

---

## 📜 License

[GNU GPL v3.0](LICENSE) · Uses [libzim](https://github.com/openzim/libzim) · Thanks to [Kiwix](https://kiwix.org/)

## 👤 Author

**Chen Chi (Xarker)** — Kaili, Guizhou, China

📧 12097652@QQ.com · [GitHub](https://github.com/556000/3d-zim-explorer) · [Gitee](https://gitee.com/xarker/3d-zim-explorer)

---

*Navigate knowledge, light the way of exploration* ✨
