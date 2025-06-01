import os
import shutil
import pytest
from pathlib import Path
import json
from unittest.mock import Mock, patch

from vector.embedding_router import EmbeddingRouter

# Test data
TEST_TEXT = "这是一段用于测试的文本内容"
TEST_CACHE_DIR = ".test_cache/embeddings"

@pytest.fixture
def router():
    """Create a test router instance with a temporary cache directory."""
    router = EmbeddingRouter(cache_dir=TEST_CACHE_DIR)
    yield router
    # Cleanup after tests
    if Path(TEST_CACHE_DIR).exists():
        shutil.rmtree(TEST_CACHE_DIR)

def test_router_initialization(router):
    """Test router initialization and configuration."""
    assert router.model == "text-embedding-ada-002"
    assert router.cache_dir == Path(TEST_CACHE_DIR)
    assert router.client is not None

def test_embedding_dimensions(router):
    """Test if the embedding has the correct dimensions."""
    vector = router.get_embedding(TEST_TEXT)
    assert isinstance(vector, list)
    assert len(vector) == 1536  # OpenAI ada-002 model dimension
    assert all(isinstance(x, float) for x in vector)

def test_cache_creation(router):
    """Test if cache directory is created."""
    assert Path(TEST_CACHE_DIR).exists()
    assert Path(TEST_CACHE_DIR).is_dir()

def test_cache_functionality(router):
    """Test if caching works correctly."""
    # First call should create cache
    vector1 = router.get_embedding(TEST_TEXT)
    
    # Get cache info
    cache_info = router.get_cache_info()
    assert cache_info['num_entries'] == 1
    
    # Second call should use cache
    vector2 = router.get_embedding(TEST_TEXT)
    assert vector1 == vector2  # Should get exact same vector from cache

def test_cache_metadata(router):
    """Test if metadata is stored correctly in cache."""
    metadata = {"source": "test", "timestamp": "2024-03-20"}
    vector = router.get_embedding(TEST_TEXT, metadata=metadata)
    
    # Check if metadata is stored
    cache_key = router._get_cache_key(TEST_TEXT)
    cache_path = router._get_cache_path(cache_key)
    
    with cache_path.open('r') as f:
        cache_data = json.load(f)
    assert cache_data['metadata'] == metadata

def test_cache_disable(router):
    """Test if cache can be disabled."""
    # First call with cache
    vector1 = router.get_embedding(TEST_TEXT)
    
    # Second call without cache
    vector2 = router.get_embedding(TEST_TEXT, use_cache=False)
    
    # Vectors should be nearly identical (small floating point differences possible)
    assert len(vector1) == len(vector2)
    # Check if vectors are close enough (allowing for minor API variations)
    assert all(abs(a - b) < 1e-6 for a, b in zip(vector1, vector2))

def test_clear_cache(router):
    """Test cache clearing functionality."""
    # Create some cached embeddings
    router.get_embedding(TEST_TEXT)
    router.get_embedding(TEST_TEXT + "2")
    
    # Verify cache exists
    assert router.get_cache_info()['num_entries'] == 2
    
    # Clear cache
    router.clear_cache()
    
    # Verify cache is empty
    assert router.get_cache_info()['num_entries'] == 0

def test_invalid_input(router):
    """Test handling of invalid inputs."""
    with pytest.raises(ValueError):
        router.get_embedding("")
    
    with pytest.raises(ValueError):
        router.get_embedding(None)
    
    with pytest.raises(ValueError):
        router.get_embedding(123)

def test_api_key_validation(monkeypatch):
    """Test API key validation."""
    # Remove API key from environment and prevent load_dotenv from loading it
    monkeypatch.delenv('OPENAI_API_KEY', raising=False)
    
    # Temporarily rename .env file to prevent load_dotenv from working
    env_file = Path('.env')
    temp_env_file = Path('.env.temp')
    
    if env_file.exists():
        env_file.rename(temp_env_file)
    
    try:
        # Should raise error when no API key is present
        with pytest.raises(ValueError, match="OPENAI_API_KEY not found"):
            EmbeddingRouter()
    finally:
        # Restore .env file
        if temp_env_file.exists():
            temp_env_file.rename(env_file)

def test_openai_client_initialization_error(monkeypatch):
    """Test handling of OpenAI client initialization errors."""
    # Remove API key from environment and prevent load_dotenv from loading it
    monkeypatch.delenv('OPENAI_API_KEY', raising=False)
    
    # Temporarily rename .env file to prevent load_dotenv from working
    env_file = Path('.env')
    temp_env_file = Path('.env.temp')
    
    if env_file.exists():
        env_file.rename(temp_env_file)
    
    # Set a fake API key to bypass the first check
    monkeypatch.setenv('OPENAI_API_KEY', 'fake-key')
    
    try:
        with patch('vector.embedding_router.OpenAI') as mock_openai:
            # Make OpenAI initialization raise an exception
            mock_openai.side_effect = Exception("OpenAI initialization failed")
            
            with pytest.raises(ValueError, match="Failed to initialize OpenAI client"):
                EmbeddingRouter()
    finally:
        # Restore .env file
        if temp_env_file.exists():
            temp_env_file.rename(env_file)

def test_cache_file_corruption(router):
    """Test handling of corrupted cache files."""
    # Create a corrupted cache file
    cache_key = router._get_cache_key(TEST_TEXT)
    cache_path = router._get_cache_path(cache_key)
    
    # Write invalid JSON
    with cache_path.open('w') as f:
        f.write("invalid json content")
    
    # Should handle corruption gracefully and not return cached data
    cached = router._load_from_cache(cache_key)
    assert cached is None

