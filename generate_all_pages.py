#!/usr/bin/env python3
"""
完整的技术文档站点生成器
包含所有页面：首页、博客、功能、文档、关于
"""
import os
from pathlib import Path
from datetime import datetime

WORKSPACE = '/root/autogpt-data/workspace'

def generate_navbar(active='home'):
    """生成导航栏"""
    links = {
        'home': ('/', '首页'),
        'docs': ('/docs.html', '文档'),
        'blogs': ('/blogs.html', '博客'),
        'features': ('/features.html', '功能'),
        'about': ('/about.html', '关于')
    }

    nav = '<nav class="navbar">'
    nav += '<a href="/" class="navbar-logo">🤖 AutoGPT</a>'
    nav += '<div class="navbar-links">'

    for key, (url, label) in links.items():
        active_class = ' active' if key == active else ''
        nav += f'<a href="{url}" class="navbar-link{active_class}">{label}</a>'

    nav += '</div>'
    nav += '<a href="https://github.com/Significant-Gravitas/AutoGPT" class="btn btn-secondary" target="_blank">GitHub</a>'
    nav += '</nav>'

    return nav

def generate_blogs_page():
    """生成博客列表页"""
    blogs = list(Path(f'{WORKSPACE}/blogs').glob('*.html')) if os.path.exists(f'{WORKSPACE}/blogs') else []

    blog_cards = ''
    for blog in sorted(blogs, reverse=True):
        name = blog.name
        mtime = datetime.fromtimestamp(blog.stat().st_mtime).strftime('%Y-%m-%d %H:%M')
        blog_cards += f'''
        <div class="card">
            <h3 style="color: #7c8cff; margin-bottom: 15px;">{name}</h3>
            <p style="color: #94a3b8; margin-bottom: 20px;">生成时间: {mtime}</p>
            <a href="blogs/{name}" class="btn" target="_blank">阅读博客</a>
        </div>
        '''

    if not blog_cards:
        blog_cards = '<p style="text-align: center; color: #94a3b8; padding: 60px;">暂无博客，系统会每 30 分钟自动生成</p>'

    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>技术博客 - AutoGPT</title>
    <link rel="stylesheet" href="/styles.css">
</head>
<body>
    <canvas id="bg-canvas"></canvas>
    <div class="content-wrapper">
        {generate_navbar('blogs')}
        <div class="breadcrumb">
            <a href="/">首页</a> <span>/</span> <span style="color: #e5eefb;">博客</span>
        </div>
        <div class="container">
            <h1 class="page-title">技术博客</h1>
            <p class="page-subtitle">自动生成的深度技术文章，每 30 分钟更新</p>
            <div class="grid">
                {blog_cards}
            </div>
        </div>
    </div>
    <script src="/bg.js"></script>
</body>
</html>'''

    return html

def generate_features_page():
    """生成功能展示页"""
    features = list(Path(f'{WORKSPACE}/features').glob('**/*.html')) if os.path.exists(f'{WORKSPACE}/features') else []

    feature_cards = ''
    for feature in sorted(features, reverse=True):
        rel_path = feature.relative_to(f'{WORKSPACE}/features')
        mtime = datetime.fromtimestamp(feature.stat().st_mtime).strftime('%Y-%m-%d %H:%M')
        feature_cards += f'''
        <div class="card">
            <h3 style="color: #7c8cff; margin-bottom: 15px;">{rel_path}</h3>
            <p style="color: #94a3b8; margin-bottom: 20px;">开发时间: {mtime}</p>
            <a href="features/{rel_path}" class="btn" target="_blank">查看详情</a>
        </div>
        '''

    if not feature_cards:
        feature_cards = '<p style="text-align: center; color: #94a3b8; padding: 60px;">暂无功能，系统会每小时自动开发</p>'

    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>功能展示 - AutoGPT</title>
    <link rel="stylesheet" href="/styles.css">
</head>
<body>
    <canvas id="bg-canvas"></canvas>
    <div class="content-wrapper">
        {generate_navbar('features')}
        <div class="breadcrumb">
            <a href="/">首页</a> <span>/</span> <span style="color: #e5eefb;">功能</span>
        </div>
        <div class="container">
            <h1 class="page-title">功能展示</h1>
            <p class="page-subtitle">自动开发的实用功能，包含完整代码和演示</p>
            <div class="grid">
                {feature_cards}
            </div>
        </div>
    </div>
    <script src="/bg.js"></script>
</body>
</html>'''

    return html

