# 🔗 Weaviate Memory System API 参考文档

> **完整的REST API接口文档** | 包含所有端点、参数、响应格式和使用示例

---

## 📋 概述

Weaviate Memory System 提供RESTful API接口，支持文本向量化、内存管理、缓存控制等功能。API基于FastAPI构建，自动生成OpenAPI规范和Swagger文档。

### 🌐 API基础信息

| 项目 | 值 |
|-----|---|
| **基础URL** | `http://localhost:8000` |
| **API版本** | v1.0 |
| **文档格式** | OpenAPI 3.0 |
| **认证方式** | 暂不需要（开发版本） |
| **Content-Type** | `application/json` |

### 🔗 快速链接

- 📖 **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- 📚 **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)
- 🔍 **OpenAPI JSON**: [http://localhost:8000/openapi.json](http://localhost:8000/openapi.json)
- 💚 **健康检查**: [http://localhost:8000/health](http://localhost:8000/health)

---

## 📁 API端点分组

### 1️⃣ 根目录
- `GET /` - API基本信息

### 2️⃣ 文本向量化
- `POST /embedding` - 单文本向量化
- `POST /embedding/batch` - 批量文本向量化

### 3️⃣ 内存管理
- `POST /memory` - 写入单条内存
- `POST /memory/batch` - 批量写入内存

### 4️⃣ 缓存管理
- `GET /cache/info` - 获取缓存信息
- `DELETE /cache` - 清空缓存

### 5️⃣ 系统管理
- `GET /health` - 健康检查

---

## 🔍 详细API参考

### 根目录

#### `GET /` - API基本信息

**描述**: 返回API的基本信息和入口链接

**响应示例**:
```json
{
  "name": "Weaviate Memory System API",
  "version": "1.0.0",
  "description": "高性能向量内存系统API",
  "docs": "/docs",
  "redoc": "/redoc",
  "openapi": "/openapi.json"
}
```

---

### 文本向量化

#### `POST /embedding` - 单文本向量化

**描述**: 将单个文本转换为向量表示，支持智能缓存

**请求体**:
```json
{
  "text": "要向量化的文本",
  "use_cache": true,
  "metadata": {
    "source": "user_input",
    "category": "query"
  }
}
```

**参数说明**:
| 参数 | 类型 | 必需 | 默认值 | 描述 |
|-----|------|------|-------|------|
| `text` | string | ✅ | - | 要向量化的文本内容 |
| `use_cache` | boolean | ❌ | true | 是否使用缓存 |
| `metadata` | object | ❌ | null | 可选的元数据 |

**响应示例**:
```json
{
  "vector": [0.1, -0.2, 0.3, ...],
  "cached": false,
  "processing_time": 0.856
}
```

**错误响应**:
```json
{
  "error": "数据验证错误",
  "detail": "文本不能为空",
  "timestamp": "2024-12-19T10:30:00"
}
```

**使用示例**:
```bash
curl -X POST "http://localhost:8000/embedding" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "这是一个测试文本",
    "use_cache": true
  }'
```

```python
import requests

response = requests.post("http://localhost:8000/embedding", json={
    "text": "这是一个测试文本",
    "use_cache": True
})

result = response.json()
vector = result["vector"]  # 1536维向量
```

#### `POST /embedding/batch` - 批量文本向量化

**描述**: 高效处理多个文本的向量化，通过智能缓存和API优化显著提升性能

**请求体**:
```json
{
  "texts": ["文本1", "文本2", "文本3"],
  "use_cache": true,
  "metadata": [
    {"type": "title"},
    {"type": "content"},
    {"type": "summary"}
  ]
}
```

**参数说明**:
| 参数 | 类型 | 必需 | 默认值 | 描述 |
|-----|------|------|-------|------|
| `texts` | array[string] | ✅ | - | 要向量化的文本列表（最多100个） |
| `use_cache` | boolean | ❌ | true | 是否使用缓存 |
| `metadata` | array[object] | ❌ | null | 可选的元数据列表（长度需与texts相同） |

**响应示例**:
```json
{
  "vectors": [
    [0.1, -0.2, 0.3, ...],
    [0.4, -0.5, 0.6, ...],
    [0.7, -0.8, 0.9, ...]
  ],
  "cache_hits": 1,
  "cache_misses": 2,
  "processing_time": 1.234,
  "performance_gain": 67.5
}
```

**性能指标说明**:
| 字段 | 描述 |
|-----|------|
| `cache_hits` | 缓存命中的文本数量 |
| `cache_misses` | 缓存未命中的文本数量 |
| `performance_gain` | 相比单独处理的性能提升百分比 |

**使用示例**:
```bash
curl -X POST "http://localhost:8000/embedding/batch" \
  -H "Content-Type: application/json" \
  -d '{
    "texts": ["文本1", "文本2", "文本3"],
    "use_cache": true
  }'
```

```python
import requests

texts = [
    "Python是一种高级编程语言",
    "机器学习是人工智能的一个分支",
    "向量数据库用于存储和检索高维向量"
]

response = requests.post("http://localhost:8000/embedding/batch", json={
    "texts": texts,
    "use_cache": True
})

result = response.json()
vectors = result["vectors"]
performance_gain = result["performance_gain"]
```

---

### 内存管理

#### `POST /memory` - 写入单条内存

**描述**: 将内容和元数据存储到向量数据库中，支持后续的语义搜索

**请求体**:
```json
{
  "content": "实现了用户认证功能",
  "project": "my-project",
  "repo": "backend",
  "agent": "developer-001",
  "tags": ["feature", "auth", "security"],
  "source": "development"
}
```

**参数说明**:
| 参数 | 类型 | 必需 | 默认值 | 描述 |
|-----|------|------|-------|------|
| `content` | string | ✅ | - | 内存内容 |
| `project` | string | ✅ | - | 项目标识 |
| `repo` | string | ✅ | - | 仓库名称 |
| `agent` | string | ✅ | - | 代理标识 |
| `tags` | array[string] | ✅ | - | 标签列表 |
| `source` | string | ❌ | "agent" | 来源标识 |

**响应示例**:
```json
{
  "uuid": "550e8400-e29b-41d4-a716-446655440000",
  "processing_time": 1.123
}
```

**使用示例**:
```bash
curl -X POST "http://localhost:8000/memory" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "实现了用户认证功能",
    "project": "my-project",
    "repo": "backend",
    "agent": "developer-001",
    "tags": ["feature", "auth", "security"],
    "source": "development"
  }'
```

```python
import requests

response = requests.post("http://localhost:8000/memory", json={
    "content": "实现了用户认证功能",
    "project": "my-project",
    "repo": "backend",
    "agent": "developer-001",
    "tags": ["feature", "auth", "security"],
    "source": "development"
})

result = response.json()
uuid = result["uuid"]
```

#### `POST /memory/batch` - 批量写入内存

**描述**: 高效处理大量内存记录的写入，适用于数据迁移、批量导入等场景

**请求体**:
```json
{
  "memories": [
    {
      "content": "实现了新功能",
      "project": "my-project",
      "repo": "backend",
      "agent": "developer-001",
      "tags": ["feature"],
      "source": "development"
    },
    {
      "content": "修复了bug",
      "project": "my-project",
      "repo": "backend",
      "agent": "developer-002",
      "tags": ["bugfix"],
      "source": "development"
    }
  ]
}
```

**参数说明**:
| 参数 | 类型 | 必需 | 默认值 | 描述 |
|-----|------|------|-------|------|
| `memories` | array[object] | ✅ | - | 内存记录列表（最多50条） |

**响应示例**:
```json
{
  "uuids": [
    "550e8400-e29b-41d4-a716-446655440000",
    "550e8400-e29b-41d4-a716-446655440001"
  ],
  "success_count": 2,
  "total_count": 2,
  "processing_time": 2.456
}
```

**使用示例**:
```python
import requests

memories = [
    {
        "content": "实现了新功能",
        "project": "my-project",
        "repo": "backend",
        "agent": "developer-001",
        "tags": ["feature"],
        "source": "development"
    },
    {
        "content": "修复了bug",
        "project": "my-project",
        "repo": "backend",
        "agent": "developer-002",
        "tags": ["bugfix"],
        "source": "development"
    }
]

response = requests.post("http://localhost:8000/memory/batch", json={
    "memories": memories
})

result = response.json()
uuids = result["uuids"]
success_rate = result["success_count"] / result["total_count"]
```

---

### 缓存管理

#### `GET /cache/info` - 获取缓存信息

**描述**: 返回当前缓存的统计信息，包括条目数、大小、命中率等

**响应示例**:
```json
{
  "num_entries": 1256,
  "total_size_bytes": 52428800,
  "hit_rate": 0.85
}
```

**字段说明**:
| 字段 | 类型 | 描述 |
|-----|------|------|
| `num_entries` | integer | 缓存条目总数 |
| `total_size_bytes` | integer | 缓存占用字节数 |
| `hit_rate` | float | 缓存命中率（0-1之间） |

**使用示例**:
```bash
curl -X GET "http://localhost:8000/cache/info"
```

```python
import requests

response = requests.get("http://localhost:8000/cache/info")
cache_info = response.json()

print(f"缓存条目数: {cache_info['num_entries']}")
print(f"缓存大小: {cache_info['total_size_bytes'] / 1024 / 1024:.2f} MB")
print(f"缓存命中率: {cache_info['hit_rate'] * 100:.1f}%")
```

#### `DELETE /cache` - 清空缓存

**描述**: 删除所有缓存的向量数据。⚠️ 谨慎使用，此操作不可逆

**响应示例**:
```json
{
  "message": "缓存已清空",
  "timestamp": "2024-12-19T10:30:00"
}
```

**使用示例**:
```bash
curl -X DELETE "http://localhost:8000/cache"
```

```python
import requests

response = requests.delete("http://localhost:8000/cache")
result = response.json()
print(result["message"])
```

---

### 系统管理

#### `GET /health` - 健康检查

**描述**: 检查API服务和依赖组件的状态

**响应示例**:
```json
{
  "status": "healthy",
  "timestamp": "2024-12-19T10:30:00",
  "version": "1.0.0",
  "cache_status": "healthy"
}
```

**状态说明**:
| 状态 | 描述 |
|-----|------|
| `healthy` | 服务正常运行 |
| `unhealthy` | 服务异常 |
| `degraded` | 服务降级 |

**使用示例**:
```bash
curl -X GET "http://localhost:8000/health"
```

```python
import requests

response = requests.get("http://localhost:8000/health")
health = response.json()

if health["status"] == "healthy":
    print("✅ 服务状态正常")
else:
    print("❌ 服务状态异常")
```

---

## 📊 性能基准

### 响应时间基准

| 端点 | 平均响应时间 | P95响应时间 | 说明 |
|-----|-------------|------------|------|
| `GET /health` | 10ms | 25ms | 健康检查 |
| `POST /embedding` | 800ms | 1200ms | 单文本向量化（未缓存） |
| `POST /embedding` | 50ms | 100ms | 单文本向量化（缓存命中） |
| `POST /embedding/batch` | 1500ms | 2500ms | 批量向量化（50个文本） |
| `POST /memory` | 1000ms | 1500ms | 单条内存写入 |
| `POST /memory/batch` | 3000ms | 5000ms | 批量内存写入（25条） |

### 吞吐量基准

| 操作 | 吞吐量 | 说明 |
|-----|-------|------|
| 文本向量化 | 60 texts/min | 单线程，无缓存 |
| 批量向量化 | 300 texts/min | 批量API，智能缓存 |
| 内存写入 | 50 records/min | 单线程写入 |
| 批量内存写入 | 200 records/min | 批量API |

---

## 🔧 错误处理

### HTTP状态码

| 状态码 | 含义 | 说明 |
|-------|------|------|
| 200 | OK | 请求成功 |
| 400 | Bad Request | 请求参数错误 |
| 422 | Unprocessable Entity | 数据验证失败 |
| 500 | Internal Server Error | 服务器内部错误 |
| 503 | Service Unavailable | 服务不可用 |

### 错误响应格式

```json
{
  "error": "错误类型",
  "detail": "详细错误信息",
  "timestamp": "2024-12-19T10:30:00"
}
```

### 常见错误

#### 1. 数据验证错误 (400)
```json
{
  "error": "数据验证错误",
  "detail": "文本不能为空",
  "timestamp": "2024-12-19T10:30:00"
}
```

#### 2. 批量大小超限 (422)
```json
{
  "error": "数据验证错误",
  "detail": "批量处理最多支持100个文本",
  "timestamp": "2024-12-19T10:30:00"
}
```

#### 3. 服务内部错误 (500)
```json
{
  "error": "内部服务器错误",
  "detail": "向量化处理失败: OpenAI API调用失败",
  "timestamp": "2024-12-19T10:30:00"
}
```

---

## 🚀 最佳实践

### 1. 批量处理优化

```python
# ✅ 推荐：使用批量API
texts = ["文本1", "文本2", "文本3", ...]
result = requests.post("/embedding/batch", json={"texts": texts})

# ❌ 不推荐：逐个调用
for text in texts:
    result = requests.post("/embedding", json={"text": text})
```

### 2. 缓存策略

```python
# 启用缓存以提升性能
response = requests.post("/embedding", json={
    "text": "常用文本",
    "use_cache": True  # 默认值，可省略
})

# 在需要强制刷新时禁用缓存
response = requests.post("/embedding", json={
    "text": "需要最新结果的文本",
    "use_cache": False
})
```

### 3. 错误处理

```python
import requests
from requests.exceptions import HTTPError, ConnectionError, Timeout

try:
    response = requests.post("/embedding", json={"text": "测试文本"})
    response.raise_for_status()
    result = response.json()
    
except HTTPError as e:
    if e.response.status_code == 400:
        print("请求参数错误")
    elif e.response.status_code == 500:
        print("服务器错误，请稍后重试")
        
except ConnectionError:
    print("无法连接到API服务器")
    
except Timeout:
    print("请求超时")
```

### 4. 批次大小建议

| 文本长度 | 建议批次大小 | 说明 |
|---------|-------------|------|
| < 100字符 | 50-80个 | 短文本，如标题、标签 |
| 100-500字符 | 30-50个 | 中等文本，如摘要、评论 |
| 500-2000字符 | 15-30个 | 长文本，如文章段落 |
| > 2000字符 | 5-15个 | 超长文本，如完整文档 |

---

## 🔌 客户端SDK

### Python客户端

```python
# 安装
pip install weaviate-memory-client

# 使用
from weaviate_memory_client import WeaviateMemoryAPI

api = WeaviateMemoryAPI("http://localhost:8000")

# 文本向量化
vector = api.embed_text("测试文本")

# 批量向量化
vectors = api.embed_texts_batch(["文本1", "文本2", "文本3"])

# 内存写入
uuid = api.write_memory(
    content="内容",
    project="项目",
    repo="仓库",
    agent="代理",
    tags=["标签"]
)
```

### JavaScript客户端

```javascript
// 安装
npm install weaviate-memory-client

// 使用
import WeaviateMemoryAPI from 'weaviate-memory-client';

const api = new WeaviateMemoryAPI('http://localhost:8000');

// 文本向量化
const result = await api.embedText('测试文本');

// 批量向量化
const results = await api.embedTextsBatch(['文本1', '文本2', '文本3']);

// 内存写入
const uuid = await api.writeMemory({
  content: '内容',
  project: '项目',
  repo: '仓库',
  agent: '代理',
  tags: ['标签']
});
```

---

## 🔄 版本更新

### v1.0.0 (2024-12-19)
- ✅ 初始版本发布
- ✅ 基础文本向量化API
- ✅ 批量处理优化
- ✅ 智能缓存机制
- ✅ 内存管理功能
- ✅ OpenAPI文档生成

### 即将发布
- 🔄 异步处理支持
- 🔄 内存搜索API
- 🔄 用户认证机制
- 🔄 更多语言SDK

---

## 📞 支持与反馈

### 获取帮助
- 📧 **API支持**: api-support@company.com
- 💬 **技术讨论**: [GitHub Discussions](https://github.com/your-repo/discussions)
- 🐛 **问题报告**: [GitHub Issues](https://github.com/your-repo/issues)

### 社区资源
- 📖 **完整文档**: [docs.company.com](https://docs.company.com)
- 🎓 **教程系列**: [tutorials.company.com](https://tutorials.company.com)
- 💡 **最佳实践**: [best-practices.company.com](https://best-practices.company.com)

---

*API参考文档 | 版本 1.0 | 维护团队: API Development Team | 最后更新: 2024-12-19* 