def test_cache_file_missing_key(router):
    """Test handling of cache files missing embedding key."""
    # Create a cache file without embedding key
    cache_key = router._get_cache_key(TEST_TEXT)
    cache_path = router._get_cache_path(cache_key)
    
    # Write JSON without embedding key
    with cache_path.open('w') as f:
        json.dump({"metadata": {"test": "data"}}, f)
    
    # Should handle missing key gracefully and not return cached data
    cached = router._load_from_cache(cache_key)
    assert cached is None

def test_openai_error_handling(router):
    """Test handling of OpenAI API errors."""
    with patch.object(router.client.embeddings, 'create') as mock_create:
        from openai import OpenAIError
        mock_create.side_effect = OpenAIError("API Error")
        
        with pytest.raises(OpenAIError, match="Failed to generate embedding"):
            router.get_embedding(TEST_TEXT)

# Batch processing tests
def test_get_embeddings_batch_basic(router):
    """Test basic batch embedding functionality."""
    texts = [TEST_TEXT, TEST_TEXT + "2", TEST_TEXT + "3"]
    vectors = router.get_embeddings_batch(texts)
    
    assert isinstance(vectors, list)
    assert len(vectors) == len(texts)
    for vector in vectors:
        assert isinstance(vector, list)
        assert len(vector) == 1536
        assert all(isinstance(x, float) for x in vector)

def test_get_embeddings_batch_with_cache(router):
    """Test batch embedding with caching."""
    texts = [TEST_TEXT, TEST_TEXT + "2"]
    
    # First call should create cache
    vectors1 = router.get_embeddings_batch(texts)
    
    # Verify cache
    cache_info = router.get_cache_info()
    assert cache_info['num_entries'] == 2
    
    # Second call should use cache
    vectors2 = router.get_embeddings_batch(texts)
    assert vectors1 == vectors2

def test_get_embeddings_batch_partial_cache(router):
    """Test batch embedding with partial cache hits."""
    # Cache one text first
    text1 = TEST_TEXT
    router.get_embedding(text1)
    
    # Now batch with one cached and one new text
    texts = [text1, TEST_TEXT + "new"]
    vectors = router.get_embeddings_batch(texts)
    
    assert len(vectors) == 2
    assert all(len(v) == 1536 for v in vectors)

def test_get_embeddings_batch_with_metadata(router):
    """Test batch embedding with metadata."""
    texts = [TEST_TEXT, TEST_TEXT + "2"]
    metadata = [{"source": "test1"}, {"source": "test2"}]
    
    vectors = router.get_embeddings_batch(texts, metadata=metadata)
    assert len(vectors) == 2
    
    # Check that metadata is cached
    for i, text in enumerate(texts):
        cache_key = router._get_cache_key(text)
        cache_path = router._get_cache_path(cache_key)
        with cache_path.open('r') as f:
            cache_data = json.load(f)
        assert cache_data['metadata'] == metadata[i]

def test_get_embeddings_batch_without_cache(router):
    """Test batch embedding without cache."""
    texts = [TEST_TEXT, TEST_TEXT + "2"]
    vectors = router.get_embeddings_batch(texts, use_cache=False)
    
    assert len(vectors) == 2
    # Should not create cache entries
    assert router.get_cache_info()['num_entries'] == 0

def test_get_embeddings_batch_invalid_input(router):
    """Test batch embedding with invalid inputs."""
    # Empty list
    with pytest.raises(ValueError, match="Texts must be a non-empty list"):
        router.get_embeddings_batch([])
    
    # Not a list
    with pytest.raises(ValueError, match="Texts must be a non-empty list"):
        router.get_embeddings_batch("not a list")
    
    # List with invalid items
    with pytest.raises(ValueError, match="All texts must be non-empty strings"):
        router.get_embeddings_batch([TEST_TEXT, "", TEST_TEXT + "2"])
    
    with pytest.raises(ValueError, match="All texts must be non-empty strings"):
        router.get_embeddings_batch([TEST_TEXT, 123, TEST_TEXT + "2"])

def test_get_embeddings_batch_metadata_length_mismatch(router):
    """Test batch embedding with mismatched metadata length."""
    texts = [TEST_TEXT, TEST_TEXT + "2"]
    metadata = [{"source": "test1"}]  # Wrong length
    
    with pytest.raises(ValueError, match="Metadata list must have the same length as texts list"):
        router.get_embeddings_batch(texts, metadata=metadata)

def test_get_embeddings_batch_openai_error(router):
    """Test batch embedding with OpenAI API error."""
    with patch.object(router.client.embeddings, 'create') as mock_create:
        from openai import OpenAIError
        mock_create.side_effect = OpenAIError("API Error")
        
        with pytest.raises(OpenAIError, match="Failed to generate batch embeddings"):
            router.get_embeddings_batch([TEST_TEXT, TEST_TEXT + "2"])

def test_batch_cache_methods(router):
    """Test batch cache helper methods."""
    texts = [TEST_TEXT, TEST_TEXT + "2"]
    
    # Test _load_batch_from_cache with no cache
    results = router._load_batch_from_cache(texts)
    assert all(v is None for v in results.values())
    
    # Cache one text
    router.get_embedding(texts[0])
    
    # Test partial cache
    results = router._load_batch_from_cache(texts)
    assert results[texts[0]] is not None
    assert results[texts[1]] is None 