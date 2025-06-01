from vector.config import get_weaviate_client
from vector.schema_init import create_project_memory_class

if __name__ == "__main__":
    client = get_weaviate_client()
    create_project_memory_class(client)
    print("✅ ProjectMemory schema created.")
