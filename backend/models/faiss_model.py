import faiss
import numpy as np
import logging

def initialize_faiss_index(data_np):
    try:
        data_np = np.ascontiguousarray(data_np)  # Ensure C-contiguous layout
        dimension = data_np.shape[1]
        index = faiss.IndexFlatL2(dimension)
        index.add(data_np)
        return index
    except Exception as e:
        print(f"Error initializing FAISS index: {e}")
        return None

def search_similar_foods(query, index, k=5):
    try:
        logging.debug(f"Query data shape: {query.shape}")
        logging.debug(f"Query data type: {query.dtype}")

        D, I = index.search(query, k)

        logging.debug(f"Distances: {D}")
        logging.debug(f"Indices: {I}")

        return D, I
    except Exception as e:
        print(f"Error searching similar foods: {e}")
        return None, None
