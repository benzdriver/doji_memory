# 🚀 Weaviate Memory System API 服务

> **统一的REST API接口** | 基于FastAPI构建，提供完整的OpenAPI/Swagger文档

---

## 📋 概述

Weaviate Memory System API 是一个高性能的RESTful服务，提供文本向量化、内存管理、缓存控制等功能。基于FastAPI构建，具有自动文档生成、数据验证、异步支持等现代Web API特性。

### ✨ 核心特性

- 🚀 **高性能**: 基于FastAPI和uvicorn，支持异步处理
- 📖 **自动文档**: 自动生成OpenAPI规范和Swagger UI
- 🔧 **数据验证**: 基于Pydantic的请求/响应验证
- 💾 **智能缓存**: 内置缓存机制，显著提升性能
- ⚡ **批量优化**: 支持批量处理，性能提升60-80%
- 🐳 **容器化**: 完整的Docker支持
- 📊 **监控**: 内置健康检查和性能监控

---

## 🛠️ 快速开始

### 方式1: 本地开发模式

```bash
# 1. 安装依赖
pip install -r requirements.txt
pip install -r api/requirements-api.txt

# 2. 设置环境变量
export OPENAI_API_KEY=your_openai_api_key

# 3. 启动开发服务器
python api/start_api.py --mode dev

# 4. 访问API文档
open http://localhost:8000/docs
```

### 方式2: Docker容器模式

```bash
# 1. 创建环境变量文件
echo "OPENAI_API_KEY=your_openai_api_key" > .env

# 2. 使用Docker Compose启动
cd api
docker-compose up -d

# 3. 查看服务状态
docker-compose ps

# 4. 访问API文档
open http://localhost:8000/docs
```

### 方式3: 生产部署模式

```bash
# 1. 启动生产服务器
python api/start_api.py --mode prod

# 2. 或使用自定义配置
python api/start_api.py --mode custom \
  --host 0.0.0.0 \
  --port 8080 \
  --workers 4
```

---

## 📖 API文档

### 🌐 在线文档

| 文档类型 | URL | 描述 |
|---------|-----|------|
| **Swagger UI** | http://localhost:8000/docs | 交互式API文档 |
| **ReDoc** | http://localhost:8000/redoc | 美观的API文档 |
| **OpenAPI JSON** | http://localhost:8000/openapi.json | 机器可读规范 |

### 📁 主要端点

| 端点 | 方法 | 描述 |
|-----|------|------|
| `/health` | GET | 健康检查 |
| `/embedding` | POST | 单文本向量化 |
| `/embedding/batch` | POST | 批量文本向量化 |
| `/memory` | POST | 写入单条内存 |
| `/memory/batch` | POST | 批量写入内存 |
| `/cache/info` | GET | 获取缓存信息 |
| `/cache` | DELETE | 清空缓存 |

---

## 🔧 配置选项

### 环境变量

| 变量名 | 必需 | 默认值 | 描述 |
|-------|------|-------|------|
| `OPENAI_API_KEY` | ✅ | - | OpenAI API密钥 |
| `OPENAI_PROJECT_ID` | ❌ | - | OpenAI项目ID |
| `OPENAI_ORGANIZATION_ID` | ❌ | - | OpenAI组织ID |
| `WEAVIATE_URL` | ❌ | http://localhost:8080 | Weaviate数据库URL |
| `CACHE_DIR` | ❌ | .cache | 缓存目录路径 |
| `LOG_LEVEL` | ❌ | info | 日志级别 |

### 启动参数

```bash
python api/start_api.py --help
```

```
optional arguments:
  --mode {dev,prod,custom}  启动模式 (默认: dev)
  --host HOST              绑定主机 (默认: 127.0.0.1)
  --port PORT              绑定端口 (默认: 8000)
  --workers WORKERS        工作进程数 (默认: 1)
  --reload                 启用热重载
  --check-deps            检查依赖
  --check-env             检查环境变量
  --generate-spec         生成OpenAPI规范文件
```

---

## 💻 使用示例

### Python客户端

