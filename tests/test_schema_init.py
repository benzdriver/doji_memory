import pytest
from unittest.mock import Mock, patch
from vector.schema_init import create_project_memory_class, class_name


def test_create_project_memory_class_new_class():
    """Test creating ProjectMemory class when it doesn't exist."""
    # Create a mock client
    mock_client = Mock()
    mock_client.schema.contains.return_value = False
    
    # Call the function
    create_project_memory_class(mock_client)
    
    # Verify that contains was called with the correct class
    mock_client.schema.contains.assert_called_once_with({"class": "ProjectMemory"})
    
    # Verify that create_class was called
    mock_client.schema.create_class.assert_called_once()
    
    # Check the class definition that was passed
    call_args = mock_client.schema.create_class.call_args[0][0]
    assert call_args["class"] == "ProjectMemory"
    assert call_args["description"] == "Long-term semantic memory for all AI agents and projects."
    
    # Check properties
    properties = call_args["properties"]
    property_names = [prop["name"] for prop in properties]
    expected_properties = ["content", "project", "repo", "agent", "tags", "source", "timestamp"]
    assert property_names == expected_properties
    
    # Check specific property data types
    property_dict = {prop["name"]: prop["dataType"] for prop in properties}
    assert property_dict["content"] == ["text"]
    assert property_dict["project"] == ["string"]
    assert property_dict["repo"] == ["string"]
    assert property_dict["agent"] == ["string"]
    assert property_dict["tags"] == ["string[]"]
    assert property_dict["source"] == ["string"]
    assert property_dict["timestamp"] == ["date"]


def test_create_project_memory_class_existing_class():
    """Test that nothing happens when ProjectMemory class already exists."""
    # Create a mock client
    mock_client = Mock()
    mock_client.schema.contains.return_value = True
    
    # Call the function
    create_project_memory_class(mock_client)
    
    # Verify that contains was called
    mock_client.schema.contains.assert_called_once_with({"class": "ProjectMemory"})
    
    # Verify that create_class was NOT called
    mock_client.schema.create_class.assert_not_called()


def test_class_name_constant():
    """Test that the class_name constant is correct."""
    assert class_name == "ProjectMemory"


def test_create_project_memory_class_schema_structure():
    """Test the complete schema structure in detail."""
    mock_client = Mock()
    mock_client.schema.contains.return_value = False
    
    create_project_memory_class(mock_client)
    
    # Get the actual class object that was passed
    call_args = mock_client.schema.create_class.call_args[0][0]
    
    # Test the complete structure
    expected_class_obj = {
        "class": "ProjectMemory",
        "description": "Long-term semantic memory for all AI agents and projects.",
        "properties": [
            {"name": "content", "dataType": ["text"]},
            {"name": "project", "dataType": ["string"]},
            {"name": "repo", "dataType": ["string"]},
            {"name": "agent", "dataType": ["string"]},
            {"name": "tags", "dataType": ["string[]"]},
            {"name": "source", "dataType": ["string"]},
            {"name": "timestamp", "dataType": ["date"]}
        ]
    }
    
    assert call_args == expected_class_obj


def test_create_project_memory_class_integration():
    """Test the function with a more realistic mock setup."""
    mock_client = Mock()
    
    # Test both scenarios in sequence
    # First: class doesn't exist
    mock_client.schema.contains.return_value = False
    create_project_memory_class(mock_client)
    assert mock_client.schema.create_class.called
    
    # Reset the mock
    mock_client.reset_mock()
    
    # Second: class already exists
    mock_client.schema.contains.return_value = True
    create_project_memory_class(mock_client)
    assert not mock_client.schema.create_class.called 