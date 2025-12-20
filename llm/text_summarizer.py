from ollama import chat

def summarize_reviews(reviews, model_name="llama3"):
    """
    Takes a list of review strings, sends them to Ollama,
    and returns the summarized pros and cons.
    """
    prompt = (
        f"Summarize the following reviews by giving pros and cons:\n{reviews}\n"
        "Dont provide pros and cons for each review but create one section for pros and one section for cons"
        "If pros don't exist write 'No pros found' and if cons don't exist write 'No cons found'."
    )

    response = chat(
        model=model_name,
        messages=[{"role": "user", "content": prompt}]
    )

    return response["message"]["content"]