```python
import requests

# API基础URL
API_BASE = "http://localhost:8000"

# 1. 健康检查
response = requests.get(f"{API_BASE}/health")
print(response.json())

# 2. 单文本向量化
response = requests.post(f"{API_BASE}/embedding", json={
    "text": "这是一个测试文本",
    "use_cache": True
})
result = response.json()
vector = result["vector"]

# 3. 批量文本向量化
texts = ["文本1", "文本2", "文本3"]
response = requests.post(f"{API_BASE}/embedding/batch", json={
    "texts": texts,
    "use_cache": True
})
result = response.json()
vectors = result["vectors"]

# 4. 写入内存
response = requests.post(f"{API_BASE}/memory", json={
    "content": "实现了新功能",
    "project": "my-project",
    "repo": "backend",
    "agent": "developer",
    "tags": ["feature", "implementation"]
})
result = response.json()
uuid = result["uuid"]
```

### JavaScript客户端

```javascript
// 使用fetch API
const API_BASE = 'http://localhost:8000';

// 1. 健康检查
const health = await fetch(`${API_BASE}/health`).then(r => r.json());

// 2. 文本向量化
const embedding = await fetch(`${API_BASE}/embedding`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        text: '这是一个测试文本',
        use_cache: true
    })
}).then(r => r.json());

// 3. 批量向量化
const batch = await fetch(`${API_BASE}/embedding/batch`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        texts: ['文本1', '文本2', '文本3'],
        use_cache: true
    })
}).then(r => r.json());
```

### cURL示例

```bash
# 健康检查
curl -X GET "http://localhost:8000/health"

# 文本向量化
curl -X POST "http://localhost:8000/embedding" \
  -H "Content-Type: application/json" \
  -d '{"text": "测试文本", "use_cache": true}'

# 批量向量化
curl -X POST "http://localhost:8000/embedding/batch" \
  -H "Content-Type: application/json" \
  -d '{"texts": ["文本1", "文本2"], "use_cache": true}'

# 写入内存
curl -X POST "http://localhost:8000/memory" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "实现了新功能",
    "project": "my-project",
    "repo": "backend",
    "agent": "developer",
    "tags": ["feature"],
    "source": "development"
  }'
```

---

## 🐳 Docker部署

### 基础部署

```bash
# 构建镜像
docker build -f api/Dockerfile -t weaviate-memory-api .

# 运行容器
docker run -d \
  --name memory-api \
  -p 8000:8000 \
  -e OPENAI_API_KEY=your_key \
  weaviate-memory-api
```

### Docker Compose部署

```yaml
# docker-compose.yml
version: '3.8'

services:
  memory-api:
    build:
      context: .
      dockerfile: api/Dockerfile
    ports:
      - "8000:8000"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
    depends_on:
      - weaviate
    restart: unless-stopped

  weaviate:
    image: semitechnologies/weaviate:1.22.4
    ports:
      - "8080:8080"
    environment:
      AUTHENTICATION_ANONYMOUS_ACCESS_ENABLED: 'true'
      PERSISTENCE_DATA_PATH: '/var/lib/weaviate'
    volumes:
      - weaviate_data:/var/lib/weaviate

volumes:
  weaviate_data:
```

```bash
# 启动服务
docker-compose up -d

# 查看日志
docker-compose logs -f memory-api

# 停止服务
docker-compose down
```

### 生产环境配置

```yaml
# docker-compose.prod.yml
version: '3.8'

services:
  memory-api:
    image: weaviate-memory-api:latest
    deploy:
      replicas: 3
      resources:
        limits:
          cpus: '1.0'
          memory: 1G
        reservations:
          cpus: '0.5'
          memory: 512M
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - LOG_LEVEL=warning
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
    depends_on:
      - memory-api
```

---

## 📊 性能监控

### 内置监控

API服务内置了多种监控功能：

```python
# 健康检查端点
GET /health

# 缓存状态监控
GET /cache/info

# 性能指标包含在响应中
{
  "processing_time": 1.234,
  "cache_hits": 10,
  "performance_gain": 67.5
}
```

### Prometheus集成

```yaml
# prometheus.yml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'weaviate-memory-api'
    static_configs:
      - targets: ['memory-api:8000']
    metrics_path: '/metrics'
```

### Grafana仪表板

```bash
# 启动监控栈
docker-compose --profile monitoring up -d

# 访问Grafana
open http://localhost:3000
# 用户名: admin, 密码: admin
```

---

## 🔒 安全配置

### 生产环境安全

