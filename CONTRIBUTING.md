# 🤝 贡献指南

感谢您对 Weaviate Memory System 的关注！我们欢迎任何形式的贡献。

## 📋 贡献类型

- 🐛 **Bug 报告**: 发现问题，帮助我们改进
- 💡 **功能建议**: 提出新的功能想法
- 📖 **文档改进**: 完善文档和示例
- 💻 **代码贡献**: 修复 bug 或添加新功能
- 🧪 **测试用例**: 增加测试覆盖率
- 🌐 **国际化**: 添加多语言支持

## 🚀 快速开始

### 环境要求

- Python 3.9+
- Docker & Docker Compose
- Git
- OpenAI API 密钥

### 开发环境设置

```bash
# 1. Fork 并克隆仓库
git clone https://github.com/YOUR_USERNAME/weaviate-memory-syste.git
cd weaviate-memory-syste

# 2. 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或 .\venv\Scripts\activate  # Windows

# 3. 安装依赖
pip install -r requirements.txt
pip install -r requirements-dev.txt

# 4. 配置环境变量
cp .env.example .env
# 编辑 .env 文件，添加您的 OpenAI API 密钥

# 5. 启动开发环境
docker-compose up -d  # 启动 Weaviate
python api/start_api.py --mode dev  # 启动 API 服务

# 6. 运行测试
pytest --cov=vector tests/
```

## 📝 代码规范

### Python 代码风格

我们使用以下工具确保代码质量：

```bash
# 代码格式化
black .
isort .

# 代码检查
flake8 .
mypy .

# 安全检查
bandit -r .
```

### 提交信息规范

请使用 [Conventional Commits](https://www.conventionalcommits.org/) 格式：

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

**类型**：
- `feat`: 新功能
- `fix`: 修复 bug
- `docs`: 文档更新
- `style`: 代码格式调整
- `refactor`: 重构代码
- `test`: 添加或修改测试
- `chore`: 其他改动

**示例**：
```
feat(api): add batch embedding endpoint

Add new endpoint for processing multiple texts in a single request.
This improves performance by 60-80% compared to individual requests.

Closes #123
```

## 🔄 贡献流程

### 1. 准备工作

```bash
# 确保您的 fork 是最新的
git remote add upstream https://github.com/benzdriver/weaviate-memory-syste.git
git fetch upstream
git checkout main
git merge upstream/main
```

### 2. 创建功能分支

```bash
# 创建并切换到新分支
git checkout -b feature/your-feature-name
# 或
git checkout -b fix/your-bug-fix
```

### 3. 开发和测试

```bash
# 进行开发工作
# ...

# 运行测试确保代码质量
pytest --cov=vector tests/
python -m flake8 .
python -m black --check .
python -m isort --check-only .
```

### 4. 提交更改

```bash
# 添加更改
git add .

# 提交更改（使用规范的提交信息）
git commit -m "feat: add new feature description"

# 推送到您的 fork
git push origin feature/your-feature-name
```

### 5. 创建 Pull Request

1. 在 GitHub 上导航到您的 fork
2. 点击 "Compare & pull request"
3. 填写 PR 描述，包括：
   - 更改的简要描述
   - 相关的 issue 编号
   - 测试说明
   - 截图（如适用）

## 🧪 测试指南

### 运行测试

```bash
# 运行所有测试
pytest

# 运行特定测试文件
pytest tests/test_embedding.py

# 查看覆盖率报告
pytest --cov=vector tests/ --cov-report=html
```

### 添加新测试

请为新功能添加相应的测试：

```python
# tests/test_new_feature.py
import pytest
from vector.new_feature import NewFeature

def test_new_feature():
    """测试新功能的基本行为"""
    feature = NewFeature()
    result = feature.do_something()
    assert result == expected_value

def test_new_feature_edge_case():
    """测试边界情况"""
    feature = NewFeature()
    with pytest.raises(ValueError):
        feature.do_something_invalid()
```

## 📚 文档贡献

### API 文档

API 文档使用 FastAPI 自动生成，但您可以：

- 改进 docstring
- 添加使用示例
- 更新 README 和其他文档

### 文档格式

```python
def your_function(param1: str, param2: int = 10) -> dict:
    """
    函数的简短描述。
    
    详细说明函数的作用和使用方法。
    
    Args:
        param1: 参数1的描述
        param2: 参数2的描述，默认值为10
        
    Returns:
        返回值的描述
        
    Raises:
        ValueError: 当参数无效时抛出
        
    Example:
        >>> result = your_function("test", 20)
        >>> print(result)
        {'status': 'success'}
    """
    pass
```

## 🐛 Bug 报告

请使用 [GitHub Issues](https://github.com/benzdriver/weaviate-memory-syste/issues) 报告 bug，包括：

### Bug 报告模板

```markdown
**Bug 描述**
简要描述遇到的问题。

**复现步骤**
1. 进入 '...'
2. 点击 '....'
3. 滚动到 '....'
4. 看到错误

**期望行为**
描述您期望发生的情况。

**实际行为**
描述实际发生的情况。

**环境信息**
- OS: [e.g. macOS 12.0]
- Python: [e.g. 3.9.7]
- Docker: [e.g. 20.10.8]

**额外信息**
其他可能有用的信息，如日志、截图等。
```

## 💡 功能建议

使用 [GitHub Issues](https://github.com/benzdriver/weaviate-memory-syste/issues) 提出功能建议：

### 功能建议模板

```markdown
**功能描述**
描述您想要的功能。

**动机**
解释为什么需要这个功能，它解决什么问题。

**详细设计**
如果有的话，描述您期望的具体实现方式。

**替代方案**
描述您考虑过的其他解决方案。

**额外信息**
其他相关信息。
```

## 🔒 安全问题

如果发现安全漏洞，请不要在公开的 issue 中报告。请发送邮件到：[security@your-domain.com]

## 📄 许可证

通过贡献代码，您同意您的贡献将在 [MIT License](LICENSE) 下发布。

## 🙏 感谢

感谢所有贡献者！您的努力让这个项目变得更好。

### 贡献者

- [Ziyan Zhou](https://github.com/benzdriver) - 项目创始人和维护者

## 📞 获取帮助

如果您在贡献过程中遇到问题，可以：

- 查看 [文档](README.md)
- 搜索 [已有的 issues](https://github.com/benzdriver/weaviate-memory-syste/issues)
- 在 [Discussions](https://github.com/benzdriver/weaviate-memory-syste/discussions) 中提问
- 联系维护者

---

再次感谢您的贡献！🚀 