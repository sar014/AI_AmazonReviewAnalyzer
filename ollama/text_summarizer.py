import requests
import json

# Configuration
OLLAMA_URL = "http://localhost:11434"  # Ollama local server
MODEL_NAME = "ollama/llama3"           # Your Ollama model

def query_ollama(prompt: str, model: str = MODEL_NAME):
    """
    Sends a prompt to the local Ollama server and returns the response.
    """
    endpoint = f"{OLLAMA_URL}/api/completions"
    headers = {"Content-Type": "application/json"}
    
    payload = {
        "model": model,
        "prompt": prompt,
        "max_tokens": 200
    }

    response = requests.post(endpoint, headers=headers, data=json.dumps(payload))
    response.raise_for_status()  # Will throw an error if request fails

    result = response.json()
    # Ollama responses usually have: result['completion']
    return result.get("completion", "")

# Test the model
if __name__ == "__main__":
    prompt = "Hello Ollama, can you introduce yourself?"
    reply = query_ollama(prompt)
    print("Ollama Response:\n", reply)
