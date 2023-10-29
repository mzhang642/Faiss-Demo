from flask import Flask, current_app
from flask_cors import CORS
from backend.utils.load_config import load_config
from backend.api.routes.search_route import search_route
from backend.api.routes.fuzzy_matching_route import fuzzy_matching_route
from backend.models.data_preprocessor import load_data_from_s3, normalize_data, convert_to_numpy
from backend.models.faiss_model import initialize_faiss_index
from backend.models.elastic_search import initialize_elasticsearch
import logging


def create_app():
    app = Flask(__name__)

    # Initialize CORS with app instance
    CORS(app)  

    # Initialize logging
    logging.basicConfig(level=logging.DEBUG)

    try:
        # Load configuration
        config = load_config()
    except Exception as e:
        logging.error(f"Failed to load config: {e}")
        raise

    with app.app_context():
        try:
            # Load data 
            current_app.df = load_data_from_s3(config['s3_bucket_name'], config['s3_object_name'])
            # Initialize ElasticSearch index (for fuzzy matching)
            current_app.es = initialize_elasticsearch(current_app.df, config['elasticsearch_host'])
            logging.debug(f"Initialized ES index: {current_app.es}")
        except Exception as e:
            logging.error(f"Failed to initialize ES index: {e}")
            
        try:
            # Initialize Faiss index
            df_normalized, _ = normalize_data(current_app.df, config['nutritional_columns'])
            current_app.data_np = convert_to_numpy(df_normalized, config['nutritional_columns'])
            current_app.index = initialize_faiss_index(current_app.data_np)
            logging.debug(f"Initialized FAISS index: {current_app.index}")
        except Exception as e:
            logging.error(f"Failed to initialize FAISS index: {e}")
            raise

    # Register blueprints
    app.register_blueprint(search_route, url_prefix='/api')
    app.register_blueprint(fuzzy_matching_route, url_prefix='/api')

    @app.route("/")
    def index():
        return "Hello, this is Faiss-Demo!"

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
