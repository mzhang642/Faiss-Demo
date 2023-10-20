from flask import Blueprint, request, jsonify, current_app
from backend.models.faiss_model import search_similar_foods, convert_query
import numpy as np
import logging

search_route = Blueprint('search', __name__)

@search_route.route('/search', methods=['POST'])
def search():
    # Get the FAISS index from the application context
    index = current_app.index
    data_np = current_app.data_np
    
    # Log the FAISS index to verify that it's initialized correctly
    logging.debug(f"Current FAISS index: {index}")

    # Validate that the index has been initialized
    if index is None:
        logging.error("FAISS index not initialized")
        return jsonify({"error": "FAISS index not initialized"}), 500

    # the data coming from JSON could be interpreted as a different type. 
    # JSON data gets automatically parsed into Python types, but sometimes 
    # numbers can be parsed into float instead of int, especially when passed through different systems. 
    query_data = int(request.json.get('query_data', []))  
    
    # Log the incoming query_data to verify that it's what you expect
    logging.debug(f"Received query_data: {query_data}")

    # Validate that query_data is not empty or None
    if not query_data:
        logging.warning("Empty query_data received")
        return jsonify({"error": "Empty query data"}), 400
    
    # Validate that query_data is a list (assuming you are expecting a list)
    if not isinstance(query_data, int):
        logging.warning("query_data is not an index")
        return jsonify({"error": "query_data must be an index"}), 400

    try:
        # Perform the actual search

        query = convert_query(data_np, query_data)
        D, I = search_similar_foods(np.array(query, dtype=np.float32), index)

        # Return results
        return jsonify({"distances": D.tolist(), "indices": I.tolist()})
    except Exception as e:
        # Log the exception for debugging
        logging.error(f"Error during search: {e}")
        return jsonify({"error": "An error occurred during search"}), 500



#  curl -X POST -H "Content-Type: application/json" -d '{"query_data": 1}' http://127.0.0.1:5000/api/search
