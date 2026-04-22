# 3D 时空调律器 - Spatial Knowledge Navigator

## Concept & Vision

一个沉浸式的3D知识探索器，将Wikipedia的关联信息以星云般的三维形态展开。用户输入起始词后，相关概念如星辰般在空间中绽放——节点代表词条，连线代表关联，粒子流动暗示知识的流转。用鼠标自由漫步，时间轴控制穿越历史版本，让探索知识成为一种视觉与空间的双重体验。

## Design Language

### Aesthetic Direction
深空星云主题 —— 暗色背景中漂浮着发光的信息节点，像在宇宙中探索知识星系。灵感来源：星际穿越的时空展现 + Spotify Wrapped的流动美感 + 古籍星图的浪漫。

### Color Palette
- **Background**: `#050510` (深空黑)
- **Primary Node**: `#00D4FF` (量子蓝)
- **Secondary Node**: `#FF6B35` (暖星橙)
- **Timeline Past**: `#8B5CF6` (紫罗兰)
- **Timeline Future**: `#10B981` (翠翠绿)
- **Connections**: `#ffffff20` (半透明白线)
- **Text/UI**: `#E2E8F0` (月光白)
- **Accent Glow**: `#00D4FF` (节点发光)

### Typography
- **Display**: Orbitron (科技感标题)
- **Body**: Inter (清晰可读)
- **Mono**: JetBrains Mono (技术细节)

### Motion Philosophy
- 节点出现：从小点爆发式展开，带有光晕消散 (800ms ease-out)
- 节点悬停：柔和脉冲发光 + 轻微放大
- 时间切换：整体场景如万花筒般旋转重组
- 连接线：持续的粒子流动动画

## Layout & Structure

### Main View
```
┌─────────────────────────────────────────────────────────┐
│  [搜索框]  ┌──────────────────────────────────────────┐ │
│            │                                          │ │
│  ┌──────┐  │         3D CANVAS                       │ │
│  │时间线│  │      (Three.js WebGL)                   │ │
│  │控制器│  │                                          │ │
│  │      │  │                                          │ │
│  │◄ ██ ►│  │                                          │ │
│  └──────┘  │                                          │ │
│            └──────────────────────────────────────────┘ │
│  [词条信息面板]                        [控制提示]        │
└─────────────────────────────────────────────────────────┘
```

### Responsive Strategy
- Desktop: 全功能3D体验，左侧时间线面板
- Tablet: 简化控制面板，触摸友好的节点选择
- Mobile: 降级为2D关系图模式

## Features & Interactions

### Core Features

#### 1. 词条搜索与展开
- 输入框支持中英文搜索
- 实时匹配Wikipedia词条
- 回车或点击展开知识网络
- 首次加载显示3个关联节点，之后逐步展开更多

#### 2. 3D ZIM 图谱
- 每个词条显示为一个发光球体节点
- 节点大小：与关联数量成正比
- 节点颜色：主词条=蓝色，子节点=橙/紫色渐变
- 节点标签：悬浮显示词条名
- 连线：带有流动粒子的半透明线条
- 相机：OrbitControls自由旋转/缩放/平移

#### 3. 时间线导航
- 滑块范围：-10年 到 当前
- 拖动时实时更新场景
- 关键时间点标记
- 年份以柔和动画过渡

#### 4. 词条详情面板
- 点击节点打开右侧信息面板
- 显示：标题、摘要、相关图片（如有）
- 相关链接列表（可点击跳转）
- 发布时间线标记

### Interaction Details

| 操作 | 响应 |
|------|------|
| 鼠标拖拽 | 旋转视角 |
| 滚轮 | 缩放 |
| 右键拖拽 | 平移视角 |
| 单击节点 | 高亮选中，显示信息 |
| 双击节点 | 以该节点为新中心重建网络 |
| 时间滑块 | 平滑过渡到对应时间的版本 |

### Edge Cases
- 搜索无结果：显示"未找到相关词条，请尝试其他关键词"
- 加载中：节点骨架动画 + 进度指示
- 节点过多(>50)：自动聚类分组
- 无历史数据：时间滑块禁用

## Component Inventory

### SearchBox
- Default: 暗色背景，蓝色边框发光
- Focus: 边框加亮，显示下拉建议
- Loading: 边框脉冲动画
- Error: 红色边框 + 错误提示

### TimeSlider
- Track: 渐变色（紫→绿）
- Thumb: 发光圆点，带年份标签
- Marks: 关键时间节点

### Node3D
- Default: 半透明球体，微弱发光
- Hover: 放大1.2x，强发光，弹出标签
- Selected: 脉冲光环，连接线加亮
- Dimmed: 其他节点变暗

### InfoPanel
- Slide-in from right (300ms)
- 半透明毛玻璃效果
- 滚动区域显示长内容

## Technical Approach

### Architecture
```
┌─────────────────┐     HTTP/REST      ┌─────────────────┐
│   Web Browser   │ ←───────────────→ │  Python Server  │
│   (Three.js)    │                   │   (FastAPI)     │
└─────────────────┘                   └────────┬────────┘
                                               │
                                               ▼
                                        ┌─────────────────┐
                                        │   ZIM File      │
                                        │ (Wikipedia Dump)│
                                        └─────────────────┘
```

### Backend (Python + FastAPI)
- 读取ZIM文件，解析Wikipedia内容
- 构建知识图谱（词条→关联）
- 提供搜索API和时间线版本API
- 可选：预计算常用词条的关联图

### Frontend (Vanilla JS + Three.js)
- Three.js渲染3D场景
- OrbitControls相机控制
- 自定义节点shader（发光效果）
- 粒子系统实现连接线流动

### ZIM Parsing
使用 `libzim` Python绑定 或 `kiwix-serve` 作为代理

## Implementation Notes

由于ZIM文件解析的复杂性，MVP采用以下策略：
1. 使用简化的内存图结构演示核心交互
2. 词条数据来自预定义的Wikipedia子集或模拟数据
3. 完整ZIM支持作为后续迭代

3D效果核心使用Three.js实现：
- SphereGeometry + ShaderMaterial 实现发光节点
- Line + Points 实现连接线和粒子
- OrbitControls 实现自由视角控制
