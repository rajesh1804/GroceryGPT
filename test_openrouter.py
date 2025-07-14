import requests
import os
from pprint import pprint

API_KEY = os.getenv("OPENROUTER_API_KEY")

res = requests.get(
    "https://openrouter.ai/api/v1/models",
    headers={"Authorization": f"Bearer {API_KEY}"}
)

models = res.json()

for model in models['data']:
    pprint(f"Model ID: {model['id']}")
    # if model['id'] == 'mistralai/mistral-7b-instruct':
    #     print(f"Model ID: {model['id']}")
    #     print(f"Description: {model['description']}")
    #     # print(f"Max Tokens: {model['max_tokens']}")
    #     # print(f"Supports Streaming: {model['supports_streaming']}")
    #     # print(f"Supports Fine-tuning: {model['supports_fine_tuning']}")
    #     pprint(model)
