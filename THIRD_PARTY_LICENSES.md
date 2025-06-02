# 第三方许可证声明

本文档列出了 Doji Memory System 项目中使用的所有第三方软件及其许可证信息。

## 核心依赖

### Weaviate Vector Database
- **项目**: [Weaviate](https://github.com/weaviate/weaviate)
- **版权**: Copyright (c) 2024 Weaviate, B.V.
- **许可证**: BSD-3-Clause License
- **用途**: 向量数据库核心组件
- **许可证文本**: https://github.com/weaviate/weaviate/blob/master/LICENSE

### OpenAI API
- **项目**: OpenAI API
- **版权**: Copyright (c) 2024 OpenAI
- **许可证**: Commercial License (付费服务)
- **用途**: 文本向量化服务
- **使用条款**: https://openai.com/terms/

### FastAPI
- **项目**: [FastAPI](https://github.com/tiangolo/fastapi)
- **版权**: Copyright (c) 2018 Sebastián Ramírez
- **许可证**: MIT License
- **用途**: Web API框架
- **许可证文本**: https://github.com/tiangolo/fastapi/blob/master/LICENSE

## Python依赖

### 运行时依赖
- **weaviate-client**: Apache-2.0 License
- **openai**: MIT License
- **pydantic**: MIT License
- **uvicorn**: BSD-3-Clause License
- **python-dotenv**: BSD-3-Clause License

### 开发依赖
- **pytest**: MIT License
- **pytest-cov**: MIT License
- **black**: MIT License
- **flake8**: MIT License
- **mypy**: MIT License

## 基础设施

### Docker
- **项目**: [Docker](https://github.com/moby/moby)
- **版权**: Copyright (c) 2013-2024 Docker, Inc.
- **许可证**: Apache-2.0 License
- **用途**: 容器化部署

### Python
- **项目**: [Python Programming Language](https://github.com/python/cpython)
- **版权**: Copyright (c) Python Software Foundation
- **许可证**: PSF License
- **用途**: 编程语言运行时

## 许可证兼容性

所有使用的第三方软件许可证都与本项目的MIT许可证兼容：

| 许可证类型 | 兼容性 | 商业使用 | 修改 | 分发 |
|-----------|--------|----------|------|------|
| MIT | ✅ 兼容 | ✅ 允许 | ✅ 允许 | ✅ 允许 |
| BSD-3-Clause | ✅ 兼容 | ✅ 允许 | ✅ 允许 | ✅ 允许 |
| Apache-2.0 | ✅ 兼容 | ✅ 允许 | ✅ 允许 | ✅ 允许 |
| PSF | ✅ 兼容 | ✅ 允许 | ✅ 允许 | ✅ 允许 |

## 合规声明

本项目严格遵循所有第三方软件的许可证要求：

1. ✅ **保留版权声明**: 所有原始版权信息已保留
2. ✅ **许可证分发**: 相关许可证文本已包含
3. ✅ **归属声明**: 在文档中明确注明来源
4. ✅ **条款遵循**: 符合所有使用条款和限制

## 感谢

特别感谢以下开源项目和公司：

- 🙏 **Weaviate团队** - 提供优秀的向量数据库
- 🙏 **OpenAI** - 提供强大的文本嵌入API
- 🙏 **FastAPI社区** - 提供现代化的Web框架
- 🙏 **Python社区** - 提供强大的编程语言和生态系统

## 更新说明

本文档会随着项目依赖的更新而同步更新。如有疑问或发现遗漏，请通过以下方式联系：

- 📧 提交Issue: https://github.com/benzdriver/doji_memory/issues
- 📝 提交PR: https://github.com/benzdriver/doji_memory/pulls

---

*最后更新: 2024年*  
*维护者: Ziyan Zhou* 