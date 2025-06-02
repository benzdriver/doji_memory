# 🚀 Doji Memory System

> **企业级向量内存系统** | 智能缓存 · 批量处理 · REST API · 一键部署

一个基于 Weaviate 的高性能向量存储和检索系统，提供完整的 REST API 接口，支持语义搜索、智能缓存和批量处理优化。

## ✨ 核心特性

- 🧠 **智能向量化**: 基于 OpenAI text-embedding-ada-002 模型
- ⚡ **批量优化**: 批量处理性能提升 60-80%
- 💾 **智能缓存**: 文件缓存系统，减少 API 调用成本
- 🔗 **REST API**: 完整的 FastAPI 服务，自动生成文档
- 🐳 **一键部署**: Docker Compose 一键启动完整服务栈
- 📊 **生产就绪**: 健康检查、监控、日志记录

## 🚀 快速开始

### 一键启动完整服务

```bash
# 1. 克隆项目
git clone https://github.com/benzdriver/doji_memory.git
cd doji_memory

# 2. 配置环境变量
echo "OPENAI_API_KEY=your_openai_api_key" > .env

# 3. 一键启动服务栈
cd api
docker-compose up -d

# 4. 访问 API 文档
open http://localhost:8000/docs
```

就是这么简单！🎉

### 服务地址

| 服务 | 地址 | 说明 |
|-----|------|------|
| **API 服务** | http://localhost:8000 | 主要 REST API |
| **Swagger UI** | http://localhost:8000/docs | 交互式 API 文档 |
| **ReDoc** | http://localhost:8000/redoc | 美观的 API 文档 |
| **Weaviate** | http://localhost:8080 | 向量数据库 |

## 📖 API 示例

### Python 客户端

```python
import requests

# 文本向量化
response = requests.post("http://localhost:8000/embedding", json={
    "text": "这是一个测试文本",
    "use_cache": True
})
vector = response.json()["vector"]

# 批量向量化
response = requests.post("http://localhost:8000/embedding/batch", json={
    "texts": ["文本1", "文本2", "文本3"],
    "use_cache": True
})
vectors = response.json()["vectors"]

# 写入内存
response = requests.post("http://localhost:8000/memory", json={
    "content": "实现了新功能",
    "project": "my-project",
    "repo": "backend",
    "agent": "developer",
    "tags": ["feature", "implementation"]
})
uuid = response.json()["uuid"]
```

### cURL 示例

```bash
# 健康检查
curl http://localhost:8000/health

# 文本向量化
curl -X POST "http://localhost:8000/embedding" \
  -H "Content-Type: application/json" \
  -d '{"text": "测试文本"}'

# 批量处理
curl -X POST "http://localhost:8000/embedding/batch" \
  -H "Content-Type: application/json" \
  -d '{"texts": ["文本1", "文本2"]}'
```

## 🛠️ 环境要求

- Docker & Docker Compose
- OpenAI API 密钥

就这两个！Docker 会处理其他所有依赖。

## 📚 详细文档

- 📖 **[API 服务文档](api/README.md)** - 完整的 API 服务指南
- 🔍 **[API 参考手册](docs/api-reference.md)** - 详细的端点文档
- 🎯 **[使用示例](examples/api_usage_examples.py)** - 完整的使用示例
- ⚡ **[批量处理指南](docs/batch-processing-guide.md)** - 性能优化指南

## 🔧 开发模式

如果你想进行开发或贡献代码：

```bash
# 1. 安装 Python 依赖
pip install -r requirements.txt
pip install -r requirements-dev.txt

# 2. 启动 Weaviate 数据库
docker-compose up -d

# 3. 本地运行 API 服务
python api/start_api.py --mode dev

# 4. 运行测试
pytest --cov=vector tests/
```

## 📊 性能基准

| 操作 | 单次处理 | 批量处理 | 性能提升 |
|-----|---------|---------|---------|
| 文本向量化 | 800ms | 300ms (10个) | 60-80% |
| 缓存命中 | 50ms | 20ms (10个) | 1000x+ |
| 内存写入 | 1000ms | 400ms (10个) | 60% |

## 🎯 适用场景

