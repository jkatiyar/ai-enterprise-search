import requests
import json

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.2:3b"


def generate_answer(prompt: str) -> str:
    """
    Sends prompt to local Ollama model and returns generated answer.
    """
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False
    }

    try:
        response = requests.post(
            OLLAMA_URL,
            headers={"Content-Type": "application/json"},
            data=json.dumps(payload),
            timeout=120
        )
        response.raise_for_status()
        return response.json().get("response", "").strip()

    except Exception as e:
        return f"LLM error: {str(e)}"
