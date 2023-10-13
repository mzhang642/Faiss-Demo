from flask import Blueprint, request, jsonify
# Import other modules or utility functions you need
from backend.models import search_similar_foods, initialize_faiss_index
from backend.utils import load_data_from_s3, normalize_data

search_route = Blueprint('search', __name__)

# Assuming you've initialized FAISS index elsewhere or here
index = None

@search_route.route('/search', methods=['POST'])
def search():
    global index
    if index is None:
        # Load and preprocess your data, then initialize the FAISS index
        df = load_data_from_s3(...) 
        df_normalized, _ = normalize_data(df)
        index = initialize_faiss_index(df_normalized)

    query_data = request.json.get('query_data', [])
    # Perform the actual search
    D, I = search_similar_foods(np.array(query_data), index)
    
    # Return results
    return jsonify({"distances": D.tolist(), "indices": I.tolist()})
