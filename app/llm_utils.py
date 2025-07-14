# app/llm_utils.py

import requests
import os
import json
import time
from functools import lru_cache
from pathlib import Path

API_KEY = os.getenv("OPENROUTER_API_KEY")
BASE_URL = "https://openrouter.ai/api/v1"
FALLBACK_MODELS = [
    "qwen/qwen3-14b:free",
    "mistralai/mistral-7b-instruct:free",
    "deepseek/deepseek-chat-v3-0324:free"
]

# 🗂️ Use ~/.grocerygpt/ for clean cache management
CACHE_DIR = Path.home() / ".grocerygpt"
CACHE_DIR.mkdir(exist_ok=True)
CACHE_FILE = CACHE_DIR / "model_cache.json"

SELECTED_MODEL = None


def load_cached_model():
    if CACHE_FILE.exists():
        try:
            with open(CACHE_FILE, "r") as f:
                cached = json.load(f)
                print(f"[INFO] Using cached model: {cached}")
                return cached
        except Exception as e:
            print(f"[WARNING] Failed to load cached model: {e}")
    return None


def save_cached_model(model_id):
    try:
        with open(CACHE_FILE, "w") as f:
            json.dump(model_id, f)
        print(f"[INFO] Cached model: {model_id}")
    except Exception as e:
        print(f"[ERROR] Failed to save cached model: {e}")


def ping_model(model_id):
    """
    Sends a basic prompt to verify the model is actually working.
    """
    try:
        start_time = time.time()

        res = requests.post(
            f"{BASE_URL}/chat/completions",
            headers={"Authorization": f"Bearer {API_KEY}"},
            json={
                "model": model_id,
                "messages": [{"role": "user", "content": f"Say 'Hello from {model_id}'"}],
                "max_tokens": 20,
            },
            timeout=10,
        )
        res.raise_for_status()

        elapsed_ms = (time.time() - start_time) * 1000
        message = res.json().get("choices", [{}])[0].get("message", {}).get("content", "")
        success = f"Hello from {model_id}" in message

        print(f"[INFO] Model {model_id} ping success: {success} | Latency: {elapsed_ms:.2f} ms")
        return success
    except Exception as e:
        print(f"[WARNING] Model {model_id} ping failed: {e}")
        return False


@lru_cache(maxsize=1)
def get_available_model():
    global SELECTED_MODEL

    # Try cached model
    cached_model = load_cached_model()
    if cached_model and ping_model(cached_model):
        SELECTED_MODEL = cached_model
        return SELECTED_MODEL

    # Live check from OpenRouter
    try:
        res = requests.get(
            f"{BASE_URL}/models",
            headers={"Authorization": f"Bearer {API_KEY}"}
        )
        res.raise_for_status()
        available_models = {model["id"] for model in res.json()['data']}
    except Exception as e:
        print(f"[ERROR] Could not fetch model list from OpenRouter: {e}")
        SELECTED_MODEL = FALLBACK_MODELS[0]
        return SELECTED_MODEL

    for model_id in FALLBACK_MODELS:
        if model_id in available_models:
            print(f"[INFO] Trying to ping model: {model_id}")
            if ping_model(model_id):
                SELECTED_MODEL = model_id
                save_cached_model(model_id)
                return model_id

    # Fallback
    SELECTED_MODEL = FALLBACK_MODELS[0]
    print(f"[WARNING] No valid models passed ping. Falling back to: {SELECTED_MODEL}")
    return SELECTED_MODEL
