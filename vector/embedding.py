import os
from typing import List, Optional, Dict
from openai import OpenAI, OpenAIError
from dotenv import load_dotenv
from .embedding_router import EmbeddingRouter

# Load environment variables from .env file
load_dotenv()

# Configure OpenAI with API key
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY not found in environment variables")

# Create a global router instance
_router = EmbeddingRouter()

def embed_text(text: str) -> List[float]:
    """
    Generate an embedding vector for the given text using OpenAI's API.
    
    This function uses OpenAI's text-embedding-ada-002 model to create
    a vector representation of the input text that can be used for 
    semantic similarity search.
    
    Args:
        text (str): The text to generate an embedding for
        
    Returns:
        List[float]: The embedding vector as a list of floats
        
    Raises:
        OpenAIError: If there's an error calling the OpenAI API
        ValueError: If the input text is empty or invalid
        
    Example:
        >>> vector = embed_text("Example memory text")
        >>> len(vector)  # Typically 1536 dimensions
        1536
    """
    if not text or not isinstance(text, str):
        raise ValueError("Input text must be a non-empty string")
        
    try:
        return _router.get_embedding(text)
    except OpenAIError as e:
        raise OpenAIError(f"Failed to generate embedding: {str(e)}")

def embed_texts_batch(texts: List[str], metadata: Optional[List[Dict]] = None) -> List[List[float]]:
    """
    Generate embedding vectors for multiple texts using OpenAI's API in batch.
    
    This function efficiently processes multiple texts by:
    1. Checking cache for each text first
    2. Only calling OpenAI API for uncached texts
    3. Processing uncached texts in a single batch API call
    
    Args:
        texts (List[str]): List of texts to generate embeddings for
        metadata (Optional[List[Dict]]): Optional metadata for each text
        
    Returns:
        List[List[float]]: List of embedding vectors in the same order as input texts
        
    Raises:
        OpenAIError: If there's an error calling the OpenAI API
        ValueError: If the input texts are empty or invalid
        
    Example:
        >>> texts = ["First text", "Second text", "Third text"]
        >>> vectors = embed_texts_batch(texts)
        >>> len(vectors)  # Same as number of input texts
        3
        >>> len(vectors[0])  # Typically 1536 dimensions
        1536
    """
    if not texts or not isinstance(texts, list):
        raise ValueError("Input texts must be a non-empty list")
        
    if not all(isinstance(text, str) and text.strip() for text in texts):
        raise ValueError("All texts must be non-empty strings")
        
    try:
        return _router.get_embeddings_batch(texts, metadata=metadata)
    except OpenAIError as e:
        raise OpenAIError(f"Failed to generate batch embeddings: {str(e)}")