```bash
# 1. 设置强密码和密钥
export OPENAI_API_KEY=your_secure_key

# 2. 配置防火墙
sudo ufw allow 8000/tcp

# 3. 使用HTTPS
# 配置nginx反向代理和SSL证书

# 4. 限制访问
# 在nginx中配置IP白名单
```

### API认证（计划中）

```python
# 未来版本将支持
headers = {
    "Authorization": "Bearer your_api_token",
    "X-API-Key": "your_api_key"
}
```

---

## 🐛 故障排除

### 常见问题

#### 1. 服务启动失败

```bash
# 检查依赖
python api/start_api.py --check-deps

# 检查环境变量
python api/start_api.py --check-env

# 查看详细错误日志
python api/start_api.py --mode dev
```

#### 2. OpenAI API错误

```bash
# 检查API密钥
curl -H "Authorization: Bearer $OPENAI_API_KEY" \
  https://api.openai.com/v1/models

# 检查配额和余额
# 访问 https://platform.openai.com/account/usage
```

#### 3. 缓存问题

```bash
# 清空缓存
curl -X DELETE "http://localhost:8000/cache"

# 检查缓存目录权限
ls -la .cache/
chmod 755 .cache/
```

#### 4. 性能问题

```bash
# 查看系统资源
htop
df -h

# 调整工作进程数
python api/start_api.py --mode custom --workers 4

# 监控API性能
curl -X GET "http://localhost:8000/cache/info"
```

### 日志分析

```bash
# 查看API日志
tail -f logs/api.log

# Docker环境查看日志
docker-compose logs -f memory-api

# 日志级别设置
export LOG_LEVEL=debug
```

---

## 🔄 版本升级

### 升级步骤

```bash
# 1. 停止服务
docker-compose down

# 2. 备份数据
docker run --rm -v weaviate_data:/data -v $(pwd):/backup \
  busybox tar czf /backup/weaviate_backup.tar.gz /data

# 3. 拉取新版本
git pull origin main

# 4. 重新构建
docker-compose build

# 5. 启动新版本
docker-compose up -d

# 6. 验证服务
curl -X GET "http://localhost:8000/health"
```

### 兼容性说明

| 版本 | 兼容性 | 说明 |
|-----|-------|------|
| v1.0.x | ✅ 完全兼容 | 补丁版本，向后兼容 |
| v1.x.0 | ⚠️ 部分兼容 | 次版本，可能有新增功能 |
| v2.0.0 | ❌ 不兼容 | 主版本，可能有破坏性变更 |

---

## 📚 相关文档

- 📖 [API参考文档](../docs/api-reference.md)
- 🎯 [用例目录](../docs/use-cases-catalog.md)
- ⚡ [批量处理指南](../docs/batch-processing-guide.md)
- 🏆 [行业最佳实践](../docs/industry-best-practices.md)
- 🔧 [开发指南](../docs/development-guide.md)

---

## 🤝 贡献指南

### 开发环境搭建

```bash
# 1. 克隆仓库
git clone https://github.com/your-repo/doji-memory.git
cd doji-memory

# 2. 安装开发依赖
pip install -r requirements-dev.txt
pip install -r api/requirements-api.txt

# 3. 启动开发服务器
python api/start_api.py --mode dev

# 4. 运行测试
pytest tests/
```

### 代码规范

```bash
# 代码格式化
black api/
isort api/

# 代码检查
flake8 api/
mypy api/

# 安全检查
bandit -r api/
```

### 提交流程

1. Fork仓库并创建功能分支
2. 编写代码和测试
3. 确保所有测试通过
4. 提交Pull Request
5. 代码审查和合并

---

## 📞 支持与联系

### 技术支持

- 📧 **API支持**: api-support@company.com
- 💬 **即时沟通**: [Slack #api-support](https://company.slack.com/channels/api-support)
- 🐛 **问题报告**: [GitHub Issues](https://github.com/your-repo/issues)

### 社区资源

- 📖 **文档中心**: [docs.company.com](https://docs.company.com)
- 💡 **讨论社区**: [GitHub Discussions](https://github.com/your-repo/discussions)
- 🎓 **教程视频**: [YouTube频道](https://youtube.com/@company)

---

*API服务文档 | 版本 1.0 | 维护团队: API Development Team | 最后更新: 2024-12-19* 