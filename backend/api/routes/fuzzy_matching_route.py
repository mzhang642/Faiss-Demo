from flask import Blueprint, request, jsonify, current_app
from backend.models.elastic_search import perform_fuzzy_search
import logging

fuzzy_matching_route = Blueprint('fuzzy_matching', __name__)

@fuzzy_matching_route.route('/fuzzy_matching', methods=['POST'])
def fuzzy_matching():
    es = current_app.es  # Get the ElasticSearch index from the app context

    query_data = str(request.json.get('query_data', ''))
    logging.debug(f"Received fuzzy query_data: {query_data}")

    if not query_data:
        logging.warning("Empty query_data received")
        return jsonify({"error": "Empty query data"}), 400
    
    matches = perform_fuzzy_search(es, query_data)
    
    if matches is None:
        return jsonify({"error": "An error occurred during fuzzy search"}), 500
    
    return jsonify({"matches": matches})


# curl -X POST -H "Content-Type: application/json" -d '{"query_data": "aple"}' http://127.0.0.1:5000/api/fuzzy_matching