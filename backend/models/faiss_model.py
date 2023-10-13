import faiss
import numpy as np

def initialize_faiss_index(data_np):
    try:
        dimension = data_np.shape[1]
        index = faiss.IndexFlatL2(dimension)
        index.add(data_np)
        return index
    except Exception as e:
        print(f"Error initializing FAISS index: {e}")
        return None

def search_similar_foods(query, index, k=5):
    try:
        D, I = index.search(query, k)
        return D, I
    except Exception as e:
        print(f"Error searching similar foods: {e}")
        return None, None
