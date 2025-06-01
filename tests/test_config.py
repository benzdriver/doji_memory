import pytest
import weaviate
from unittest.mock import patch, Mock
from vector.config import get_weaviate_client


@patch('vector.config.weaviate.Client')
def test_get_weaviate_client_default(mock_client):
    """Test getting Weaviate client with default URL."""
    mock_instance = Mock()
    mock_client.return_value = mock_instance
    
    client = get_weaviate_client()
    
    # Verify that weaviate.Client was called with default URL
    mock_client.assert_called_once_with("http://localhost:8080")
    assert client == mock_instance


@patch('vector.config.weaviate.Client')
def test_get_weaviate_client_custom_url(mock_client):
    """Test getting Weaviate client with custom URL."""
    mock_instance = Mock()
    mock_client.return_value = mock_instance
    custom_url = "http://custom-host:9999"
    
    client = get_weaviate_client(custom_url)
    
    # Verify that weaviate.Client was called with custom URL
    mock_client.assert_called_once_with(custom_url)
    assert client == mock_instance


@patch('vector.config.weaviate.Client')
def test_get_weaviate_client_return_type(mock_client):
    """Test that the function returns the correct type."""
    mock_instance = Mock()
    mock_client.return_value = mock_instance
    
    client = get_weaviate_client()
    
    # Verify the return value
    assert client == mock_instance
    mock_client.assert_called_once() 