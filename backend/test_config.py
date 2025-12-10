"""Test script to verify config.py has no errors."""
import sys

try:
    import config

    print("✓ config.py imported successfully!")
    print(f"  - Host: {config.Config.HOST}")
    print(f"  - Port: {config.Config.PORT}")
    print(f"  - Model: {config.Config.OLLAMA_MODEL}")
    print(f"  - Ollama URL: {config.Config.OLLAMA_BASE_URL}")
    print(f"  - Log Level: {config.Config.LOG_LEVEL}")
    print("\n✓ All configuration values loaded correctly!")
    sys.exit(0)
except SyntaxError as e:
    print(f"✗ Syntax Error in config.py: {e}")
    sys.exit(1)
except Exception as e:
    print(f"✗ Error loading config.py: {e}")
    sys.exit(1)
