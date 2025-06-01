import weaviate
from typing import Dict, Any

# The class name for project memory objects in Weaviate
class_name = "ProjectMemory"

def create_project_memory_class(client: weaviate.Client) -> None:
    """
    Create the ProjectMemory class schema in Weaviate if it doesn't exist.
    
    This function defines the schema for storing project-related memories in Weaviate.
    The schema includes fields for content, project details, and metadata.
    
    Schema Properties:
        - content: The main text content of the memory
        - project: The project identifier
        - repo: The repository name
        - agent: The AI agent identifier
        - tags: Array of relevant tags
        - source: The source of the memory (default: "agent")
        - timestamp: When the memory was created
    
    Args:
        client (weaviate.Client): The Weaviate client instance to use
        
    Example:
        >>> client = get_weaviate_client()
        >>> create_project_memory_class(client)
    """
    class_obj: Dict[str, Any] = {
        "class": class_name,
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

    # Only create if the class doesn't already exist
    if not client.schema.contains({"class": class_name}):
        client.schema.create_class(class_obj)
