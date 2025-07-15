from app.search_agent import create_schema, ingest_data, semantic_search

# Only run these once
# create_schema()
ingest_data()

# Then use semantic search freely
results = semantic_search("organic almond milk")

print(results)
