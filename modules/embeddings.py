# =======================
# modules/embeddings.py
# =======================
from sentence_transformers import SentenceTransformer
import numpy as np
import faiss

# Load embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')

def create_index(logs):
    """Create a FAISS index for log embeddings"""
    embeddings = model.encode(logs['message'].tolist(), show_progress_bar=False)
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(np.array(embeddings).astype('float32'))
    return index, embeddings

def query_index(index, model, query, logs, k=5):
    """Retrieve top-k most relevant logs for a given query"""
    query_embedding = model.encode([query])
    distances, indices = index.search(np.array(query_embedding).astype('float32'), k)
    top_logs = logs.iloc[indices[0]]
    return top_logs



