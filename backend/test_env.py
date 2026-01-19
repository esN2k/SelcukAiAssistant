import os
from pathlib import Path
from dotenv import load_dotenv

def test_env_loading():
    env_path = Path(__file__).parent / ".env"
    if not env_path.exists():
        print("FAIL: .env file not found!")
        return False
    
    load_dotenv(env_path)
    
    required_vars = [
        "OLLAMA_MODEL",
        "RAG_VECTOR_DB_PATH",
        "SECRET_KEY",
        "DATABASE_URL"
    ]
    
    missing = []
    for var in required_vars:
        if not os.getenv(var):
            missing.append(var)
    
    if missing:
        print(f"FAIL: Missing environment variables: {', '.join(missing)}")
        return False
    
    print("SUCCESS: All critical environment variables are loaded.")
    return True

if __name__ == "__main__":
    test_env_loading()
