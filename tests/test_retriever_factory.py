import pytest
from unittest.mock import Mock, patch
from vector.retriever_factory import get_similar_memories


def test_get_similar_memories_success():
    """Test successful memory retrieval."""
    with patch('vector.retriever_factory.get_weaviate_client') as mock_client, \
         patch('vector.retriever_factory.embed_text') as mock_embed:
        
        # Setup mocks
        mock_client_instance = Mock()
        mock_client.return_value = mock_client_instance
        mock_embed.return_value = [0.1, 0.2, 0.3]
        
        # Mock query builder chain
        mock_query = Mock()
        mock_get = Mock()
        mock_with_near_vector = Mock()
        mock_with_where = Mock()
        mock_with_limit = Mock()
        
        mock_client_instance.query = mock_query
        mock_query.get.return_value = mock_get
        mock_get.with_near_vector.return_value = mock_with_near_vector
        mock_with_near_vector.with_where.return_value = mock_with_where
        mock_with_where.with_limit.return_value = mock_with_limit
        
        # Mock the final result
        mock_result = {
            "data": {
                "Get": {
                    "ProjectMemory": [
                        {
                            "content": "Test memory 1",
                            "project": "test-project",
                            "repo": "test-repo",
                            "agent": "test-agent",
                            "tags": ["tag1"],
                            "source": "agent",
                            "timestamp": "2024-01-01T12:00:00"
                        },
                        {
                            "content": "Test memory 2",
                            "project": "test-project",
                            "repo": "test-repo",
                            "agent": "test-agent",
                            "tags": ["tag2"],
                            "source": "agent",
                            "timestamp": "2024-01-01T13:00:00"
                        }
                    ]
                }
            }
        }
        mock_with_limit.do.return_value = mock_result
        
        # Call the function
        result = get_similar_memories("test query")
        
        # Verify the result
        assert len(result) == 2
        assert result[0]["content"] == "Test memory 1"
        assert result[1]["content"] == "Test memory 2"
        
        # Verify the calls
        mock_embed.assert_called_once_with("test query")
        mock_query.get.assert_called_once_with("ProjectMemory", [
            "content", "project", "repo", "agent", "tags", "source", "timestamp"
        ])


def test_get_similar_memories_with_project_filter():
    """Test memory retrieval with project filter."""
    with patch('vector.retriever_factory.get_weaviate_client') as mock_client, \
         patch('vector.retriever_factory.embed_text') as mock_embed:
        
        # Setup mocks
        mock_client_instance = Mock()
        mock_client.return_value = mock_client_instance
        mock_embed.return_value = [0.1, 0.2, 0.3]
        
        # Mock query builder chain
        mock_query = Mock()
        mock_get = Mock()
        mock_with_near_vector = Mock()
        mock_with_where = Mock()
        mock_with_limit = Mock()
        
        mock_client_instance.query = mock_query
        mock_query.get.return_value = mock_get
        mock_get.with_near_vector.return_value = mock_with_near_vector
        mock_with_near_vector.with_where.return_value = mock_with_where
        mock_with_where.with_limit.return_value = mock_with_limit
        
        mock_result = {
            "data": {
                "Get": {
                    "ProjectMemory": []
                }
            }
        }
        mock_with_limit.do.return_value = mock_result
        
        # Call with project filter
        result = get_similar_memories("test query", project="specific-project", limit=3)
        
        # Check that with_where was called with the correct filter
        expected_filter = {
            "path": ["project"],
            "operator": "Equal",
            "valueString": "specific-project"
        }
        mock_with_near_vector.with_where.assert_called_once_with(expected_filter)
        mock_with_where.with_limit.assert_called_once_with(3)


