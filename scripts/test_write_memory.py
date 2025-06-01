from vector.memory_writer import write_memory
import sys

def main():
    """Test the memory writing functionality with a sample memory."""
    try:
        uuid = write_memory(
            content="Nova 成功解决了 semantic loop 的 prompt 问题。",
            project="generic-ai-agent",
            repo="clarifier",
            agent="nova",
            tags=["prompt", "semantic-loop", "success"]
        )
        print("✅ Memory written successfully!")
        print(f"Memory UUID: {uuid}")
        
    except Exception as e:
        print(f"❌ Error writing memory: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
