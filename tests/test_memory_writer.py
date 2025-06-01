import pytest
from unittest.mock import Mock, patch, MagicMock
import datetime
import weaviate
from vector.memory_writer import write_memory, write_memories_batch


def test_write_memory_success():
    """Test successful memory write."""
    with patch('vector.memory_writer.get_weaviate_client') as mock_client, \
         patch('vector.memory_writer.embed_text') as mock_embed:
        
        # Setup mocks
        mock_client_instance = Mock()
        mock_client.return_value = mock_client_instance
        mock_embed.return_value = [0.1, 0.2, 0.3]
        
        # Mock the result object with uuid attribute
        mock_result = Mock()
        mock_result.uuid = "test-uuid-123"
        mock_client_instance.data_object.create.return_value = mock_result
        
        # Call the function
        result = write_memory(
            content="Test memory content",
            project="test-project",
            repo="test-repo",
            agent="test-agent",
            tags=["tag1", "tag2"]
        )
        
        # Verify the result
        assert result == "test-uuid-123"
        
        # Verify the calls
        mock_embed.assert_called_once_with("Test memory content")
        mock_client_instance.data_object.create.assert_called_once()


def test_write_memory_with_custom_source():
    """Test memory write with custom source."""
    with patch('vector.memory_writer.get_weaviate_client') as mock_client, \
         patch('vector.memory_writer.embed_text') as mock_embed:
        
        # Setup mocks
        mock_client_instance = Mock()
        mock_client.return_value = mock_client_instance
        mock_embed.return_value = [0.1, 0.2, 0.3]
        
        mock_result = Mock()
        mock_result.uuid = "test-uuid-456"
        mock_client_instance.data_object.create.return_value = mock_result
        
        # Call with custom source
        result = write_memory(
            content="Test memory",
            project="project",
            repo="repo",
            agent="agent",
            tags=["tag"],
            source="custom-source"
        )
        
        assert result == "test-uuid-456"


def test_write_memory_invalid_content():
    """Test validation error for invalid content."""
    with pytest.raises(ValueError, match="Content must be a non-empty string"):
        write_memory("", "project", "repo", "agent", ["tag"])
    
    with pytest.raises(ValueError, match="Content must be a non-empty string"):
        write_memory(None, "project", "repo", "agent", ["tag"])


def test_write_memory_invalid_project():
    """Test validation error for invalid project."""
    with pytest.raises(ValueError, match="Project must be a non-empty string"):
        write_memory("content", "", "repo", "agent", ["tag"])
    
    with pytest.raises(ValueError, match="Project must be a non-empty string"):
        write_memory("content", None, "repo", "agent", ["tag"])


def test_write_memory_invalid_repo():
    """Test validation error for invalid repo."""
    with pytest.raises(ValueError, match="Repo must be a non-empty string"):
        write_memory("content", "project", "", "agent", ["tag"])
    
    with pytest.raises(ValueError, match="Repo must be a non-empty string"):
        write_memory("content", "project", None, "agent", ["tag"])


def test_write_memory_invalid_agent():
    """Test validation error for invalid agent."""
    with pytest.raises(ValueError, match="Agent must be a non-empty string"):
        write_memory("content", "project", "repo", "", ["tag"])
    
    with pytest.raises(ValueError, match="Agent must be a non-empty string"):
        write_memory("content", "project", "repo", None, ["tag"])


def test_write_memory_invalid_tags():
    """Test validation error for invalid tags."""
    with pytest.raises(ValueError, match="Tags must be a list of strings"):
        write_memory("content", "project", "repo", "agent", "not-a-list")
    
    with pytest.raises(ValueError, match="Tags must be a list of strings"):
        write_memory("content", "project", "repo", "agent", [1, 2, 3])
    
    with pytest.raises(ValueError, match="Tags must be a list of strings"):
        write_memory("content", "project", "repo", "agent", ["valid", 123])


