# secrets_example.py
import os
key = os.environ.get("API_KEY", "")
if key:
    print("API key length:", len(key))
else:
    print("No API key set")
