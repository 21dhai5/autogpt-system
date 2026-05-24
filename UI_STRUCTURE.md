# AutoGPT 技术文档站点 - UI 结构说明

## 页面架构总结

### 新版站点（技术文档风格 + 动态背景）

**首页** (index_new.html)
- 导航栏: 首页 | 文档 | 博客 | 功能 | 关于
- Hero 区域 + 统计数据 + 核心功能展示
- 动态粒子背景

**博客列表** (blogs.html)
- 展示所有自动生成的技术博客
- 卡片网格布局
- 链接到 blogs/*.html

**功能展示** (features.html)
- 展示所有自动开发的功能
- 卡片网格布局
- 链接到 features/**/*.html

**文档中心** (docs.html)
- 执行报告列表
- 系统文档卡片
- 链接到 reports/*.md

### 旧版页面（保留）

- index.html - 原始首页（已优化）
- content_index.html - 内容索引页

## 动态背景系统

### 技术实现
- Canvas 粒子系统（100个浮动粒子）
- 粒子间自动连线
- 鼠标交互效果（粒子躲避鼠标）
- 鼠标位置渐变光晕
- requestAnimationFrame 动画循环
- 性能优化：粒子数量自适应屏幕宽度

### 视觉效果
- 深色背景 #0a0e1a
- 紫蓝渐变色 #7c8cff → #22d3ee
- 半透明粒子 opacity: 0.6
- 动态连线 opacity: 0-0.2

## 导航系统

### 全局导航栏
- 固定在顶部
- 毛玻璃效果 backdrop-filter: blur
- 当前页面高亮显示
- 渐变下划线指示器

### 面包屑导航
- 显示当前位置
- 可点击返回上级

## 文件结构

```
/root/autogpt-data/workspace/
├── index_new.html          # 新首页（动态背景）
├── blogs.html              # 博客列表页
├── features.html           # 功能展示页
├── docs.html               # 文档中心页
├── styles.css              # 公共样式
├── bg.js                   # 动态背景脚本
├── index.html              # 旧首页（保留）
├── content_index.html      # 内容索引（保留）
├── blogs/                  # 博客文件
├── features/               # 功能文件
└── reports/                # 执行报告
```

## 访问地址

### 新版站点
- 首页: http://38.47.221.152:8001/index_new.html
- 博客: http://38.47.221.152:8001/blogs.html
- 功能: http://38.47.221.152:8001/features.html
- 文档: http://38.47.221.152:8001/docs.html

### 旧版页面（保留）
- 旧首页: http://38.47.221.152:8001/index.html
- 内容索引: http://38.47.221.152:8001/content_index.html

## 设计规范

### 颜色系统
- 主背景: #0a0e1a
- 卡片背景: rgba(15, 23, 42, 0.6)
- 主文本: #e5eefb
- 次要文本: #94a3b8
- 主色调: #7c8cff
- 强调色: #22d3ee

### 字体系统
- 主字体: Inter, Segoe UI, system-ui
- 标题: 800 weight
- 正文: 400-500 weight

### 间距系统
- 容器最大宽度: 1400px
- 卡片间距: 30px
- 内边距: 30-40px
- 圆角: 12-20px

## 维护命令

### 重新生成所有页面
```bash
python3 /root/generate_site.py
python3 /root/generate_all_pages.py
```

### 更新公共资源
```bash
vim /root/autogpt-data/workspace/styles.css
vim /root/autogpt-data/workspace/bg.js
```

## 注意事项

1. 新旧页面共存，不影响现有功能
2. 可以逐步将流量切换到新页面
3. 动态背景在低端设备上可能影响性能
4. 需要现代浏览器支持 Canvas 和 CSS backdrop-filter
5. 移动端优化：粒子数量会自动减少

---

更新时间: 2026-05-24
版本: 1.0.0