def test_write_memory_exception():
    """Test handling of general exceptions."""
    with patch('vector.memory_writer.get_weaviate_client') as mock_client, \
         patch('vector.memory_writer.embed_text') as mock_embed:
        
        # Setup mocks
        mock_client_instance = Mock()
        mock_client.return_value = mock_client_instance
        mock_embed.return_value = [0.1, 0.2, 0.3]
        
        # Make the create method raise an exception
        mock_client_instance.data_object.create.side_effect = Exception("Weaviate error")
        
        # Test that it raises an exception
        with pytest.raises(Exception):
            write_memory("content", "project", "repo", "agent", ["tag"])


def test_write_memory_data_object_structure():
    """Test that the data object has the correct structure."""
    with patch('vector.memory_writer.get_weaviate_client') as mock_client, \
         patch('vector.memory_writer.embed_text') as mock_embed, \
         patch('datetime.datetime') as mock_datetime:
        
        # Setup mocks
        mock_client_instance = Mock()
        mock_client.return_value = mock_client_instance
        mock_embed.return_value = [0.1, 0.2, 0.3]
        
        # Mock datetime
        mock_now = Mock()
        mock_now.isoformat.return_value = "2024-01-01T12:00:00"
        mock_datetime.utcnow.return_value = mock_now
        
        mock_result = Mock()
        mock_result.uuid = "test-uuid"
        mock_client_instance.data_object.create.return_value = mock_result
        
        # Call the function
        write_memory("content", "project", "repo", "agent", ["tag1", "tag2"], "custom")
        
        # Check the call arguments
        call_args = mock_client_instance.data_object.create.call_args
        data_object = call_args[1]['data_object']
        
        assert data_object['content'] == "content"
        assert data_object['project'] == "project"
        assert data_object['repo'] == "repo"
        assert data_object['agent'] == "agent"
        assert data_object['tags'] == ["tag1", "tag2"]
        assert data_object['source'] == "custom"
        assert data_object['timestamp'] == "2024-01-01T12:00:00"
        
        assert call_args[1]['class_name'] == "ProjectMemory"
        assert call_args[1]['vector'] == [0.1, 0.2, 0.3]

# Batch processing tests for write_memories_batch
def test_write_memories_batch_success():
    """Test successful batch memory write."""
    with patch('vector.memory_writer.get_weaviate_client') as mock_client, \
         patch('vector.memory_writer.embed_texts_batch') as mock_embed_batch:
        
        # Setup mocks
        mock_client_instance = Mock()
        mock_client.return_value = mock_client_instance
        mock_embed_batch.return_value = [[0.1, 0.2, 0.3], [0.4, 0.5, 0.6]]
        
        # Mock results
        mock_result1 = Mock()
        mock_result1.uuid = "uuid-1"
        mock_result2 = Mock()
        mock_result2.uuid = "uuid-2"
        mock_client_instance.data_object.create.side_effect = [mock_result1, mock_result2]
        
        # Test data
        memories = [
            {
                "content": "Memory 1",
                "project": "project1",
                "repo": "repo1",
                "agent": "agent1",
                "tags": ["tag1"]
            },
            {
                "content": "Memory 2",
                "project": "project2",
                "repo": "repo2",
                "agent": "agent2",
                "tags": ["tag2"],
                "source": "user"
            }
        ]
        
        # Call the function
        result = write_memories_batch(memories)
        
        # Verify results
        assert result == ["uuid-1", "uuid-2"]
        mock_embed_batch.assert_called_once_with(["Memory 1", "Memory 2"])
        assert mock_client_instance.data_object.create.call_count == 2


def test_write_memories_batch_invalid_input():
    """Test batch memory write with invalid inputs."""
    # Empty list
    with pytest.raises(ValueError, match="Memories must be a non-empty list"):
        write_memories_batch([])
    
    # Not a list
    with pytest.raises(ValueError, match="Memories must be a non-empty list"):
        write_memories_batch("not a list")
    
    # Invalid memory object
    with pytest.raises(ValueError, match="Memory at index 0 must be a dictionary"):
        write_memories_batch(["not a dict"])


