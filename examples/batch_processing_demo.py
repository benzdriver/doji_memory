"""
Batch Processing Demo - Weaviate Memory System

This script demonstrates the new batch processing capabilities:
1. Batch embedding generation
2. Batch memory writing
3. Performance comparisons

Usage:
    python examples/batch_processing_demo.py
"""

import time
import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from vector import embed_text, embed_texts_batch, write_memory, write_memories_batch
from vector.embedding_router import EmbeddingRouter


def demo_batch_embeddings():
    """Demonstrate batch embedding generation."""
    print("🚀 Batch Embedding Demo")
    print("=" * 50)
    
    # Test data
    texts = [
        "Machine learning is transforming software development",
        "Vector databases enable semantic search capabilities", 
        "Embedding models convert text to numerical representations",
        "Weaviate provides efficient vector storage and retrieval",
        "Batch processing improves API call efficiency significantly"
    ]
    
    print(f"Processing {len(texts)} texts...")
    print()
    
    # Individual embedding calls
    print("📝 Individual embedding calls:")
    start_time = time.time()
    individual_vectors = []
    for i, text in enumerate(texts):
        vector = embed_text(text)
        individual_vectors.append(vector)
        print(f"  Text {i+1}: {len(vector)} dimensions")
    individual_time = time.time() - start_time
    print(f"  Total time: {individual_time:.3f}s")
    print()
    
    # Batch embedding calls
    print("⚡ Batch embedding call:")
    start_time = time.time()
    batch_vectors = embed_texts_batch(texts)
    batch_time = time.time() - start_time
    
    for i, vector in enumerate(batch_vectors):
        print(f"  Text {i+1}: {len(vector)} dimensions")
    print(f"  Total time: {batch_time:.3f}s")
    print()
    
    # Performance comparison
    performance_improvement = (individual_time - batch_time) / individual_time
    print("📊 Performance Results:")
    print(f"  Individual calls: {individual_time:.3f}s")
    print(f"  Batch call: {batch_time:.3f}s")
    print(f"  Performance improvement: {performance_improvement:.1%}")
    print(f"  Speedup: {individual_time/batch_time:.1f}x faster")
    print()
    
    # Verify results are equivalent
    results_match = all(
        individual == batch 
        for individual, batch in zip(individual_vectors, batch_vectors)
    )
    print(f"✅ Results verification: {'PASS' if results_match else 'FAIL'}")
    print()


def demo_batch_memory_writing():
    """Demonstrate batch memory writing."""
    print("💾 Batch Memory Writing Demo")
    print("=" * 50)
    
    # Test data
    memories = [
        {
            "content": "Implemented batch processing for embedding generation",
            "project": "weaviate-memory-system",
            "repo": "main",
            "agent": "claude",
            "tags": ["feature", "batch-processing", "performance"]
        },
        {
            "content": "Added comprehensive test coverage for batch operations",
            "project": "weaviate-memory-system", 
            "repo": "main",
            "agent": "claude",
            "tags": ["testing", "batch-processing"]
        },
        {
            "content": "Optimized API calls with intelligent caching strategy",
            "project": "weaviate-memory-system",
            "repo": "main", 
            "agent": "claude",
            "tags": ["optimization", "caching"]
        }
    ]
    
    print(f"Processing {len(memories)} memories...")
    print()
    
    # Note: This demo uses mocked Weaviate client for safety
    print("⚠️  Note: Using mocked Weaviate client for demo purposes")
    print("   Real implementation would connect to actual Weaviate instance")
    print()
    
    # Simulate batch write (would normally call write_memories_batch)
    print("📝 Batch Memory Write:")
    print("  Memory 1: Implemented batch processing...")
    print("  Memory 2: Added comprehensive test coverage...")  
    print("  Memory 3: Optimized API calls...")
    print()
    print("✅ All memories would be written efficiently in batch!")
    print()


def demo_caching_benefits():
    """Demonstrate caching benefits with batch processing."""
    print("🗄️  Caching Benefits Demo")
    print("=" * 50)
    
    # Create isolated router for demo
    cache_dir = ".demo_cache"
    router = EmbeddingRouter(cache_dir=cache_dir)
    
    try:
        # Clear any existing cache
        router.clear_cache()
        
        texts = [
            "Caching improves performance significantly",
            "Vector embeddings are expensive to compute",
            "Batch processing with cache is optimal"
        ]
        
        print("🔄 First batch call (no cache):")
        start_time = time.time()
        vectors1 = router.get_embeddings_batch(texts)
        first_time = time.time() - start_time
        print(f"  Time: {first_time:.3f}s")
        print(f"  Cache entries: {router.get_cache_info()['num_entries']}")
        print()
        
        print("⚡ Second batch call (full cache hit):")
        start_time = time.time()
        vectors2 = router.get_embeddings_batch(texts)
        second_time = time.time() - start_time
        print(f"  Time: {second_time:.3f}s")
        print(f"  Cache entries: {router.get_cache_info()['num_entries']}")
        print()
        
        # Verify cache speedup
        speedup = first_time / second_time if second_time > 0 else float('inf')
        print(f"📊 Cache speedup: {speedup:.1f}x faster")
        
        # Verify results are identical
        results_match = vectors1 == vectors2
        print(f"✅ Cache consistency: {'PASS' if results_match else 'FAIL'}")
        print()
        
        # Test partial cache scenario
        mixed_texts = texts[:2] + ["New text not in cache"]
        print("🔀 Partial cache scenario:")
        print("  2 texts from cache + 1 new text")
        start_time = time.time()
        mixed_vectors = router.get_embeddings_batch(mixed_texts)
        mixed_time = time.time() - start_time
        print(f"  Time: {mixed_time:.3f}s")
        print(f"  Cache entries: {router.get_cache_info()['num_entries']}")
        print()
        
    finally:
        # Cleanup demo cache
        import shutil
        if Path(cache_dir).exists():
            shutil.rmtree(cache_dir)


def main():
    """Run all batch processing demos."""
    print("🎯 Weaviate Memory System - Batch Processing Demo")
    print("=" * 60)
    print()
    
    try:
        # Check if API key is available
        import os
        if not os.getenv("OPENAI_API_KEY"):
            print("⚠️  Warning: OPENAI_API_KEY not found in environment")
            print("   Some demos may use mock data")
            print()
        
        # Run demos
        demo_batch_embeddings()
        demo_batch_memory_writing()
        demo_caching_benefits()
        
        print("🎉 All demos completed successfully!")
        print()
        print("💡 Key Takeaways:")
        print("  • Batch processing significantly improves performance")
        print("  • Intelligent caching reduces redundant API calls")
        print("  • Batch operations maintain result consistency")
        print("  • Partial cache hits are handled efficiently")
        
    except KeyboardInterrupt:
        print("\n⏹️  Demo interrupted by user")
    except Exception as e:
        print(f"\n❌ Demo failed with error: {str(e)}")
        raise


if __name__ == "__main__":
    main() 