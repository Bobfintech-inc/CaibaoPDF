# CaibaoPDF 财务报告处理系统

基于Django的智能化PDF处理解决方案，提供财务报表OCR解析、异步任务管理和RESTful API服务。

## 功能特性

- 多线程PDF文件扫描与处理
- Celery异步任务队列管理
- REST API状态回调通知
- 分布式OCR处理节点管理
- 文件哈希校验与版本控制

## 技术栈

- Web框架: Django 4.2
- API构建: Django REST Framework
- 任务队列: Celery
- 数据库: SQLite3/SQLAlchemy
- 文件处理: python-filehash
- 进度显示: tqdm

## 开发环境搭建

### 前置要求
- Python 3.9+
- Redis 6.2+ (Celery Broker)
- SQLite 3

### 安装步骤
```bash
# 创建虚拟环境
python -m venv .venv

# 激活环境
source .venv/bin/activate  # Linux/macOS
# 或
.\.venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt

# 数据库配置
createdb caibao_pdf
python manage.py migrate

# 启动服务
python manage.py runserver  # 开发服务器
celery -A project worker -l info  # Celery worker
```

## 关键配置
```python
# .env
SITE_DOMAIN=http://<ip>:8000
OCR_OUTPUT_FORMAT=md
```

## 使用说明
```bash
# 初始化数据库，扫描所有文件
python manage.py scan_caibao

# 启动OCR处理守护进程
python manage.py ocr_deamon

# 启动回调服务
python manage.py runserver 0.0.0.0:8000
```

## 贡献指南
欢迎提交Pull Request，请确保：
1. 代码符合PEP8规范
2. 包含必要的单元测试
3. 更新相关文档


