import weaviate
from typing import Optional

def get_weaviate_client(url: str = "http://localhost:8080") -> weaviate.Client:
    """
    Get a configured Weaviate client instance.
    
    This function creates and returns a Weaviate client that can be used to interact
    with the Weaviate vector database. The client is configured with the specified URL.
    
    Args:
        url (str): The URL where the Weaviate instance is running. 
                  Defaults to "http://localhost:8080" for local development.
        
    Returns:
        weaviate.Client: A configured Weaviate client instance ready for use.
        
    Example:
        >>> client = get_weaviate_client()
        >>> # Use client to interact with Weaviate
        >>> client.schema.get()
    """
    client = weaviate.Client(url)
    return client 