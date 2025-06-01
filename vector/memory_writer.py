import datetime
from typing import List, Optional, Dict, Any
import weaviate
from vector.config import get_weaviate_client
from vector.embedding import embed_text, embed_texts_batch

def write_memory(
    content: str,
    project: str,
    repo: str,
    agent: str,
    tags: List[str],
    source: str = "agent"
) -> str:
    """
    Write a new memory entry to the Weaviate database.
    
    This function creates a new memory entry with the given content and metadata,
    generates its embedding vector, and stores it in Weaviate.
    
    Args:
        content (str): The main text content of the memory
        project (str): The project identifier
        repo (str): The repository name
        agent (str): The AI agent identifier
        tags (List[str]): List of relevant tags for categorization
        source (str, optional): Source of the memory. Defaults to "agent"
        
    Returns:
        str: The UUID of the created memory object
        
    Raises:
        ValueError: If any required parameters are empty or invalid
        Exception: If there's an error writing to Weaviate
        
    Example:
        >>> uuid = write_memory(
        ...     content="Implemented new feature X",
        ...     project="my-project",
        ...     repo="main-repo",
        ...     agent="assistant",
        ...     tags=["feature", "implementation"]
        ... )
    """
    # Validate input parameters
    if not content or not isinstance(content, str):
        raise ValueError("Content must be a non-empty string")
    if not project or not isinstance(project, str):
        raise ValueError("Project must be a non-empty string")
    if not repo or not isinstance(repo, str):
        raise ValueError("Repo must be a non-empty string")
    if not agent or not isinstance(agent, str):
        raise ValueError("Agent must be a non-empty string")
    if not isinstance(tags, list) or not all(isinstance(tag, str) for tag in tags):
        raise ValueError("Tags must be a list of strings")
        
    # Get client and generate embedding
    client = get_weaviate_client()
    vector = embed_text(content)
    
    # Prepare the data object
    data_object = {
        "content": content,
        "project": project,
        "repo": repo,
        "agent": agent,
        "tags": tags,
        "source": source,
        "timestamp": datetime.datetime.utcnow().isoformat()
    }
    
    # Write to Weaviate
    try:
        result = client.data_object.create(
            data_object=data_object,
            class_name="ProjectMemory",
            vector=vector
        )
        return result.uuid
    except Exception as e:
        raise Exception(f"Failed to write memory: {str(e)}")

def write_memories_batch(memories: List[Dict[str, Any]]) -> List[str]:
    """
    Write multiple memory entries to the Weaviate database in batch.
    
    This function efficiently processes multiple memories by:
    1. Validating all memories upfront
    2. Generating embeddings in batch
    3. Writing all memories to Weaviate in batch
    
    Args:
        memories (List[Dict[str, Any]]): List of memory dictionaries, each containing:
            - content (str): The main text content of the memory
            - project (str): The project identifier  
            - repo (str): The repository name
            - agent (str): The AI agent identifier
            - tags (List[str]): List of relevant tags for categorization
            - source (str, optional): Source of the memory. Defaults to "agent"
            
    Returns:
        List[str]: List of UUIDs for the created memory objects in the same order
        
    Raises:
        ValueError: If memories list is empty or contains invalid entries
        Exception: If there's an error writing to Weaviate
        
    Example:
        >>> memories = [
        ...     {
        ...         "content": "Implemented feature A",
        ...         "project": "my-project",
        ...         "repo": "main-repo", 
        ...         "agent": "assistant",
        ...         "tags": ["feature", "implementation"]
        ...     },
        ...     {
        ...         "content": "Fixed bug B",
        ...         "project": "my-project",
        ...         "repo": "main-repo",
        ...         "agent": "assistant", 
        ...         "tags": ["bugfix"],
        ...         "source": "user"
        ...     }
        ... ]
        >>> uuids = write_memories_batch(memories)
        >>> len(uuids)  # Same as number of input memories
        2
    """
    if not memories or not isinstance(memories, list):
        raise ValueError("Memories must be a non-empty list")
    
    # Validate all memories upfront
    validated_memories = []
    contents = []
    
    for i, memory in enumerate(memories):
        if not isinstance(memory, dict):
            raise ValueError(f"Memory at index {i} must be a dictionary")
        
        # Validate required fields
        content = memory.get("content")
        project = memory.get("project") 
        repo = memory.get("repo")
        agent = memory.get("agent")
        tags = memory.get("tags")
        source = memory.get("source", "agent")  # Default source
        
        if not content or not isinstance(content, str):
            raise ValueError(f"Memory at index {i}: content must be a non-empty string")
        if not project or not isinstance(project, str):
            raise ValueError(f"Memory at index {i}: project must be a non-empty string")
        if not repo or not isinstance(repo, str):
            raise ValueError(f"Memory at index {i}: repo must be a non-empty string")
        if not agent or not isinstance(agent, str):
            raise ValueError(f"Memory at index {i}: agent must be a non-empty string")
        if not isinstance(tags, list) or not all(isinstance(tag, str) for tag in tags):
            raise ValueError(f"Memory at index {i}: tags must be a list of strings")
        if not isinstance(source, str):
            raise ValueError(f"Memory at index {i}: source must be a string")
        
        # Store validated memory
        validated_memory = {
            "content": content,
            "project": project,
            "repo": repo,
            "agent": agent,
            "tags": tags,
            "source": source,
            "timestamp": datetime.datetime.utcnow().isoformat()
        }
        validated_memories.append(validated_memory)
        contents.append(content)
    
    try:
        # Generate embeddings in batch
        vectors = embed_texts_batch(contents)
        
        # Get Weaviate client
        client = get_weaviate_client()
        
        # Prepare batch operation
        uuids = []
        
        # Process each memory with its corresponding vector
        for memory, vector in zip(validated_memories, vectors):
            try:
                result = client.data_object.create(
                    data_object=memory,
                    class_name="ProjectMemory", 
                    vector=vector
                )
                uuids.append(result.uuid)
            except Exception as e:
                # If one memory fails, we still continue but track the error
                raise Exception(f"Failed to write memory '{memory['content'][:50]}...': {str(e)}")
        
        return uuids
        
    except Exception as e:
        raise Exception(f"Failed to write memories batch: {str(e)}")