- 🤖 **AI 应用**: RAG、语义搜索、聊天机器人
- 📚 **知识管理**: 文档检索、内容推荐
- 💬 **客服系统**: 智能问答、对话分析
- 🔍 **搜索引擎**: 语义搜索、相似度匹配

## 📄 开源使用指南

### 📋 引用要求

如果您在项目中使用本系统，请按照以下方式引用：

**在代码中引用**：
```python
# Powered by Doji Memory System
# Source: https://github.com/benzdriver/doji_memory
# Author: Ziyan Zhou
```

**在文档中引用**：
```markdown
本项目使用了 [Doji Memory System](https://github.com/benzdriver/doji_memory) 
作为向量存储解决方案，作者：Ziyan Zhou
```

**在学术论文中引用**：
```bibtex
@software{zhou2024_doji_memory_system,
  author = {Zhou, Ziyan},
  title = {Doji Memory System: Enterprise Vector Memory System},
  url = {https://github.com/benzdriver/doji_memory},
  year = {2024},
  note = {Open source vector storage and retrieval system}
}
```

### 🛡️ 反抄袭最佳实践

#### ✅ 鼓励的使用方式
- **学习参考**: 学习代码架构和实现思路
- **功能集成**: 将API集成到您的项目中
- **二次开发**: 基于本项目进行功能扩展
- **社区贡献**: 提交PR改进功能

#### ❌ 不当使用方式
- **直接复制**: 复制代码不注明来源
- **商业抄袭**: 去除版权信息后商业使用
- **恶意分发**: 修改作者信息后重新发布

#### 🔒 技术防护措施
- 代码中嵌入版权信息和源码链接
- API响应包含系统标识信息
- Docker镜像包含构建元数据
- 日志系统记录系统来源信息

### 📜 许可证说明

本项目采用 MIT 许可证，这意味着：

✅ **您可以**：
- 商业使用
- 修改代码
- 分发代码
- 私人使用

⚠️ **条件**：
- 保留版权声明
- 保留许可证声明
- 注明源项目

❌ **限制**：
- 作者不承担责任
- 不提供担保

## 🤝 贡献指南

欢迎贡献代码！请查看 [CONTRIBUTING.md](CONTRIBUTING.md) 了解详细指南。

### 🔄 贡献流程
1. Fork 本仓库
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送分支 (`git push origin feature/AmazingFeature`)
5. 提交 Pull Request

## 📞 支持与联系

- 👨‍💻 **作者**: Ziyan Zhou
- 📧 **邮箱**: [联系邮箱]
- 🐛 **问题报告**: [GitHub Issues](https://github.com/benzdriver/doji_memory/issues)
- 💬 **讨论**: [GitHub Discussions](https://github.com/benzdriver/doji_memory/discussions)
- 📖 **文档**: [项目文档](https://github.com/benzdriver/doji_memory/wiki)

## ⭐ 如果觉得有用，请给个Star！

如果这个项目对您有帮助，请考虑给个 Star ⭐ 来支持开发！

[![GitHub stars](https://img.shields.io/github/stars/benzdriver/doji_memory.svg?style=social&label=Star)](https://github.com/benzdriver/doji_memory/stargazers)

---

## 📜 第三方软件声明

本项目使用了以下开源软件，特此致谢：

### 核心依赖
- **[Weaviate](https://github.com/weaviate/weaviate)** - Vector Database (BSD-3-Clause License)
- **[OpenAI API](https://openai.com/)** - Text Embedding Service (Commercial License)
- **[FastAPI](https://github.com/tiangolo/fastapi)** - Web Framework (MIT License)

### 开发依赖
- **[Python](https://python.org/)** - Programming Language (PSF License)
- **[Docker](https://docker.com/)** - Containerization Platform (Apache 2.0 License)

完整的依赖列表和许可证信息请参见 `requirements.txt` 文件。

本项目遵循所有第三方软件的许可证要求，并感谢开源社区的贡献。

---

*Powered by Open Source Software 🙏*

---

<div align="center">

**🚀 企业级向量内存系统 | 由 Weaviate + OpenAI 驱动**

*Copyright © 2024 Ziyan Zhou. Released under the [MIT License](LICENSE).*

Made with ❤️ for the AI community

</div>
