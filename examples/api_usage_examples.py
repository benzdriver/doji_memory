"""
Weaviate Memory System API 使用示例

展示如何通过REST API调用各种功能：
- 文本向量化（单个和批量）
- 内存管理（写入和检索）
- 缓存管理
- 系统监控
"""

import requests
import json
import time
from typing import List, Dict, Any

# API基础配置
API_BASE_URL = "http://localhost:8000"
HEADERS = {"Content-Type": "application/json"}

class WeaviateMemoryAPI:
    """Weaviate Memory System API 客户端"""
    
    def __init__(self, base_url: str = API_BASE_URL):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update(HEADERS)
    
    def health_check(self) -> Dict[str, Any]:
        """健康检查"""
        response = self.session.get(f"{self.base_url}/health")
        response.raise_for_status()
        return response.json()
    
    def embed_text(self, text: str, use_cache: bool = True, metadata: Dict = None) -> Dict[str, Any]:
        """单文本向量化"""
        payload = {
            "text": text,
            "use_cache": use_cache,
            "metadata": metadata
        }
        
        response = self.session.post(f"{self.base_url}/embedding", json=payload)
        response.raise_for_status()
        return response.json()
    
    def embed_texts_batch(self, texts: List[str], use_cache: bool = True, 
                         metadata: List[Dict] = None) -> Dict[str, Any]:
        """批量文本向量化"""
        payload = {
            "texts": texts,
            "use_cache": use_cache,
            "metadata": metadata
        }
        
        response = self.session.post(f"{self.base_url}/embedding/batch", json=payload)
        response.raise_for_status()
        return response.json()
    
    def write_memory(self, content: str, project: str, repo: str, 
                    agent: str, tags: List[str], source: str = "agent") -> Dict[str, Any]:
        """写入单条内存"""
        payload = {
            "content": content,
            "project": project,
            "repo": repo,
            "agent": agent,
            "tags": tags,
            "source": source
        }
        
        response = self.session.post(f"{self.base_url}/memory", json=payload)
        response.raise_for_status()
        return response.json()
    
    def write_memories_batch(self, memories: List[Dict[str, Any]]) -> Dict[str, Any]:
        """批量写入内存"""
        payload = {"memories": memories}
        
        response = self.session.post(f"{self.base_url}/memory/batch", json=payload)
        response.raise_for_status()
        return response.json()
    
    def get_cache_info(self) -> Dict[str, Any]:
        """获取缓存信息"""
        response = self.session.get(f"{self.base_url}/cache/info")
        response.raise_for_status()
        return response.json()
    
    def clear_cache(self) -> Dict[str, Any]:
        """清空缓存"""
        response = self.session.delete(f"{self.base_url}/cache")
        response.raise_for_status()
        return response.json()

def example_1_basic_embedding():
    """示例1: 基础文本向量化"""
    print("=== 示例1: 基础文本向量化 ===")
    
    api = WeaviateMemoryAPI()
    
    # 健康检查
    health = api.health_check()
    print(f"🏥 系统状态: {health['status']}")
    
    # 单文本向量化
    text = "这是一个测试文本，用于演示API功能"
    result = api.embed_text(text)
    
    print(f"📝 输入文本: {text}")
    print(f"🧠 向量维度: {len(result['vector'])}")
    print(f"💾 使用缓存: {result['cached']}")
    print(f"⏱️ 处理时间: {result['processing_time']:.3f}秒")
    
    # 再次调用同样文本（应该命中缓存）
    result2 = api.embed_text(text)
    print(f"🔄 第二次调用缓存命中: {result2['cached']}")
    print(f"⚡ 缓存响应时间: {result2['processing_time']:.3f}秒")

