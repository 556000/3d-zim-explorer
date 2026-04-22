# 🌌 3D ZIM Explorer — 时空导航

A 3D interactive Wikipedia knowledge graph explorer. Navigate the universe of knowledge with an immersive star-map visualization.

一个基于 3D 星图可视化的维基百科知识探索器，将词条之间的关系以星空连线的方式呈现，支持时空穿梭动画、数学公式渲染和多语言界面。

![Version](https://img.shields.io/badge/version-0.95-blue)
![License](https://img.shields.io/badge/license-GPL%20v3-green)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)

## ✨ Features

- 🌠 **3D Knowledge Graph** — Central article card with orbiting related-topic nodes and arc connections
- 🚀 **Warp Animation** — Starfield acceleration streaks when navigating between articles
- 🧭 **Breadcrumb Navigation** — Trace your exploration path and jump back
- 🔢 **Math Rendering** — KaTeX-powered formula rendering (displaystyle, textstyle, $$, \[\], \(\))
- 🔗 **Wiki Links** — Clickable in-article links that navigate to other entries
- 🌐 **Multi-language UI** — Simplified Chinese / Traditional Chinese / English
- 📷 **Thumbnails** — Article images displayed in related-node cards
- 💡 **Idea Export** — Export your exploration trail as structured notes

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- A Wikipedia ZIM file (download from [Kiwix](https://wiki.kiwix.org/wiki/Content))

### 1. Install Dependencies

```bash
pip install fastapi uvicorn libzim beautifulsoup4
```

### 2. Configure ZIM Path

Edit `zim-config.json` to point to your ZIM file:

```json
{"zim_path": "C:/path/to/wikipedia_zh_all_maxi_2025-04.zim"}
```

### 3. Start the Server

```bash
python server.py
```

Then open **http://localhost:8765** in your browser.

Or use the included batch files:
- `启动.bat` — Auto-start server + open browser
- `start.bat` — Start server only

## 🎮 Controls

| Action | Effect |
|--------|--------|
| Search + Enter | Search and expand knowledge graph |
| Click node | View article summary |
| Double-click node | Re-center on that article |
| Drag | Rotate view |
| Scroll | Zoom in/out |
| Right-drag | Pan |

## 🛠️ Tech Stack

- **Backend**: FastAPI + libzim + BeautifulSoup4
- **Frontend**: Three.js + OrbitControls + KaTeX
- **Rendering**: Pure HTML/CSS/Canvas (no framework)
- **Data Source**: ZIM offline Wikipedia archives (via Kiwix)

## 📁 Project Structure

```
3d-zim-explorer/
├── server.py          # FastAPI backend (ZIM parsing + API)
├── index.html         # Single-file frontend (HTML/CSS/JS)
├── three.min.js       # Three.js 3D engine
├── OrbitControls.js   # Camera controls
├── zim-config.json    # ZIM file path config
├── 启动.bat            # One-click launcher
├── start.bat          # Server starter
└── SPEC.md            # Design specification
```

## 📜 License

This project is licensed under **GNU General Public License v3.0** — see the [LICENSE](LICENSE) file for details.

This project uses [libzim](https://github.com/openzim/libzim) by [Kiwix](https://kiwix.org/) for ZIM file access. Special thanks to the Kiwix team.

## 👤 Author

**陈驰 (Chen Chi)** — 来自 中国·贵州·凯里

Contact: 12097652@QQ.com

---

*时空导航，点亮探索之路* ✨