def test_write_memories_batch_invalid_memory_fields():
    """Test batch memory write with invalid memory fields."""
    # Missing content
    with pytest.raises(ValueError, match="Memory at index 0: content must be a non-empty string"):
        write_memories_batch([{
            "project": "project",
            "repo": "repo", 
            "agent": "agent",
            "tags": ["tag"]
        }])
    
    # Invalid content
    with pytest.raises(ValueError, match="Memory at index 0: content must be a non-empty string"):
        write_memories_batch([{
            "content": "",
            "project": "project",
            "repo": "repo",
            "agent": "agent", 
            "tags": ["tag"]
        }])
    
    # Missing project
    with pytest.raises(ValueError, match="Memory at index 0: project must be a non-empty string"):
        write_memories_batch([{
            "content": "content",
            "repo": "repo",
            "agent": "agent",
            "tags": ["tag"]
        }])
    
    # Invalid tags
    with pytest.raises(ValueError, match="Memory at index 0: tags must be a list of strings"):
        write_memories_batch([{
            "content": "content",
            "project": "project",
            "repo": "repo",
            "agent": "agent",
            "tags": "not a list"
        }])


def test_write_memories_batch_default_source():
    """Test that batch write sets default source."""
    with patch('vector.memory_writer.get_weaviate_client') as mock_client, \
         patch('vector.memory_writer.embed_texts_batch') as mock_embed_batch, \
         patch('datetime.datetime') as mock_datetime:
        
        # Setup mocks
        mock_client_instance = Mock()
        mock_client.return_value = mock_client_instance
        mock_embed_batch.return_value = [[0.1, 0.2, 0.3]]
        
        mock_now = Mock()
        mock_now.isoformat.return_value = "2024-01-01T12:00:00"
        mock_datetime.utcnow.return_value = mock_now
        
        mock_result = Mock()
        mock_result.uuid = "uuid-1"
        mock_client_instance.data_object.create.return_value = mock_result
        
        # Test data without source
        memories = [{
            "content": "Memory 1",
            "project": "project1",
            "repo": "repo1",
            "agent": "agent1",
            "tags": ["tag1"]
        }]
        
        write_memories_batch(memories)
        
        # Check that default source was set
        call_args = mock_client_instance.data_object.create.call_args
        data_object = call_args[1]['data_object']
        assert data_object['source'] == "agent"  # Default source
        assert data_object['timestamp'] == "2024-01-01T12:00:00"


def test_write_memories_batch_weaviate_error():
    """Test batch memory write with Weaviate error."""
    with patch('vector.memory_writer.get_weaviate_client') as mock_client, \
         patch('vector.memory_writer.embed_texts_batch') as mock_embed_batch:
        
        # Setup mocks
        mock_client_instance = Mock()
        mock_client.return_value = mock_client_instance
        mock_embed_batch.return_value = [[0.1, 0.2, 0.3]]
        
        # Make create method raise an exception
        mock_client_instance.data_object.create.side_effect = Exception("Weaviate error")
        
        memories = [{
            "content": "Memory 1",
            "project": "project1",
            "repo": "repo1",
            "agent": "agent1",
            "tags": ["tag1"]
        }]
        
        with pytest.raises(Exception, match="Failed to write memory"):
            write_memories_batch(memories)


def test_write_memories_batch_embedding_error():
    """Test batch memory write with embedding error."""
    with patch('vector.memory_writer.embed_texts_batch') as mock_embed_batch:
        
        # Make embedding generation fail
        mock_embed_batch.side_effect = Exception("Embedding error")
        
        memories = [{
            "content": "Memory 1",
            "project": "project1",
            "repo": "repo1",
            "agent": "agent1",
            "tags": ["tag1"]
        }]
        
        with pytest.raises(Exception, match="Failed to write memories batch"):
            write_memories_batch(memories)


def test_write_memories_batch_validation_comprehensive():
    """Test comprehensive validation of batch memory write."""
    # Test validation at different indices
    memories = [
        {
            "content": "Memory 1",
            "project": "project1",
            "repo": "repo1",
            "agent": "agent1",
            "tags": ["tag1"]
        },
        {
            "content": "",  # Invalid content at index 1
            "project": "project2",
            "repo": "repo2",
            "agent": "agent2",
            "tags": ["tag2"]
        }
    ]
    
    with pytest.raises(ValueError, match="Memory at index 1: content must be a non-empty string"):
        write_memories_batch(memories) 