def generate_docs_page():
    """生成文档中心页"""
    reports = list(Path(f'{WORKSPACE}/reports').glob('*.md')) if os.path.exists(f'{WORKSPACE}/reports') else []

    report_cards = ''
    for report in sorted(reports, reverse=True):
        name = report.name
        mtime = datetime.fromtimestamp(report.stat().st_mtime).strftime('%Y-%m-%d %H:%M')
        report_cards += f'''
        <div class="card">
            <h3 style="color: #7c8cff; margin-bottom: 15px;">{name}</h3>
            <p style="color: #94a3b8; margin-bottom: 20px;">生成时间: {mtime}</p>
            <a href="reports/{name}" class="btn" target="_blank">查看报告</a>
        </div>
        '''

    if not report_cards:
        report_cards = '<p style="text-align: center; color: #94a3b8; padding: 60px;">暂无报告</p>'

    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>文档中心 - AutoGPT</title>
    <link rel="stylesheet" href="/styles.css">
</head>
<body>
    <canvas id="bg-canvas"></canvas>
    <div class="content-wrapper">
        {generate_navbar('docs')}
        <div class="breadcrumb">
            <a href="/">首页</a> <span>/</span> <span style="color: #e5eefb;">文档</span>
        </div>
        <div class="container">
            <h1 class="page-title">文档中心</h1>
            <p class="page-subtitle">执行报告、系统状态、配置说明</p>

            <h2 style="color: #7c8cff; font-size: 2em; margin: 60px 0 30px;">📊 执行报告</h2>
            <div class="grid">
                {report_cards}
            </div>

            <h2 style="color: #7c8cff; font-size: 2em; margin: 60px 0 30px;">📚 系统文档</h2>
            <div class="grid">
                <div class="card">
                    <h3 style="color: #7c8cff; margin-bottom: 15px;">快速开始</h3>
                    <p style="color: #94a3b8; margin-bottom: 20px;">了解如何使用 AutoGPT 系统</p>
                </div>
                <div class="card">
                    <h3 style="color: #7c8cff; margin-bottom: 15px;">系统架构</h3>
                    <p style="color: #94a3b8; margin-bottom: 20px;">了解系统的技术架构和设计</p>
                </div>
                <div class="card">
                    <h3 style="color: #7c8cff; margin-bottom: 15px;">API 文档</h3>
                    <p style="color: #94a3b8; margin-bottom: 20px;">Agent Protocol API 使用说明</p>
                </div>
            </div>
        </div>
    </div>
    <script src="/bg.js"></script>
</body>
</html>'''

    return html

def generate_stats_json():
    """生成统计数据JSON"""
    import json
    from datetime import datetime

    # 统计各类文件数量
    blogs_count = len(list(Path(f'{WORKSPACE}/blogs').glob('*.html'))) if os.path.exists(f'{WORKSPACE}/blogs') else 0
    features_count = len([d for d in Path(f'{WORKSPACE}/features').iterdir() if d.is_dir()]) if os.path.exists(f'{WORKSPACE}/features') else 0
    reports_count = len(list(Path(f'{WORKSPACE}/reports').glob('*.md'))) if os.path.exists(f'{WORKSPACE}/reports') else 0

    # 构建数据
    stats = {
        'blogs': blogs_count,
        'features': features_count,
        'reports': reports_count,
        'last_updated': datetime.now().isoformat()
    }

    # 确保api目录存在
    api_dir = f'{WORKSPACE}/api'
    os.makedirs(api_dir, exist_ok=True)

    # 写入JSON文件
    try:
        with open(f'{api_dir}/stats.json', 'w', encoding='utf-8') as f:
            json.dump(stats, f, indent=2, ensure_ascii=False)
        print(f'✓ 统计数据已更新: 博客 {blogs_count}, 功能 {features_count}, 报告 {reports_count}')
    except Exception as e:
        print(f'✗ 统计数据生成失败: {e}')

def main():
    print("生成站点页面...")

    # 生成博客列表页
    with open(f'{WORKSPACE}/blogs.html', 'w', encoding='utf-8') as f:
        f.write(generate_blogs_page())
    print("✓ 博客列表页")

    # 生成功能展示页
    with open(f'{WORKSPACE}/features.html', 'w', encoding='utf-8') as f:
        f.write(generate_features_page())
    print("✓ 功能展示页")

    # 生成文档中心页
    with open(f'{WORKSPACE}/docs.html', 'w', encoding='utf-8') as f:
        f.write(generate_docs_page())
    print("✓ 文档中心页")
    
    # 生成统计数据JSON
    generate_stats_json()
    print("✓ 统计数据API")

    print(f"\n所有页面已生成到: {WORKSPACE}/")
    print("\n访问地址:")
    print("  博客列表: http://38.47.221.152:8001/blogs.html")
    print("  功能展示: http://38.47.221.152:8001/features.html")
    print("  文档中心: http://38.47.221.152:8001/docs.html")

if __name__ == '__main__':
    main()
