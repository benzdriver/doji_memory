#!/usr/bin/env python3
"""
Weaviate Memory System API 启动脚本

提供多种启动模式：
- 开发模式：热重载，详细日志
- 生产模式：多进程，性能优化
- Docker模式：容器化部署
"""

import os
import sys
import argparse
import uvicorn
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def check_dependencies():
    """检查依赖是否已安装"""
    required_packages = [
        'fastapi',
        'uvicorn', 
        'pydantic',
        'openai',
        'weaviate'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ 缺少以下依赖包: {', '.join(missing_packages)}")
        print("请运行以下命令安装依赖:")
        print("pip install -r requirements.txt")
        print("pip install -r api/requirements-api.txt")
        sys.exit(1)
    
    print("✅ 所有依赖已安装")

def check_environment():
    """检查环境变量"""
    required_env_vars = ['OPENAI_API_KEY']
    missing_vars = []
    
    for var in required_env_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"⚠️ 缺少以下环境变量: {', '.join(missing_vars)}")
        print("请设置以下环境变量:")
        for var in missing_vars:
            print(f"export {var}=your_value")
        
        # 在开发模式下，提供默认值提示
        if 'OPENAI_API_KEY' in missing_vars:
            print("\n💡 你可以创建 .env 文件来设置环境变量:")
            print("echo 'OPENAI_API_KEY=your_openai_api_key' > .env")
    else:
        print("✅ 环境变量配置正确")

def start_development():
    """启动开发模式"""
    print("🚀 启动开发模式...")
    print("📍 API文档地址: http://localhost:8000/docs")
    print("📍 ReDoc文档: http://localhost:8000/redoc")
    print("📍 健康检查: http://localhost:8000/health")
    
    uvicorn.run(
        "api.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        reload_dirs=["api", "vector"],
        log_level="info",
        access_log=True
    )

def start_production():
    """启动生产模式"""
    import multiprocessing
    
    workers = multiprocessing.cpu_count()
    print(f"🚀 启动生产模式（{workers} 个工作进程）...")
    print("📍 API地址: http://0.0.0.0:8000")
    
    uvicorn.run(
        "api.main:app",
        host="0.0.0.0",
        port=8000,
        workers=workers,
        log_level="warning",
        access_log=False
    )

def start_custom(host, port, workers, reload):
    """自定义启动模式"""
    print(f"🚀 启动自定义模式...")
    print(f"📍 地址: http://{host}:{port}")
    print(f"📍 工作进程: {workers}")
    print(f"📍 热重载: {'开启' if reload else '关闭'}")
    
    uvicorn.run(
        "api.main:app",
        host=host,
        port=port,
        workers=workers if not reload else 1,  # reload模式下只能单进程
        reload=reload,
        log_level="info"
    )

def generate_openapi_spec():
    """生成OpenAPI规范文件"""
    try:
        from api.main import app
        import json
        
        openapi_spec = app.openapi()
        
        # 保存为JSON文件
        spec_file = project_root / "api" / "openapi.json"
        with open(spec_file, 'w', encoding='utf-8') as f:
            json.dump(openapi_spec, f, indent=2, ensure_ascii=False)
        
        print(f"✅ OpenAPI规范已生成: {spec_file}")
        
        # 保存为YAML文件
        try:
            import yaml
            yaml_file = project_root / "api" / "openapi.yaml" 
            with open(yaml_file, 'w', encoding='utf-8') as f:
                yaml.dump(openapi_spec, f, default_flow_style=False, allow_unicode=True)
            print(f"✅ OpenAPI YAML规范已生成: {yaml_file}")
        except ImportError:
            print("💡 安装PyYAML来生成YAML格式: pip install PyYAML")
            
    except Exception as e:
        print(f"❌ 生成OpenAPI规范失败: {e}")

def main():
    parser = argparse.ArgumentParser(description='Weaviate Memory System API 启动器')
    parser.add_argument('--mode', 
                       choices=['dev', 'prod', 'custom'], 
                       default='dev',
                       help='启动模式 (默认: dev)')
    parser.add_argument('--host', 
                       default='127.0.0.1', 
                       help='绑定主机 (默认: 127.0.0.1)')
    parser.add_argument('--port', 
                       type=int, 
                       default=8000, 
                       help='绑定端口 (默认: 8000)')
    parser.add_argument('--workers', 
                       type=int, 
                       default=1, 
                       help='工作进程数 (默认: 1)')
    parser.add_argument('--reload', 
                       action='store_true', 
                       help='启用热重载')
    parser.add_argument('--check-deps', 
                       action='store_true', 
                       help='检查依赖')
    parser.add_argument('--check-env', 
                       action='store_true', 
                       help='检查环境变量')
    parser.add_argument('--generate-spec', 
                       action='store_true', 
                       help='生成OpenAPI规范文件')
    
    args = parser.parse_args()
    
    # 执行检查命令
    if args.check_deps:
        check_dependencies()
        return
        
    if args.check_env:
        check_environment()
        return
        
    if args.generate_spec:
        generate_openapi_spec()
        return
    
    # 启动前检查
    print("🔍 检查系统状态...")
    check_dependencies()
    check_environment()
    
    # 启动API服务
    if args.mode == 'dev':
        start_development()
    elif args.mode == 'prod':
        start_production()
    elif args.mode == 'custom':
        start_custom(args.host, args.port, args.workers, args.reload)

if __name__ == "__main__":
    main() 