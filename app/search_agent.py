import pandas as pd
import uuid
import weaviate
from sentence_transformers import SentenceTransformer
from tqdm import tqdm
import os

client = weaviate.Client(
    url=os.getenv("WEAVIATE_URL"), 
    auth_client_secret=weaviate.AuthApiKey(os.getenv("WEAVIATE_API_KEY")),
    additional_headers={} # To use built-in vectorization modules set "X-OpenAI-Api-Key": os.getenv("OPENAI_API_KEY")
    )

model = SentenceTransformer('all-MiniLM-L6-v2')  # For text search

def create_schema():
    existing = client.schema.get()
    existing_classes = [cls["class"] for cls in existing["classes"]]

    if "Product" not in existing_classes:
        class_obj = {
            "class": "Product",
            "vectorizer": "none",
            "properties": [
                {"name": "name", "dataType": ["text"]},
                {"name": "description", "dataType": ["text"]},
            ]
        }
        client.schema.create_class(class_obj)
        print("✅ Created 'Product' class schema.")
    else:
        print("✅ 'Product' schema already exists.")

def ingest_data(progress_bar=True, batch_size=100):
    df = pd.read_csv('data/products_cleaned.csv')

    # Filter out already-ingested product UUIDs
    print("🔍 Checking existing products...")
    existing_uuids = set()
    for _, row in df.iterrows():
        uid = str(uuid.uuid5(uuid.NAMESPACE_DNS, str(row["product_id"])))
        if client.data_object.exists(uid):
            existing_uuids.add(uid)
    print(f"✅ Found {len(existing_uuids)} existing products.")

    df = df[~df["product_id"].apply(lambda pid: str(uuid.uuid5(uuid.NAMESPACE_DNS, str(pid))) in existing_uuids)]
    
    if df.empty:
        print("✅ All products already ingested.")
        return

    iterator = tqdm(df.iterrows(), total=len(df), desc="Batch Ingesting") if progress_bar else df.iterrows()

    print(f"⏳ Ingesting {len(df)} new products...")
    with client.batch(batch_size=batch_size) as batch:
        for _, row in iterator:
            uid = str(uuid.uuid5(uuid.NAMESPACE_DNS, str(row["product_id"])))
            vector = model.encode(row['full_text'])
            data_obj = {
                "name": row['product_name'],
                "description": row['full_text']
            }
            batch.add_data_object(data_obj, "Product", uuid=uid, vector=vector)

    print(f"✅ Ingested {len(df)} new products.")

def semantic_search(query, top_k=5):
    vector = model.encode(query)
    result = client.query.get("Product", ["name", "description"]) \
        .with_near_vector({"vector": vector.tolist()}) \
        .with_limit(top_k).do()
    return result["data"]["Get"]["Product"]

# Optional runner
if __name__ == "__main__":
    print("Creating schema...")
    create_schema()
    print("Ingesting data...")
    ingest_data(progress_bar=True)
    print("✅ Done.")