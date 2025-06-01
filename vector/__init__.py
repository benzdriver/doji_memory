"""
Vector operations package for the Weaviate memory system.
This package provides functionality for embedding generation,
memory storage, and semantic search operations.
"""

from .config import get_weaviate_client
from .embedding import embed_text, embed_texts_batch
from .memory_writer import write_memory, write_memories_batch
from .retriever_factory import get_similar_memories

__all__ = [
    'get_weaviate_client',
    'embed_text',
    'embed_texts_batch',
    'write_memory',
    'write_memories_batch',
    'get_similar_memories',
] 