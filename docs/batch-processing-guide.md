# 批量处理功能完整指南

> **Version**: 1.0  
> **Last Updated**: 2024-12-19  
> **Author**: Weaviate Memory System Team

## 📋 目录

- [概述](#概述)
- [核心概念](#核心概念)
- [使用场景](#使用场景)
- [API参考](#api参考)
- [实践案例](#实践案例)
- [性能优化](#性能优化)
- [最佳实践](#最佳实践)
- [故障排除](#故障排除)

---

## 📖 概述

批量处理功能是Weaviate Memory System的核心特性之一，旨在显著提高大规模文本处理的效率。通过智能缓存和API调用优化，批量处理可以将性能提升60%以上。

### 🎯 主要优势

- **🚀 性能提升**: 60-80%的处理速度提升
- **💰 成本优化**: 减少API调用次数，降低成本
- **🧠 智能缓存**: 自动检测缓存命中，避免重复计算
- **🔧 易于使用**: 与单文本API保持一致的使用体验

---

## 🔑 核心概念

### 批量Embedding生成

```python
# 单文本处理（传统方式）
vector1 = embed_text("文本1")
vector2 = embed_text("文本2") 
vector3 = embed_text("文本3")

# 批量处理（优化方式）
vectors = embed_texts_batch(["文本1", "文本2", "文本3"])
```

### 批量内存写入

```python
# 单个写入（传统方式）
uuid1 = write_memory(content="内容1", project="proj", repo="repo", agent="agent", tags=["tag1"])
uuid2 = write_memory(content="内容2", project="proj", repo="repo", agent="agent", tags=["tag2"])

# 批量写入（优化方式）
memories = [
    {"content": "内容1", "project": "proj", "repo": "repo", "agent": "agent", "tags": ["tag1"]},
    {"content": "内容2", "project": "proj", "repo": "repo", "agent": "agent", "tags": ["tag2"]}
]
uuids = write_memories_batch(memories)
```

### 智能缓存机制

```
输入: ["已缓存文本", "新文本", "已缓存文本2"]
      ↓
缓存检查: [✅ 命中, ❌ 未命中, ✅ 命中]
      ↓
API调用: 只处理 "新文本"
      ↓
结果组装: [缓存值, API结果, 缓存值]
```

---

## 🎯 使用场景

### 场景1: 知识库批量导入

**业务需求**: 将大量文档批量导入知识库系统

```python
def import_knowledge_base(documents):
    """批量导入知识库文档"""
    
    # 配置批次大小
    BATCH_SIZE = 50
    total_imported = 0
    
    for i in range(0, len(documents), BATCH_SIZE):
        batch = documents[i:i + BATCH_SIZE]
        
        # 准备批量内存数据
        memories = []
        for doc in batch:
            memories.append({
                "content": doc.content,
                "project": "knowledge-base",
                "repo": doc.source_repo,
                "agent": "import-bot",
                "tags": ["knowledge", doc.category, doc.language],
                "source": "document-import"
            })
        
        # 批量写入
        try:
            uuids = write_memories_batch(memories)
            total_imported += len(uuids)
            
            print(f"✅ 批次 {i//BATCH_SIZE + 1}: 成功导入 {len(uuids)} 个文档")
            print(f"📊 总进度: {total_imported}/{len(documents)} ({total_imported/len(documents)*100:.1f}%)")
            
        except Exception as e:
            print(f"❌ 批次 {i//BATCH_SIZE + 1} 导入失败: {e}")
            continue
    
    return total_imported
```

**使用示例**:
```python
# 准备文档数据
documents = [
    Document(content="Python编程指南...", source_repo="docs", category="programming", language="zh"),
    Document(content="API接口文档...", source_repo="api", category="reference", language="zh"),
    # ... 更多文档
]

# 执行批量导入
imported_count = import_knowledge_base(documents)
print(f"🎉 总共成功导入 {imported_count} 个文档")
```

### 场景2: 实时对话记录处理

**业务需求**: 处理客服系统中积累的对话记录

```python
class ConversationProcessor:
    """对话记录批量处理器"""
    
    def __init__(self):
        self.batch_size = 30
        self.pending_conversations = []
    
    def add_conversation(self, conversation):
        """添加单个对话到待处理队列"""
        self.pending_conversations.append(conversation)
        
        # 达到批次大小时自动处理
        if len(self.pending_conversations) >= self.batch_size:
            self.process_batch()
    
    def process_batch(self):
        """处理当前批次的对话"""
        if not self.pending_conversations:
            return
        
        memories = []
        for conv in self.pending_conversations:
            memories.append({
                "content": conv.content,
                "project": "customer-support",
                "repo": f"conversations-{conv.language}",
                "agent": conv.agent_id,
                "tags": ["customer-support", conv.category, conv.language, conv.sentiment],
                "source": "live-chat"
            })
        
        try:
            uuids = write_memories_batch(memories)
            print(f"✅ 成功处理 {len(uuids)} 条对话记录")
            
            # 清空待处理队列
            self.pending_conversations.clear()
            
        except Exception as e:
            print(f"❌ 批量处理失败: {e}")
    
    def flush(self):
        """强制处理剩余的对话"""
        if self.pending_conversations:
            self.process_batch()
```

**使用示例**:
```python
processor = ConversationProcessor()

# 模拟实时对话流
for conversation in real_time_conversations:
    processor.add_conversation(conversation)

# 确保所有对话都被处理
processor.flush()
```

### 场景3: 代码仓库分析

**业务需求**: 分析Git仓库的提交记录和代码注释

```python
def analyze_repository_commits(repo_path, since_date=None):
    """分析仓库提交记录"""
    
    # 获取提交信息（示例，实际需要使用git库）
    commits = get_git_commits(repo_path, since=since_date)
    
    # 按时间段分组批量处理
    commit_batches = group_commits_by_timeframe(commits, days=7)
    
    all_results = []
    
    for week, week_commits in commit_batches.items():
        print(f"📅 处理 {week} 的提交记录 ({len(week_commits)} 个提交)")
        
        # 准备批量数据
        commit_memories = []
        for commit in week_commits:
            # 结合提交信息和代码差异
            content = f"提交: {commit.message}\n文件变更: {', '.join(commit.changed_files)}\n代码行数: +{commit.additions}/-{commit.deletions}"
            
            commit_memories.append({
                "content": content,
                "project": f"repo-{repo_path.name}",
                "repo": commit.branch,
                "agent": commit.author,
                "tags": ["git-commit", commit.type, f"week-{week}"],
                "source": "git-analysis"
            })
        
        # 批量处理提交记录
        try:
            uuids = write_memories_batch(commit_memories)
            all_results.extend(uuids)
            
            print(f"✅ 成功分析 {len(uuids)} 个提交")
            
        except Exception as e:
            print(f"❌ 处理 {week} 提交失败: {e}")
            continue
    
    return all_results
```

### 场景4: 多语言内容处理

**业务需求**: 处理多语言客服数据

```python
class MultilingualProcessor:
    """多语言内容批量处理器"""
    
    def __init__(self):
        self.language_queues = {}
        self.batch_sizes = {
            'zh': 40,  # 中文批次大小
            'en': 50,  # 英文批次大小  
            'ja': 30,  # 日文批次大小
            'default': 35
        }
    
    def add_content(self, content, language, metadata):
        """添加内容到对应语言队列"""
        if language not in self.language_queues:
            self.language_queues[language] = []
        
        self.language_queues[language].append({
            'content': content,
            'language': language,
            'metadata': metadata
        })
        
        # 检查是否需要处理该语言的批次
        batch_size = self.batch_sizes.get(language, self.batch_sizes['default'])
        if len(self.language_queues[language]) >= batch_size:
            self.process_language_batch(language)
    
    def process_language_batch(self, language):
        """处理特定语言的批次"""
        if language not in self.language_queues or not self.language_queues[language]:
            return
        
        items = self.language_queues[language]
        
        # 为该语言优化的处理逻辑
        memories = []
        for item in items:
            memories.append({
                "content": item['content'],
                "project": "multilingual-support",
                "repo": f"content-{language}",
                "agent": item['metadata'].get('agent', 'system'),
                "tags": ["multilingual", language, item['metadata'].get('category', 'general')],
                "source": f"multilingual-{language}"
            })
        
        try:
            uuids = write_memories_batch(memories)
            print(f"🌐 {language.upper()}: 成功处理 {len(uuids)} 条内容")
            
            # 清空该语言队列
            self.language_queues[language].clear()
            
        except Exception as e:
            print(f"❌ {language.upper()} 批次处理失败: {e}")
    
    def process_all_remaining(self):
        """处理所有剩余的内容"""
        for language in list(self.language_queues.keys()):
            if self.language_queues[language]:
                self.process_language_batch(language)
```

**使用示例**:
```python
processor = MultilingualProcessor()

# 模拟多语言内容流
multilingual_contents = [
    ("你好，我需要帮助", "zh", {"agent": "agent-01", "category": "help"}),
    ("Hello, I have a question", "en", {"agent": "agent-02", "category": "question"}),
    ("こんにちは、質問があります", "ja", {"agent": "agent-03", "category": "question"}),
]

for content, lang, meta in multilingual_contents:
    processor.add_content(content, lang, meta)

# 处理所有剩余内容
processor.process_all_remaining()
```

---

## 🔧 API参考

### embed_texts_batch()

批量生成文本嵌入向量。

**签名**:
```python
def embed_texts_batch(
    texts: List[str], 
    metadata: Optional[List[Dict]] = None
) -> List[List[float]]
```

**参数**:
- `texts`: 要处理的文本列表
- `metadata`: 可选的元数据列表，长度必须与texts相同

**返回值**: 
- `List[List[float]]`: 嵌入向量列表，顺序与输入文本对应

**异常**:
- `ValueError`: 输入参数无效
- `OpenAIError`: OpenAI API调用失败

**示例**:
```python
# 基本使用
texts = ["文本1", "文本2", "文本3"]
vectors = embed_texts_batch(texts)

# 带元数据
metadata = [{"type": "title"}, {"type": "content"}, {"type": "summary"}]
vectors = embed_texts_batch(texts, metadata=metadata)
```

### write_memories_batch()

批量写入内存记录到Weaviate数据库。

**签名**:
```python
def write_memories_batch(
    memories: List[Dict[str, Any]]
) -> List[str]
```

**参数**:
- `memories`: 内存记录字典列表，每个字典必须包含:
  - `content` (str): 内容文本
  - `project` (str): 项目标识
  - `repo` (str): 仓库名称
  - `agent` (str): 代理标识
  - `tags` (List[str]): 标签列表
  - `source` (str, 可选): 来源，默认"agent"

**返回值**:
- `List[str]`: 创建的记录UUID列表

**异常**:
- `ValueError`: 输入数据验证失败
- `Exception`: Weaviate写入失败

**示例**:
```python
memories = [
    {
        "content": "实现了新功能",
        "project": "my-project",
        "repo": "main",
        "agent": "developer", 
        "tags": ["feature", "implementation"],
        "source": "development"
    },
    {
        "content": "修复了bug",
        "project": "my-project",
        "repo": "main",
        "agent": "developer",
        "tags": ["bugfix"]
        # source 将默认为 "agent"
    }
]

uuids = write_memories_batch(memories)
```

### EmbeddingRouter.get_embeddings_batch()

低级别的批量嵌入接口，提供更多控制选项。

**签名**:
```python
def get_embeddings_batch(
    self,
    texts: List[str],
    use_cache: bool = True,
    metadata: Optional[List[Dict]] = None
) -> List[List[float]]
```

**参数**:
- `texts`: 文本列表
- `use_cache`: 是否使用缓存，默认True
- `metadata`: 元数据列表

**示例**:
```python
from vector.embedding_router import EmbeddingRouter

router = EmbeddingRouter()

# 禁用缓存的批量处理
vectors = router.get_embeddings_batch(
    texts=["文本1", "文本2"], 
    use_cache=False
)

# 带元数据和缓存
metadata = [{"source": "doc1"}, {"source": "doc2"}]
vectors = router.get_embeddings_batch(
    texts=["文本1", "文本2"],
    use_cache=True,
    metadata=metadata
)
```

---

## 📊 性能优化

### 批次大小选择

| 内容类型 | 推荐批次大小 | 说明 |
|---------|-------------|------|
| 短文本 (< 100字符) | 40-60 | 社交媒体、聊天记录 |
| 中等文本 (100-500字符) | 30-50 | 新闻标题、产品描述 |
| 长文本 (500-2000字符) | 20-40 | 文章段落、文档章节 |
| 超长文本 (> 2000字符) | 10-25 | 完整文档、报告 |

### 缓存优化策略

```python
# 策略1: 预热缓存
def warmup_cache(common_texts):
    """预热常用文本的缓存"""
    router = EmbeddingRouter()
    
    # 批量生成常用文本的embedding
    router.get_embeddings_batch(common_texts)
    
    print(f"✅ 缓存预热完成，预热了 {len(common_texts)} 个常用文本")

# 策略2: 缓存分析
def analyze_cache_performance():
    """分析缓存性能"""
    router = EmbeddingRouter()
    cache_info = router.get_cache_info()
    
    print(f"📊 缓存统计:")
    print(f"   缓存条目数: {cache_info['num_entries']}")
    print(f"   缓存大小: {cache_info['total_size_bytes'] / 1024 / 1024:.2f} MB")
    
    # 计算缓存命中率（需要在应用层实现）
    return cache_info
```

### 内存管理

```python
import gc
from typing import Iterator

def process_large_dataset_in_chunks(
    dataset: List[str], 
    chunk_size: int = 50
) -> Iterator[List[str]]:
    """大数据集分块处理，优化内存使用"""
    
    for i in range(0, len(dataset), chunk_size):
        chunk = dataset[i:i + chunk_size]
        
        # 处理当前块
        try:
            uuids = write_memories_batch(prepare_memories(chunk))
            yield uuids
            
        except Exception as e:
            print(f"❌ 块 {i//chunk_size + 1} 处理失败: {e}")
            continue
        
        # 手动触发垃圾回收，释放内存
        if i % (chunk_size * 10) == 0:
            gc.collect()

# 使用示例
total_processed = 0
for batch_uuids in process_large_dataset_in_chunks(large_dataset):
    total_processed += len(batch_uuids)
    print(f"📈 已处理 {total_processed} 条记录")
```

---

## 💡 最佳实践

### 1. 错误处理和重试机制

```python
import time
import random
from typing import Optional

class BatchProcessor:
    """带重试机制的批量处理器"""
    
    def __init__(self, max_retries: int = 3, base_delay: float = 1.0):
        self.max_retries = max_retries
        self.base_delay = base_delay
    
    def process_with_retry(self, memories: List[Dict]) -> Optional[List[str]]:
        """带指数退避的重试机制"""
        
        for attempt in range(self.max_retries + 1):
            try:
                return write_memories_batch(memories)
                
            except Exception as e:
                if attempt == self.max_retries:
                    print(f"❌ 最终失败，已重试 {self.max_retries} 次: {e}")
                    return None
                
                # 指数退避 + 随机抖动
                delay = self.base_delay * (2 ** attempt) + random.uniform(0, 1)
                print(f"⚠️ 第 {attempt + 1} 次尝试失败，{delay:.1f}秒后重试: {e}")
                time.sleep(delay)
        
        return None
```

### 2. 进度跟踪和监控

```python
from tqdm import tqdm
import time

class ProgressTracker:
    """批量处理进度跟踪器"""
    
    def __init__(self, total_items: int, batch_size: int):
        self.total_items = total_items
        self.batch_size = batch_size
        self.processed_items = 0
        self.start_time = time.time()
        
        # 创建进度条
        self.pbar = tqdm(
            total=total_items,
            desc="批量处理",
            unit="items",
            bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}]"
        )
    
    def update_progress(self, batch_size: int):
        """更新进度"""
        self.processed_items += batch_size
        self.pbar.update(batch_size)
        
        # 计算ETA和速度
        elapsed = time.time() - self.start_time
        if elapsed > 0:
            rate = self.processed_items / elapsed
            remaining = (self.total_items - self.processed_items) / rate if rate > 0 else 0
            
            self.pbar.set_postfix({
                '速度': f'{rate:.1f} items/s',
                '预计剩余': f'{remaining:.0f}s'
            })
    
    def close(self):
        """关闭进度条"""
        self.pbar.close()
        
        total_time = time.time() - self.start_time
        avg_rate = self.processed_items / total_time if total_time > 0 else 0
        
        print(f"🎉 处理完成!")
        print(f"   总计: {self.processed_items} 项")
        print(f"   耗时: {total_time:.1f} 秒")
        print(f"   平均速度: {avg_rate:.1f} items/s")

# 使用示例
def process_with_progress(all_memories: List[Dict], batch_size: int = 50):
    """带进度跟踪的批量处理"""
    
    tracker = ProgressTracker(len(all_memories), batch_size)
    processor = BatchProcessor()
    
    try:
        for i in range(0, len(all_memories), batch_size):
            batch = all_memories[i:i + batch_size]
            
            # 处理当前批次
            result = processor.process_with_retry(batch)
            
            if result:
                tracker.update_progress(len(batch))
            else:
                print(f"⚠️ 跳过失败的批次 {i//batch_size + 1}")
    
    finally:
        tracker.close()
```

### 3. 配置管理

```python
from dataclasses import dataclass
from typing import Dict, Any
import json

@dataclass
class BatchConfig:
    """批量处理配置"""
    
    # 批次大小配置
    default_batch_size: int = 50
    text_type_batch_sizes: Dict[str, int] = None
    
    # 重试配置
    max_retries: int = 3
    base_retry_delay: float = 1.0
    
    # 缓存配置
    enable_cache: bool = True
    cache_dir: str = ".cache/embeddings"
    
    # 性能配置
    enable_progress_bar: bool = True
    gc_frequency: int = 10  # 每处理多少个批次触发垃圾回收
    
    # 错误处理
    continue_on_error: bool = True
    log_errors: bool = True
    
    def __post_init__(self):
        if self.text_type_batch_sizes is None:
            self.text_type_batch_sizes = {
                'short': 60,     # < 100 字符
                'medium': 40,    # 100-500 字符  
                'long': 25,      # 500-2000 字符
                'very_long': 15  # > 2000 字符
            }
    
    @classmethod
    def from_file(cls, config_path: str) -> 'BatchConfig':
        """从配置文件加载"""
        with open(config_path, 'r', encoding='utf-8') as f:
            config_data = json.load(f)
        return cls(**config_data)
    
    def get_batch_size_for_text(self, text: str) -> int:
        """根据文本长度获取最适合的批次大小"""
        text_len = len(text)
        
        if text_len < 100:
            return self.text_type_batch_sizes['short']
        elif text_len < 500:
            return self.text_type_batch_sizes['medium']
        elif text_len < 2000:
            return self.text_type_batch_sizes['long']
        else:
            return self.text_type_batch_sizes['very_long']
```

### 4. 监控和度量

```python
import time
from collections import defaultdict
from typing import Dict, List

class BatchMetrics:
    """批量处理度量收集器"""
    
    def __init__(self):
        self.reset()
    
    def reset(self):
        """重置所有度量"""
        self.start_time = time.time()
        self.batch_count = 0
        self.total_items = 0
        self.successful_items = 0
        self.failed_items = 0
        self.cache_hits = 0
        self.cache_misses = 0
        self.processing_times = []
        self.error_counts = defaultdict(int)
    
    def record_batch(
        self, 
        batch_size: int, 
        processing_time: float, 
        success: bool,
        cache_hit_count: int = 0
    ):
        """记录批次处理结果"""
        self.batch_count += 1
        self.total_items += batch_size
        self.processing_times.append(processing_time)
        
        if success:
            self.successful_items += batch_size
        else:
            self.failed_items += batch_size
        
        self.cache_hits += cache_hit_count
        self.cache_misses += (batch_size - cache_hit_count)
    
    def record_error(self, error_type: str):
        """记录错误类型"""
        self.error_counts[error_type] += 1
    
    def get_summary(self) -> Dict[str, Any]:
        """获取度量摘要"""
        total_time = time.time() - self.start_time
        avg_processing_time = sum(self.processing_times) / len(self.processing_times) if self.processing_times else 0
        
        return {
            '总处理时间': f'{total_time:.2f}s',
            '平均批次处理时间': f'{avg_processing_time:.2f}s',
            '总批次数': self.batch_count,
            '总项目数': self.total_items,
            '成功项目数': self.successful_items,
            '失败项目数': self.failed_items,
            '成功率': f'{(self.successful_items / self.total_items * 100):.1f}%' if self.total_items > 0 else '0%',
            '缓存命中数': self.cache_hits,
            '缓存未命中数': self.cache_misses,
            '缓存命中率': f'{(self.cache_hits / (self.cache_hits + self.cache_misses) * 100):.1f}%' if (self.cache_hits + self.cache_misses) > 0 else '0%',
            '处理速度': f'{self.total_items / total_time:.1f} items/s' if total_time > 0 else '0 items/s',
            '错误统计': dict(self.error_counts)
        }
    
    def print_summary(self):
        """打印度量摘要"""
        summary = self.get_summary()
        
        print("\n📊 批量处理度量报告")
        print("=" * 50)
        
        for key, value in summary.items():
            if key == '错误统计':
                print(f"{key}:")
                for error_type, count in value.items():
                    print(f"  - {error_type}: {count}")
            else:
                print(f"{key}: {value}")
```

---

## 🚨 故障排除

### 常见问题

#### 1. OpenAI API 限制

**问题**: 批量请求触发API速率限制

**解决方案**:
```python
import time
from openai import RateLimitError

def handle_rate_limit(func, *args, **kwargs):
    """处理API速率限制"""
    max_retries = 5
    base_delay = 60  # OpenAI推荐等待60秒
    
    for attempt in range(max_retries):
        try:
            return func(*args, **kwargs)
        except RateLimitError as e:
            if attempt == max_retries - 1:
                raise e
            
            wait_time = base_delay * (2 ** attempt)
            print(f"⚠️ API速率限制，等待 {wait_time} 秒后重试...")
            time.sleep(wait_time)
```

#### 2. 内存不足

**问题**: 处理大批次时内存溢出

**解决方案**:
```python
def adaptive_batch_processing(texts: List[str], max_memory_mb: int = 500):
    """自适应批次大小处理"""
    import psutil
    import sys
    
    # 监控内存使用
    process = psutil.Process()
    
    adaptive_batch_size = 50
    min_batch_size = 10
    max_batch_size = 100
    
    for i in range(0, len(texts), adaptive_batch_size):
        # 检查内存使用
        memory_mb = process.memory_info().rss / 1024 / 1024
        
        if memory_mb > max_memory_mb:
            # 减少批次大小
            adaptive_batch_size = max(min_batch_size, adaptive_batch_size // 2)
            print(f"⚠️ 内存使用过高 ({memory_mb:.1f}MB)，减少批次大小到 {adaptive_batch_size}")
        elif memory_mb < max_memory_mb * 0.5:
            # 增加批次大小
            adaptive_batch_size = min(max_batch_size, adaptive_batch_size + 10)
        
        # 处理当前批次
        batch = texts[i:i + adaptive_batch_size]
        try:
            result = embed_texts_batch(batch)
            yield result
        except MemoryError:
            # 强制减少批次大小
            adaptive_batch_size = max(min_batch_size, adaptive_batch_size // 2)
            print(f"❌ 内存错误，强制减少批次大小到 {adaptive_batch_size}")
```

#### 3. 缓存问题

**问题**: 缓存损坏或性能下降

**解决方案**:
```python
def diagnose_cache_health():
    """诊断缓存健康状态"""
    from vector.embedding_router import EmbeddingRouter
    import json
    
    router = EmbeddingRouter()
    cache_dir = router.cache_dir
    
    print(f"🔍 检查缓存目录: {cache_dir}")
    
    # 检查缓存文件
    cache_files = list(cache_dir.glob("*.json"))
    corrupted_files = []
    
    for cache_file in cache_files:
        try:
            with cache_file.open('r') as f:
                json.load(f)
        except json.JSONDecodeError:
            corrupted_files.append(cache_file)
    
    if corrupted_files:
        print(f"⚠️ 发现 {len(corrupted_files)} 个损坏的缓存文件")
        
        # 清理损坏的文件
        for file in corrupted_files:
            file.unlink()
            print(f"🗑️ 已删除损坏文件: {file.name}")
    
    print(f"✅ 缓存健康检查完成，有效文件数: {len(cache_files) - len(corrupted_files)}")
```

### 性能调优检查清单

- [ ] **批次大小优化**: 根据文本长度调整批次大小
- [ ] **缓存预热**: 对常用文本进行缓存预热
- [ ] **内存监控**: 实施内存使用监控和自适应调整
- [ ] **错误重试**: 实现指数退避重试机制
- [ ] **进度跟踪**: 添加详细的进度和性能度量
- [ ] **并发限制**: 避免过多并发请求导致API限制
- [ ] **资源清理**: 定期清理过期缓存和临时文件

---

## 📚 参考资源

### 官方文档
- [OpenAI Embeddings API](https://platform.openai.com/docs/guides/embeddings)
- [Weaviate官方文档](https://weaviate.io/developers/weaviate)

### 相关最佳实践
- [大规模向量处理最佳实践](docs/vector-processing-best-practices.md)
- [缓存策略指南](docs/caching-strategies.md)
- [性能优化手册](docs/performance-optimization.md)

### 示例代码
- [批量处理演示](../examples/batch_processing_demo.py)
- [性能测试套件](../tests/test_batch_performance.py)

---

**📞 获取帮助**

如果遇到问题或需要技术支持，请：
1. 查看[故障排除](#故障排除)部分
2. 检查[GitHub Issues](https://github.com/your-repo/issues)
3. 联系技术团队

---

*文档版本: 1.0 | 最后更新: 2024-12-19* 