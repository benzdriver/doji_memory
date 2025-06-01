import os
import json
import hashlib
from typing import List, Optional, Dict, Union
from pathlib import Path
from openai import OpenAI, OpenAIError
from dotenv import load_dotenv

class EmbeddingRouter:
    """
    A router for handling text embeddings with caching support.
    Currently supports OpenAI's text-embedding-ada-002 model.
    """
    
    def __init__(
        self,
        cache_dir: str = ".cache/embeddings",
        model: str = "text-embedding-ada-002"
    ):
        """
        Initialize the embedding router.
        
        Args:
            cache_dir (str): Directory to store embedding cache
            model (str): OpenAI embedding model to use
            
        Raises:
            ValueError: If OPENAI_API_KEY is not found in environment variables
        """
        # Load environment variables
        load_dotenv()
        
        # Configure OpenAI
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
            
        try:
            self.client = OpenAI(api_key=api_key)
        except Exception as e:
            raise ValueError(f"Failed to initialize OpenAI client: {str(e)}")
        
        # Setup cache
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.model = model
        
    def _get_cache_key(self, text: str) -> str:
        """Generate a unique cache key for the text."""
        return hashlib.sha256(text.encode()).hexdigest()
    
    def _get_cache_path(self, cache_key: str) -> Path:
        """Get the full path for a cache file."""
        return self.cache_dir / f"{cache_key}.json"
    
    def _load_from_cache(self, cache_key: str) -> Optional[List[float]]:
        """
        Load embedding from cache if available.
        
        Args:
            cache_key (str): The cache key to look up
            
        Returns:
            Optional[List[float]]: The cached embedding vector if found, None otherwise
        """
        cache_path = self._get_cache_path(cache_key)
        if cache_path.exists():
            try:
                with cache_path.open('r') as f:
                    cache_data = json.load(f)
                return cache_data.get('embedding')
            except (json.JSONDecodeError, KeyError):
                return None
        return None
    
    def _save_to_cache(self, cache_key: str, embedding: List[float], metadata: Optional[Dict] = None):
        """
        Save embedding to cache.
        
        Args:
            cache_key (str): The cache key to save under
            embedding (List[float]): The embedding vector to cache
            metadata (Dict, optional): Additional metadata to cache
        """
        cache_path = self._get_cache_path(cache_key)
        cache_data = {
            'embedding': embedding,
            'metadata': metadata if metadata is not None else {}
        }
        with cache_path.open('w') as f:
            json.dump(cache_data, f)
    
    def _load_batch_from_cache(self, texts: List[str]) -> Dict[str, Optional[List[float]]]:
        """
        Load multiple embeddings from cache.
        
        Args:
            texts (List[str]): List of texts to check cache for
            
        Returns:
            Dict[str, Optional[List[float]]]: Mapping of text to cached embedding (None if not cached)
        """
        results = {}
        for text in texts:
            cache_key = self._get_cache_key(text)
            results[text] = self._load_from_cache(cache_key)
        return results
    
    def _save_batch_to_cache(
        self, 
        texts: List[str], 
        embeddings: List[List[float]], 
        metadata: Optional[List[Dict]] = None
    ):
        """
        Save multiple embeddings to cache.
        
        Args:
            texts (List[str]): List of texts
            embeddings (List[List[float]]): Corresponding embeddings
            metadata (Optional[List[Dict]]): Optional metadata for each embedding
        """
        if metadata is None:
            metadata = [None] * len(texts)
            
        for text, embedding, meta in zip(texts, embeddings, metadata):
            cache_key = self._get_cache_key(text)
            self._save_to_cache(cache_key, embedding, meta)
    
    def get_embedding(
        self,
        text: str,
        use_cache: bool = True,
        metadata: Optional[Dict] = None
    ) -> List[float]:
        """
        Get embedding vector for text, using cache if available.
        
        Args:
            text (str): Text to generate embedding for
            use_cache (bool): Whether to use cache. Defaults to True.
            metadata (Dict, optional): Additional metadata to store with the embedding
            
        Returns:
            List[float]: The embedding vector
            
        Raises:
            ValueError: If text is empty or invalid
            OpenAIError: If there's an error calling the OpenAI API
        """
        if not text or not isinstance(text, str):
            raise ValueError("Text must be a non-empty string")
            
        # Try cache first
        cache_key = self._get_cache_key(text)
        if use_cache:
            cached = self._load_from_cache(cache_key)
            if cached is not None:
                return cached
        
        # Generate new embedding
        try:
            response = self.client.embeddings.create(
                input=[text],
                model=self.model
            )
            embedding = response.data[0].embedding
            
            # Cache the result
            if use_cache:
                self._save_to_cache(cache_key, embedding, metadata)
            
            return embedding
            
        except OpenAIError as e:
            raise OpenAIError(f"Failed to generate embedding: {str(e)}")
    
    def get_embeddings_batch(
        self,
        texts: List[str],
        use_cache: bool = True,
        metadata: Optional[List[Dict]] = None
    ) -> List[List[float]]:
        """
        Get embedding vectors for multiple texts, using cache when available.
        
        This method optimizes API calls by:
        1. Checking cache for all texts first
        2. Only calling OpenAI API for uncached texts
        3. Batch processing uncached texts in a single API call
        
        Args:
            texts (List[str]): List of texts to generate embeddings for
            use_cache (bool): Whether to use cache. Defaults to True.
            metadata (Optional[List[Dict]]): Optional metadata for each text
            
        Returns:
            List[List[float]]: List of embedding vectors in the same order as input texts
            
        Raises:
            ValueError: If texts list is empty or contains invalid items
            OpenAIError: If there's an error calling the OpenAI API
        """
        if not texts or not isinstance(texts, list):
            raise ValueError("Texts must be a non-empty list")
        
        if not all(isinstance(text, str) and text.strip() for text in texts):
            raise ValueError("All texts must be non-empty strings")
        
        # Handle metadata
        if metadata is not None and len(metadata) != len(texts):
            raise ValueError("Metadata list must have the same length as texts list")
        
        # Initialize results list to maintain order
        results = [None] * len(texts)
        texts_to_process = []
        indices_to_process = []
        
        # Check cache for all texts if enabled
        if use_cache:
            cached_results = self._load_batch_from_cache(texts)
            for i, text in enumerate(texts):
                cached = cached_results.get(text)
                if cached is not None:
                    results[i] = cached
                else:
                    texts_to_process.append(text)
                    indices_to_process.append(i)
        else:
            texts_to_process = texts
            indices_to_process = list(range(len(texts)))
        
        # Process uncached texts in batch if any
        if texts_to_process:
            try:
                # Make batch API call to OpenAI
                response = self.client.embeddings.create(
                    input=texts_to_process,
                    model=self.model
                )
                
                # Extract embeddings from response
                new_embeddings = [item.embedding for item in response.data]
                
                # Store results in correct positions
                for i, embedding in enumerate(new_embeddings):
                    result_index = indices_to_process[i]
                    results[result_index] = embedding
                
                # Cache the new embeddings if enabled
                if use_cache:
                    batch_metadata = None
                    if metadata is not None:
                        batch_metadata = [metadata[i] for i in indices_to_process]
                    self._save_batch_to_cache(texts_to_process, new_embeddings, batch_metadata)
                
            except OpenAIError as e:
                raise OpenAIError(f"Failed to generate batch embeddings: {str(e)}")
        
        return results
            
    def clear_cache(self):
        """Clear all cached embeddings."""
        for cache_file in self.cache_dir.glob("*.json"):
            cache_file.unlink()
            
    def get_cache_info(self) -> Dict:
        """
        Get information about the cache.
        
        Returns:
            Dict: Cache statistics including size and number of entries
        """
        cache_files = list(self.cache_dir.glob("*.json"))
        total_size = sum(f.stat().st_size for f in cache_files)
        return {
            'num_entries': len(cache_files),
            'total_size_bytes': total_size,
            'cache_dir': str(self.cache_dir)
        } 