import os
import sys

def check_env_vars():
    print("Checking environment variables...")
    
    # Required API keys
    required_keys = ["OPENAI_API_KEY", "PINECONE_API_KEY", "LANGSMITH_API_KEY"]
    optional_keys = ["LANGSMITH_PROJECT", "EMBEDDING_MODEL", "OPENAI_VALIDATION_MODEL", 
                     "OPENAI_GENERATION_MODEL", "PINECONE_INDEX_NAME"]
    
    missing_keys = []
    malformed_keys = []
    
    for key in required_keys:
        value = os.environ.get(key)
        if not value:
            missing_keys.append(key)
            print(f"❌ {key}: MISSING")
        else:
            # Check for obvious malformed values
            if key == "OPENAI_API_KEY" and not (value.startswith("sk-") or "Bearer" in value):
                malformed_keys.append(f"{key} (should start with 'sk-')")
                print(f"⚠️ {key}: PRESENT but may be malformed (doesn't start with 'sk-')")
            else:
                # Don't print actual keys for security reasons
                print(f"✅ {key}: PRESENT (value hidden)")
    
    for key in optional_keys:
        value = os.environ.get(key)
        if not value:
            print(f"ℹ️ {key}: NOT SET (optional)")
        else:
            print(f"✅ {key}: SET to '{value}'")
    
    if missing_keys:
        print(f"\n⚠️ Missing required keys: {', '.join(missing_keys)}")
    
    if malformed_keys:
        print(f"\n⚠️ Potentially malformed keys: {', '.join(malformed_keys)}")
    
    if not missing_keys and not malformed_keys:
        print("\n✅ All required environment variables are set properly.")
    
    # Check OPENAI_API_KEY format specifically
    openai_key = os.environ.get("OPENAI_API_KEY", "")
    if openai_key and "Bearer" in openai_key:
        print("\n⚠️ WARNING: Your OPENAI_API_KEY contains 'Bearer' which is incorrect.")
        print("   The API key should be just the key value (starts with 'sk-'), not the full header.")
        print("   In Hugging Face, ensure you're only entering the key value without 'Bearer '.")

if __name__ == "__main__":
    check_env_vars() 