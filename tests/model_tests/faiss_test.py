# Inside your tests/faiss_tests/ folder, create a file called test_faiss_model.py
import pytest
from backend.models.faiss_model import initialize_faiss_index, search_similar_foods  # adjust the import according to your actual file structure

def test_initialize_faiss_index():
    sample_data = [[0.1, 0.2], [0.4, 0.2], [0.1, 0.3]]
    sample_data_np = np.array(sample_data).astype('float32')
    index = initialize_faiss_index(sample_data_np)
    
    assert index.ntotal == 3  # Check if index size is correct
    assert index.d == 2  # Check if dimension is correct

def test_search_similar_foods():
    sample_data = [[0.1, 0.2], [0.4, 0.2], [0.1, 0.3]]
    sample_data_np = np.array(sample_data).astype('float32')
    index = initialize_faiss_index(sample_data_np)
    
    query = np.array([[0.1, 0.2]]).astype('float32')
    D, I = search_similar_foods(query, index)
    
    assert I[0][0] == 0  # Check if the first closest point is the point itself
    assert len(I[0]) == 3  # Check if it returns 3 neighbors