def test_get_similar_memories_without_project_filter():
    """Test memory retrieval without project filter."""
    with patch('vector.retriever_factory.get_weaviate_client') as mock_client, \
         patch('vector.retriever_factory.embed_text') as mock_embed:
        
        # Setup mocks
        mock_client_instance = Mock()
        mock_client.return_value = mock_client_instance
        mock_embed.return_value = [0.1, 0.2, 0.3]
        
        # Mock query builder chain
        mock_query = Mock()
        mock_get = Mock()
        mock_with_near_vector = Mock()
        mock_with_where = Mock()
        mock_with_limit = Mock()
        
        mock_client_instance.query = mock_query
        mock_query.get.return_value = mock_get
        mock_get.with_near_vector.return_value = mock_with_near_vector
        mock_with_near_vector.with_where.return_value = mock_with_where
        mock_with_where.with_limit.return_value = mock_with_limit
        
        mock_result = {
            "data": {
                "Get": {
                    "ProjectMemory": []
                }
            }
        }
        mock_with_limit.do.return_value = mock_result
        
        # Call without project filter
        result = get_similar_memories("test query")
        
        # Check that with_where was called with None
        mock_with_near_vector.with_where.assert_called_once_with(None)
        mock_with_where.with_limit.assert_called_once_with(5)  # default limit


def test_get_similar_memories_empty_result():
    """Test handling of empty search results."""
    with patch('vector.retriever_factory.get_weaviate_client') as mock_client, \
         patch('vector.retriever_factory.embed_text') as mock_embed:
        
        # Setup mocks
        mock_client_instance = Mock()
        mock_client.return_value = mock_client_instance
        mock_embed.return_value = [0.1, 0.2, 0.3]
        
        # Mock query builder chain
        mock_query = Mock()
        mock_get = Mock()
        mock_with_near_vector = Mock()
        mock_with_where = Mock()
        mock_with_limit = Mock()
        
        mock_client_instance.query = mock_query
        mock_query.get.return_value = mock_get
        mock_get.with_near_vector.return_value = mock_with_near_vector
        mock_with_near_vector.with_where.return_value = mock_with_where
        mock_with_where.with_limit.return_value = mock_with_limit
        
        # Mock empty result
        mock_result = {}
        mock_with_limit.do.return_value = mock_result
        
        # Call the function
        result = get_similar_memories("test query")
        
        # Should return empty list
        assert result == []


def test_get_similar_memories_malformed_result():
    """Test handling of malformed search results."""
    with patch('vector.retriever_factory.get_weaviate_client') as mock_client, \
         patch('vector.retriever_factory.embed_text') as mock_embed:
        
        # Setup mocks
        mock_client_instance = Mock()
        mock_client.return_value = mock_client_instance
        mock_embed.return_value = [0.1, 0.2, 0.3]
        
        # Mock query builder chain
        mock_query = Mock()
        mock_get = Mock()
        mock_with_near_vector = Mock()
        mock_with_where = Mock()
        mock_with_limit = Mock()
        
        mock_client_instance.query = mock_query
        mock_query.get.return_value = mock_get
        mock_get.with_near_vector.return_value = mock_with_near_vector
        mock_with_near_vector.with_where.return_value = mock_with_where
        mock_with_where.with_limit.return_value = mock_with_limit
        
        # Mock malformed result (missing expected structure)
        mock_result = {
            "data": {
                "Get": {}
            }
        }
        mock_with_limit.do.return_value = mock_result
        
        # Call the function
        result = get_similar_memories("test query")
        
        # Should handle gracefully and return empty list
        assert result == []


def test_get_similar_memories_vector_parameters():
    """Test that the correct vector parameters are passed."""
    with patch('vector.retriever_factory.get_weaviate_client') as mock_client, \
         patch('vector.retriever_factory.embed_text') as mock_embed:
        
        # Setup mocks
        mock_client_instance = Mock()
        mock_client.return_value = mock_client_instance
        test_vector = [0.1, 0.2, 0.3, 0.4, 0.5]
        mock_embed.return_value = test_vector
        
        # Mock query builder chain
        mock_query = Mock()
        mock_get = Mock()
        mock_with_near_vector = Mock()
        mock_with_where = Mock()
        mock_with_limit = Mock()
        
        mock_client_instance.query = mock_query
        mock_query.get.return_value = mock_get
        mock_get.with_near_vector.return_value = mock_with_near_vector
        mock_with_near_vector.with_where.return_value = mock_with_where
        mock_with_where.with_limit.return_value = mock_with_limit
        
        mock_result = {"data": {"Get": {"ProjectMemory": []}}}
        mock_with_limit.do.return_value = mock_result
        
        # Call the function
        get_similar_memories("test query")
        
        # Check that the correct vector was passed
        expected_vector_param = {"vector": test_vector}
        mock_get.with_near_vector.assert_called_once_with(expected_vector_param) 