def example_2_batch_embedding():
    """示例2: 批量文本向量化"""
    print("\n=== 示例2: 批量文本向量化 ===")
    
    api = WeaviateMemoryAPI()
    
    # 准备批量文本
    texts = [
        "Python是一种高级编程语言",
        "机器学习是人工智能的一个分支",
        "向量数据库用于存储和检索高维向量",
        "FastAPI是一个现代的Python Web框架",
        "Weaviate是一个开源的向量数据库"
    ]
    
    # 批量处理
    start_time = time.time()
    result = api.embed_texts_batch(texts)
    total_time = time.time() - start_time
    
    print(f"📋 输入文本数量: {len(texts)}")
    print(f"🧠 输出向量数量: {len(result['vectors'])}")
    print(f"💾 缓存命中: {result['cache_hits']}")
    print(f"❌ 缓存未命中: {result['cache_misses']}")
    print(f"⏱️ API处理时间: {result['processing_time']:.3f}秒")
    print(f"🚀 性能提升: {result['performance_gain']:.1f}%")
    print(f"📊 总调用时间: {total_time:.3f}秒")

def example_3_memory_management():
    """示例3: 内存管理"""
    print("\n=== 示例3: 内存管理 ===")
    
    api = WeaviateMemoryAPI()
    
    # 写入单条内存
    memory_result = api.write_memory(
        content="实现了用户认证功能",
        project="web-app",
        repo="backend",
        agent="developer-001",
        tags=["feature", "auth", "security"],
        source="development"
    )
    
    print(f"💾 内存记录UUID: {memory_result['uuid']}")
    print(f"⏱️ 写入时间: {memory_result['processing_time']:.3f}秒")
    
    # 批量写入内存
    memories = [
        {
            "content": "修复了登录页面的UI问题",
            "project": "web-app",
            "repo": "frontend", 
            "agent": "developer-002",
            "tags": ["bugfix", "ui", "login"],
            "source": "development"
        },
        {
            "content": "优化了数据库查询性能",
            "project": "web-app",
            "repo": "backend",
            "agent": "developer-003", 
            "tags": ["optimization", "database", "performance"],
            "source": "development"
        },
        {
            "content": "添加了API文档",
            "project": "web-app",
            "repo": "docs",
            "agent": "tech-writer",
            "tags": ["documentation", "api"],
            "source": "documentation"
        }
    ]
    
    batch_result = api.write_memories_batch(memories)
    
    print(f"📦 批量写入成功: {batch_result['success_count']}/{batch_result['total_count']}")
    print(f"⏱️ 批量处理时间: {batch_result['processing_time']:.3f}秒")
    print(f"🆔 生成的UUIDs: {len(batch_result['uuids'])}")

def example_4_cache_management():
    """示例4: 缓存管理"""
    print("\n=== 示例4: 缓存管理 ===")
    
    api = WeaviateMemoryAPI()
    
    # 获取缓存信息
    cache_info = api.get_cache_info()
    
    print(f"💾 缓存条目数: {cache_info['num_entries']}")
    print(f"📊 缓存大小: {cache_info['total_size_bytes'] / 1024 / 1024:.2f} MB")
    print(f"🎯 缓存命中率: {cache_info['hit_rate'] * 100:.1f}%")

def example_5_performance_comparison():
    """示例5: 性能对比"""
    print("\n=== 示例5: 性能对比（单个 vs 批量） ===")
    
    api = WeaviateMemoryAPI()
    
    # 测试文本
    test_texts = [
        f"这是测试文本 {i}" for i in range(20)
    ]
    
    # 方法1: 逐个处理
    print("🐌 方法1: 逐个处理")
    start_time = time.time()
    individual_results = []
    for text in test_texts:
        result = api.embed_text(text)
        individual_results.append(result['vector'])
    individual_time = time.time() - start_time
    
    print(f"⏱️ 总耗时: {individual_time:.3f}秒")
    print(f"📊 平均每个文本: {individual_time / len(test_texts):.3f}秒")
    
    # 清空缓存以确保公平比较
    api.clear_cache()
    print("🧹 已清空缓存")
    
    # 方法2: 批量处理
    print("\n🚀 方法2: 批量处理")
    start_time = time.time()
    batch_result = api.embed_texts_batch(test_texts)
    batch_time = time.time() - start_time
    
    print(f"⏱️ 总耗时: {batch_time:.3f}秒")
    print(f"📊 平均每个文本: {batch_time / len(test_texts):.3f}秒")
    
    # 性能对比
    speedup = individual_time / batch_time
    print(f"\n🏆 性能提升倍数: {speedup:.2f}x")
    print(f"⚡ 性能提升百分比: {(speedup - 1) * 100:.1f}%")

