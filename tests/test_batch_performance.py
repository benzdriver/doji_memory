"""
Performance tests for batch processing functionality.
This module tests that batch operations provide significant performance improvements.
"""
import time
import pytest
from pathlib import Path
import shutil
from unittest.mock import patch, Mock

from vector.embedding_router import EmbeddingRouter
from vector.embedding import embed_text, embed_texts_batch
from vector.memory_writer import write_memory, write_memories_batch


class TestBatchPerformance:
    """Test performance improvements of batch processing."""

    @pytest.fixture
    def isolated_router(self):
        """Create an isolated router for performance testing."""
        cache_dir = ".test_cache_performance"
        router = EmbeddingRouter(cache_dir=cache_dir)
        # Clear any existing cache
        router.clear_cache()
        yield router
        # Cleanup
        if Path(cache_dir).exists():
            shutil.rmtree(cache_dir)

    def test_embedding_batch_performance(self, isolated_router):
        """Test that batch embedding is significantly faster than individual calls."""
        # Test data - using unique texts to avoid cache hits
        texts = [f"Performance test text number {i} for embedding" for i in range(10)]
        
        # Test individual embedding calls
        start_time = time.time()
        individual_vectors = []
        for text in texts:
            vector = isolated_router.get_embedding(text, use_cache=False)
            individual_vectors.append(vector)
        individual_time = time.time() - start_time
        
        # Clear cache and test batch embedding
        isolated_router.clear_cache()
        start_time = time.time()
        batch_vectors = isolated_router.get_embeddings_batch(texts, use_cache=False)
        batch_time = time.time() - start_time
        
        # Verify results are equivalent
        assert len(individual_vectors) == len(batch_vectors)
        for i, (individual, batch) in enumerate(zip(individual_vectors, batch_vectors)):
            assert len(individual) == len(batch) == 1536
            # Vectors should be identical since we're using the same texts
            assert individual == batch, f"Vectors differ at index {i}"
        
        # Performance requirement: batch should be at least 60% faster
        performance_improvement = (individual_time - batch_time) / individual_time
        print(f"\nPerformance Results:")
        print(f"Individual calls time: {individual_time:.3f}s")
        print(f"Batch call time: {batch_time:.3f}s")
        print(f"Performance improvement: {performance_improvement:.1%}")
        
        assert performance_improvement >= 0.60, \
            f"Batch processing should be at least 60% faster, got {performance_improvement:.1%}"

    def test_embedding_batch_with_cache_performance(self, isolated_router):
        """Test batch performance with partial cache hits."""
        # Test data
        texts = [f"Cache test text {i}" for i in range(5)]
        
        # Pre-cache first 3 texts
        for text in texts[:3]:
            isolated_router.get_embedding(text)
        
        # Test batch with partial cache
        start_time = time.time()
        vectors = isolated_router.get_embeddings_batch(texts)
        batch_time = time.time() - start_time
        
        # Should be very fast due to cache hits
        assert batch_time < 2.0, f"Batch with cache should be fast, took {batch_time:.3f}s"
        assert len(vectors) == 5
        assert all(len(v) == 1536 for v in vectors)

    def test_memory_batch_write_performance(self):
        """Test that batch memory writing is more efficient."""
        # Test data
        memories = [
            {
                "content": f"Performance test memory {i}",
                "project": "test-project",
                "repo": "test-repo",
                "agent": "test-agent",
                "tags": [f"tag{i}"]
            }
            for i in range(5)
        ]
        
        with patch('vector.memory_writer.get_weaviate_client') as mock_client, \
             patch('vector.memory_writer.embed_text') as mock_embed, \
             patch('vector.memory_writer.embed_texts_batch') as mock_embed_batch:
            
            # Setup mocks
            mock_client_instance = Mock()
            mock_client.return_value = mock_client_instance
            
            # Mock individual embedding calls
            mock_embed.return_value = [0.1, 0.2, 0.3]
            
            # Mock batch embedding calls
            mock_embed_batch.return_value = [[0.1, 0.2, 0.3]] * 5
            
            # Mock Weaviate responses
            mock_result = Mock()
            mock_result.uuid = "test-uuid"
            mock_client_instance.data_object.create.return_value = mock_result
            
            # Test individual writes
            start_time = time.time()
            individual_uuids = []
            for memory in memories:
                uuid = write_memory(
                    content=memory["content"],
                    project=memory["project"],
                    repo=memory["repo"],
                    agent=memory["agent"],
                    tags=memory["tags"]
                )
                individual_uuids.append(uuid)
            individual_time = time.time() - start_time
            
            # Reset mocks
            mock_embed.reset_mock()
            mock_embed_batch.reset_mock()
            mock_client_instance.data_object.create.reset_mock()
            
            # Test batch write
            start_time = time.time()
            batch_uuids = write_memories_batch(memories)
            batch_time = time.time() - start_time
            
            # Verify API call efficiency
            # Individual should make 5 embed_text calls
            assert mock_embed.call_count == 5
            # Batch should make 1 embed_texts_batch call
            assert mock_embed_batch.call_count == 1
            
            # Both should make same number of Weaviate calls
            assert len(individual_uuids) == len(batch_uuids) == 5
            
            print(f"\nMemory Write Performance:")
            print(f"Individual writes time: {individual_time:.3f}s")
            print(f"Batch write time: {batch_time:.3f}s")
            print(f"Embedding API calls - Individual: {mock_embed.call_count}, Batch: {mock_embed_batch.call_count}")

    def test_embed_texts_batch_api_efficiency(self):
        """Test that the public API is efficient."""
        texts = [f"API efficiency test {i}" for i in range(3)]
        
        with patch('vector.embedding._router') as mock_router:
            mock_router.get_embeddings_batch.return_value = [[0.1, 0.2, 0.3]] * 3
            
            # Call batch function
            vectors = embed_texts_batch(texts)
            
            # Should call the router's batch method once
            mock_router.get_embeddings_batch.assert_called_once_with(texts, metadata=None)
            assert len(vectors) == 3

    def test_large_batch_handling(self, isolated_router):
        """Test performance with larger batches."""
        # Test with 20 texts
        texts = [f"Large batch test text {i} with more content to simulate real usage" for i in range(20)]
        
        start_time = time.time()
        vectors = isolated_router.get_embeddings_batch(texts, use_cache=False)
        batch_time = time.time() - start_time
        
        print(f"\nLarge Batch Performance:")
        print(f"20 texts batch time: {batch_time:.3f}s")
        print(f"Average per text: {batch_time/20:.3f}s")
        
        assert len(vectors) == 20
        assert all(len(v) == 1536 for v in vectors)
        # Should complete within reasonable time
        assert batch_time < 30.0, f"Large batch should complete in reasonable time, took {batch_time:.3f}s"

if __name__ == "__main__":
    # Run performance tests manually
    test_instance = TestBatchPerformance()
    
    # Create isolated router
    cache_dir = ".test_cache_manual"
    router = EmbeddingRouter(cache_dir=cache_dir)
    
    try:
        print("Running manual performance test...")
        test_instance.test_embedding_batch_performance(router)
        print("✅ Performance test passed!")
    finally:
        if Path(cache_dir).exists():
            shutil.rmtree(cache_dir) 