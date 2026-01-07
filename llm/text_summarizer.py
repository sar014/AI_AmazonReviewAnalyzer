import os
import requests


def summarize_reviews(reviews: list[str]) -> str:
    """
    Takes a list of review strings and returns summarized PROS and CONS
    using OpenRouter (no CrewAI, no Ollama).
    """

    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise ValueError("OPENROUTER_API_KEY not set")

    # Join reviews into one block of text
    review_text = "\n\n".join(reviews)

    prompt = (
        "You are a product review analyst.\n\n"
        "Summarize the following customer reviews by extracting:\n"
        "- One consolidated PROS section\n"
        "- One consolidated CONS section\n\n"
        "Rules:\n"
        "- Do NOT summarize each review individually\n"
        "- If no pros exist, write: 'No pros found'\n"
        "- If no cons exist, write: 'No cons found'\n"
        "- Keep points short and crisp\n\n"
        f"REVIEWS:\n{review_text}"
    )

    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost",
        "X-Title": "Amazon Review Analyzer"
    }

    payload = {
        "model": "mistralai/devstral-2512:free",
        "temperature": 0.1,
        "max_tokens": 850,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    response = requests.post(url, headers=headers, json=payload, timeout=30)
    response.raise_for_status()

    data = response.json()
    return data["choices"][0]["message"]["content"].strip()
