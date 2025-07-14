import streamlit as st
from search_agent import semantic_search
from session_agent import store_user_query, get_personalized_keywords
from llm_agent import rerank_results

st.title("🛒 GroceryGPT+")

query = st.text_input("What are you looking for today?")
if query:
    store_user_query(query)
    results = semantic_search(query)
    st.write("### Raw Results:")
    for res in results:
        st.markdown(f"- **{res['name']}**")

    st.write("### Personalized Re-ranking with LLM:")
    with st.spinner("Re-ranking results..."):
        reranked = rerank_results(query, results)
    st.markdown(reranked)

st.write("### 📈 Based on your history, you might like:")
for kw in get_personalized_keywords():
    st.markdown(f"- {kw}")