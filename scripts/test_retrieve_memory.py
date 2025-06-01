from vector.retriever_factory import get_similar_memories
import sys
from typing import Dict, Any

def format_memory(memory: Dict[str, Any]) -> str:
    """Format a memory object for display."""
    return (
        f"Content: {memory['content']}\n"
        f"Project: {memory['project']}\n"
        f"Repo: {memory['repo']}\n"
        f"Agent: {memory['agent']}\n"
        f"Tags: {', '.join(memory['tags'])}\n"
        f"Time: {memory['timestamp']}"
    )

def main():
    """Test the memory retrieval functionality with a sample query."""
    try:
        # Perform the search
        query = "semantic loop"
        print(f"🔍 Searching for: '{query}'")
        print("---")
        
        memories = get_similar_memories(
            query=query,
            project="generic-ai-agent",
            limit=5
        )
        
        if not memories:
            print("No matching memories found.")
            return
            
        # Display results
        for i, memory in enumerate(memories, 1):
            print(f"\nResult {i}:")
            print(format_memory(memory))
            print("---")
            
        print(f"✅ Found {len(memories)} relevant memories.")
        
    except Exception as e:
        print(f"❌ Error retrieving memories: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
