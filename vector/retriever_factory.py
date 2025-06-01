from typing import Optional, Dict, Any, List
from vector.config import get_weaviate_client
from vector.embedding import embed_text

def get_similar_memories(
    query: str,
    project: Optional[str] = None,
    limit: int = 5
) -> List[Dict[str, Any]]:
    """
    Search for similar memories using semantic similarity.
    
    This function performs a vector similarity search over stored memories
    using the query's embedding vector. It can filter results by project.
    
    Args:
        query (str): The search query text
        project (str, optional): Filter results to a specific project
        limit (int): Maximum number of results to return. Defaults to 5.
        
    Returns:
        List[Dict[str, Any]]: List of matching memories with their metadata
        
    Example:
        >>> memories = get_similar_memories(
        ...     query="semantic loop issues",
        ...     project="generic-ai-agent",
        ...     limit=3
        ... )
        >>> for mem in memories:
        ...     print(f"Content: {mem['content']}")
    """
    client = get_weaviate_client()
    vector = embed_text(query)
    
    # Prepare where filter if project is specified
    where_filter = None
    if project:
        where_filter = {
            "path": ["project"],
            "operator": "Equal",
            "valueString": project
        }
    
    # Perform vector search
    result = (client.query
        .get("ProjectMemory", [
            "content",
            "project",
            "repo",
            "agent",
            "tags",
            "source",
            "timestamp"
        ])
        .with_near_vector({
            "vector": vector
        })
        .with_where(where_filter)
        .with_limit(limit)
        .do()
    )
    
    # Extract and return memories from result
    memories = result.get("data", {}).get("Get", {}).get("ProjectMemory", [])
    return memories