def example_6_error_handling():
    """示例6: 错误处理"""
    print("\n=== 示例6: 错误处理 ===")
    
    api = WeaviateMemoryAPI()
    
    # 测试空文本错误
    try:
        result = api.embed_text("")
    except requests.exceptions.HTTPError as e:
        print(f"❌ 空文本错误: {e}")
        print(f"📋 响应详情: {e.response.json()}")
    
    # 测试过长批次错误  
    try:
        long_texts = [f"文本 {i}" for i in range(150)]  # 超过100个限制
        result = api.embed_texts_batch(long_texts)
    except requests.exceptions.HTTPError as e:
        print(f"❌ 批量大小错误: {e}")
        print(f"📋 响应详情: {e.response.json()}")

def example_7_real_world_scenario():
    """示例7: 真实场景应用"""
    print("\n=== 示例7: 真实场景 - 客服对话处理 ===")
    
    api = WeaviateMemoryAPI()
    
    # 模拟客服对话数据
    conversations = [
        {
            "content": "用户询问如何重置密码",
            "project": "customer-support",
            "repo": "conversations",
            "agent": "support-agent-01",
            "tags": ["password", "reset", "help"],
            "source": "live-chat"
        },
        {
            "content": "用户报告登录问题，提供了错误截图",
            "project": "customer-support", 
            "repo": "conversations",
            "agent": "support-agent-02",
            "tags": ["login", "error", "screenshot"],
            "source": "live-chat"
        },
        {
            "content": "用户询问产品功能和定价",
            "project": "customer-support",
            "repo": "conversations", 
            "agent": "support-agent-01",
            "tags": ["product", "pricing", "inquiry"],
            "source": "live-chat"
        }
    ]
    
    # 批量处理客服对话
    start_time = time.time()
    result = api.write_memories_batch(conversations)
    processing_time = time.time() - start_time
    
    print(f"💬 处理对话数量: {len(conversations)}")
    print(f"✅ 成功处理: {result['success_count']}")
    print(f"⏱️ 处理时间: {processing_time:.3f}秒")
    print(f"📊 平均每条对话: {processing_time / len(conversations):.3f}秒")
    
    # 显示处理结果
    for i, uuid in enumerate(result['uuids']):
        conv = conversations[i]
        print(f"📝 对话{i+1}: {conv['content'][:30]}... -> UUID: {uuid[:8]}...")

def main():
    """运行所有示例"""
    print("🚀 Weaviate Memory System API 使用示例")
    print("=" * 50)
    
    try:
        # 运行所有示例
        example_1_basic_embedding()
        example_2_batch_embedding()
        example_3_memory_management()
        example_4_cache_management()
        example_5_performance_comparison()
        example_6_error_handling()
        example_7_real_world_scenario()
        
        print("\n✅ 所有示例运行完成！")
        print("\n📖 更多信息:")
        print("- API文档: http://localhost:8000/docs")
        print("- ReDoc文档: http://localhost:8000/redoc")
        print("- 健康检查: http://localhost:8000/health")
        
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到API服务器")
        print("请确保API服务正在运行:")
        print("python api/start_api.py --mode dev")
    except Exception as e:
        print(f"❌ 运行示例时出错: {e}")

if __name__ == "__main__":
    main() 