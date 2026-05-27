# AutoGPT 自动化系统总结

## 系统概览

JTTI服务器上运行着完整的AutoGPT自动化系统，包含5个定时任务，自动生成内容、优化UI和开发功能。

## 服务信息

- **服务器**: 38.47.221.152 (JTTI - 美国)
- **AutoGPT API**: http://38.47.221.152:8003
- **监控页面**: http://38.47.221.152:8001
- **3D场景生成**: http://38.47.221.152:8001/3d-scene-generator/

## 定时任务

### 1. UI优化器 (autogpt-ui-optimizer.timer)
- **间隔**: 每10分钟
- **功能**: 访问优秀网站学习设计，优化workspace中的HTML文件
- **日志**: /root/autogpt-data/logs/ui_optimizer.log
- **脚本**: /root/ui_optimizer_v3.py

### 2. 技术博客生成 (autogpt-periodic.timer)
- **间隔**: 每30分钟
- **功能**: 收集技术新闻，生成1500-2000字深度技术博客
- **日志**: /root/autogpt-data/logs/periodic_task.log
- **脚本**: /root/autogpt_periodic_task_fixed.py

### 3. 功能开发 (autogpt-weekly.timer)
- **间隔**: 每1小时
- **功能**: 开发实用功能（Web工具、算法、API服务）
- **日志**: /root/autogpt-data/logs/weekly_feature.log
- **脚本**: /root/weekly_feature_dev_fixed.py

### 4. 索引更新 (autogpt-index-update.timer)
- **间隔**: 每5分钟
- **功能**: 更新内容索引页面
- **日志**: /root/autogpt-data/logs/index_update.log

### 5. 工具开发 (autogpt-optimizer.timer)
- **间隔**: 每30分钟
- **功能**: 创建实用的Web工具和应用
- **日志**: /root/autogpt-data/logs/autogpt_optimizer.log
- **脚本**: /root/autogpt_optimizer.py

## 管理命令

### 查看状态
```bash
# 查看所有定时器
systemctl list-timers | grep autogpt

# 查看特定定时器状态
systemctl status autogpt-optimizer.timer
```

### 启动/停止
```bash
# 启动所有
systemctl start autogpt-*.timer

# 停止所有
systemctl stop autogpt-*.timer

# 重启特定任务
systemctl restart autogpt-periodic.timer
```

### 查看日志
```bash
# 实时查看所有日志
tail -f /root/autogpt-data/logs/*.log

# 查看特定日志
tail -f /root/autogpt-data/logs/autogpt_optimizer.log
```

### 手动执行
```bash
# 手动运行优化器
python3 /root/autogpt_optimizer.py

# 手动运行UI优化
python3 /root/ui_optimizer_v3.py
```

## 输出目录

- **Workspace**: /root/autogpt-data/workspace/
- **博客**: /root/autogpt-data/workspace/blogs/
- **功能**: /root/autogpt-data/workspace/features/
- **报告**: /root/autogpt-data/workspace/reports/
- **日志**: /root/autogpt-data/logs/

## AutoGPT配置

- **API密钥**: sk-56c44cf45114b19d17c2660cae94779fbc181518efd4afb1edc815c12290872e
- **API地址**: https://api.psydo.top/v1
- **模型**: gpt-5.4
- **配置文件**: /app/original_autogpt/.env (容器内)

## 3D场景生成系统

- **路径**: /root/autogpt-data/workspace/3d-scene-generator/
- **后端**: FastAPI (端口8080)
- **前端**: Three.js
- **启动脚本**: /root/start_3d_scene_generator.sh
- **访问**: http://38.47.221.152:8001/3d-scene-generator/

## 监控

所有生成的内容都会自动显示在监控页面：
http://38.47.221.152:8001/

## 最后更新

2026-05-27 15:25
