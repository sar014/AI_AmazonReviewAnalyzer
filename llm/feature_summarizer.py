from ollama import chat

def summarize_features(feature, model_name="llama3.2:1b"):
    
    """
    Takes a feature strings, sends them to Ollama,
    and return the summary of each feature in short.
    """
    prompt = (
        f"For each feature:{feature} give a short summary.Keep it crisp,brief and concise."
    )

    response = chat(
        model=model_name,
        messages=[{"role": "user", "content": prompt}]
    )

    return response["message"]["content"]
