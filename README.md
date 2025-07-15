---
title: "GroceryGPT+"
emoji: "🛒"
colorFrom: "blue"
colorTo: "green"
sdk: streamlit
sdk_version: "1.32.2"
app_file: app/streamlit_app.py
pinned: false
---


# 🛒 GroceryGPT+ — Personalized Grocery Search Engine with LLM Reranking

[![Built with Streamlit](https://img.shields.io/badge/Built%20with-Streamlit-red?logo=streamlit)](https://streamlit.io)
[![Weaviate Vector DB](https://img.shields.io/badge/VectorDB-Weaviate-blue?logo=weaviate)](https://weaviate.io)
[![Powered by OpenRouter](https://img.shields.io/badge/LLM-Qwen%2FMistral%2FDeepSeek-green)](https://openrouter.ai)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Hugging Face Spaces](https://img.shields.io/badge/Deployed%20on-HuggingFace-orange?logo=huggingface)](https://huggingface.co/spaces/rajesh1804/grocerygpt)

> 🚀 **GroceryGPT+** is a smart, real-time product search app combining **semantic vector search** with **LLM-powered reranking** and **personalized recommendations** — all production-ready.

---

## 🔧 Features

✅ **Semantic Text Search** using Sentence Transformers  
✅ **LLM-Powered Reranking** using Qwen/Mistral/DeepSeek (via OpenRouter)  
✅ **Model Fallback System** with latency tracking & cache  
✅ **Streamlit UI** for seamless interaction  
✅ **Personalized Suggestions** using session memory  
✅ **CLI for Schema Creation + Batch Ingestion**  
✅ **Production-ready structure** with modular components

---

## 🖼️ Architecture Overview

<p align="center">
  <img src="assets/architecture.png" alt="Architecture" width="600"/>
</p>

---

## 🧪 Example Flow

1. User enters: _"vegan cereal under 200 calories"_
2. MiniLM embeds query → searches Weaviate for top matches
3. LLM reranks results based on user intent
4. Final output shown with raw + reranked sections
5. Session saves the query → influences future recommendations

---

## 📽️ Live Demo

👉 Try it on [Hugging Face](https://huggingface.co/spaces/rajesh1804/grocerygpt)

<p align="center">
  <img src="assets/grocerygpt-demo.webp" alt="Demo" width="600"/>
</p>

---

## 🚀 Getting Started

### 1. Clone & Setup

```bash
git clone https://github.com/rajesh1804/grocerygpt.git
cd grocerygpt
pip install -r requirements.txt
```

### 2. Create .env

```bash
OPENROUTER_API_KEY=your-api-key-here
```

### 3. Start Weaviate (Docker)

```bash
docker run -d -p 8080:8080 semitechnologies/weaviate:latest
```

### 4. Ingest Products (once)

```bash
python search_agent.py
```

### 5. Run the App

```bash
streamlit run main.py
```

---

## 📁 Project Structure

<p align="center">
  <img src="assets/project_structure.png" alt="Project Structure" width="600"/>
</p>

---

## 🧪 Tech Stack

- **Frontend**: [Streamlit](https://streamlit.io/) for interactive UI
- **Vector DB**: [Weaviate](https://weaviate.io/) for semantic product search
- **Embeddings**: [Sentence Transformers](https://www.sbert.net/) for encoding text
- **LLM Reranking**: OpenRouter API with fallback support for:
  - Qwen 3.14B (Free)
  - Mistral 7B Instruct (Free)
  - DeepSeek Chat v3 (Free)
- **Caching**: File-based cache for selected model
- **Logging**: Latency & error reporting in console
- **Personalization**: Query history-based keyword memory

---

## 📝 License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for more details.
