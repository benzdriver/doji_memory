#!/usr/bin/env python3
"""
简单的API测试脚本
验证Weaviate Memory System API的基本功能
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from api.main import app
from fastapi.testclient import TestClient

def test_api_basic():
    """测试API基本功能"""
    client = TestClient(app)
    
    print("🚀 开始API基本功能测试...")
    
    # 1. 测试根目录
    print("\n1️⃣ 测试根目录端点...")
    response = client.get("/")
    print(f"状态码: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"✅ API名称: {data.get('name')}")
        print(f"✅ API版本: {data.get('version')}")
    else:
        print("❌ 根目录测试失败")
        return False
    
    # 2. 测试健康检查
    print("\n2️⃣ 测试健康检查端点...")
    response = client.get("/health")
    print(f"状态码: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"✅ 服务状态: {data.get('status')}")
        print(f"✅ API版本: {data.get('version')}")
        print(f"✅ 缓存状态: {data.get('cache_status')}")
    else:
        print("❌ 健康检查测试失败")
        return False
    
    # 3. 测试OpenAPI规范
    print("\n3️⃣ 测试OpenAPI规范...")
    response = client.get("/openapi.json")
    print(f"状态码: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"✅ OpenAPI版本: {data.get('openapi')}")
        print(f"✅ API标题: {data.get('info', {}).get('title')}")
        print(f"✅ 端点数量: {len(data.get('paths', {}))}")
    else:
        print("❌ OpenAPI规范测试失败")
        return False
    
    # 4. 测试文档页面
    print("\n4️⃣ 测试文档页面...")
    response = client.get("/docs")
    print(f"状态码: {response.status_code}")
    if response.status_code == 200:
        print("✅ Swagger UI 可访问")
    else:
        print("❌ Swagger UI 测试失败")
        return False
    
    response = client.get("/redoc")
    print(f"ReDoc状态码: {response.status_code}")
    if response.status_code == 200:
        print("✅ ReDoc 可访问")
    else:
        print("❌ ReDoc 测试失败")
        return False
    
    print("\n🎉 所有基本功能测试通过！")
    return True

def test_api_validation():
    """测试API数据验证"""
    client = TestClient(app)
    
    print("\n🔍 开始API数据验证测试...")
    
    # 测试空文本验证
    print("\n1️⃣ 测试空文本验证...")
    response = client.post("/embedding", json={"text": ""})
    print(f"状态码: {response.status_code}")
    if response.status_code == 422:  # Validation Error
        print("✅ 空文本验证正常工作")
    else:
        print("❌ 空文本验证失败")
        return False
    
    # 测试批量大小限制
    print("\n2️⃣ 测试批量大小限制...")
    large_texts = [f"文本{i}" for i in range(150)]  # 超过100个限制
    response = client.post("/embedding/batch", json={"texts": large_texts})
    print(f"状态码: {response.status_code}")
    if response.status_code == 422:  # Validation Error
        print("✅ 批量大小限制正常工作")
    else:
        print("❌ 批量大小限制失败")
        return False
    
    print("\n🎉 所有数据验证测试通过！")
    return True

def main():
    """运行所有测试"""
    print("🚀 Weaviate Memory System API 测试")
    print("=" * 50)
    
    try:
        # 基本功能测试
        if not test_api_basic():
            print("❌ 基本功能测试失败")
            sys.exit(1)
        
        # 数据验证测试
        if not test_api_validation():
            print("❌ 数据验证测试失败")
            sys.exit(1)
        
        print("\n" + "=" * 50)
        print("🎉 所有API测试通过！")
        print("\n📖 访问API文档:")
        print("- Swagger UI: http://localhost:8000/docs")
        print("- ReDoc: http://localhost:8000/redoc")
        print("- OpenAPI JSON: http://localhost:8000/openapi.json")
        
    except Exception as e:
        print(f"❌ 测试过程中出错: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 