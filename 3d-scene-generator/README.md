# 3D场景生成系统

AI驱动的3D场景生成和浏览平台

## 功能特性

- 🎨 输入场景描述，AI生成多视角图像
- 🌐 3D场景重建和渲染
- 🎮 自由摄像机控制（旋转、缩放、平移）
- 💾 场景保存和加载
- 📤 导出功能（图片、3D模型）

## 技术栈

- **前端**: Three.js + HTML/CSS/JavaScript
- **后端**: Python FastAPI
- **AI**: 生图API集成
- **3D**: 深度估计 + 点云重建

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 启动后端服务

```bash
python main.py
```

服务将在 http://localhost:8080 启动

### 3. 访问前端

打开浏览器访问: http://localhost:8080

## 使用说明

1. 在输入框中描述你想要的场景（例如：一个未来科技感的城市）
2. 点击生成场景按钮
3. 等待AI生成多视角图像
4. 系统自动构建3D场景
5. 使用鼠标控制摄像机浏览场景

## API文档

查看 `ARCHITECTURE_PLAN.md` 了解详细的技术架构

## 开发者

由 AutoGPT 自动生成
