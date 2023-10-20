from flask import Flask, current_app
from flask_cors import CORS
from backend.api.routes.search_route import search_route
from backend.utils.load_config import load_config
from backend.models.data_preprocessor import load_data_from_s3, normalize_data, convert_to_numpy
from backend.models.faiss_model import initialize_faiss_index
import logging


def create_app():
    app = Flask(__name__)
    CORS(app)  # Initialize CORS with app instance

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
            # Load data and initialize FAISS index
            current_app.df = load_data_from_s3(config['s3_bucket_name'], config['s3_object_name'])
            df_normalized, _ = normalize_data(current_app.df, config['nutritional_columns'])
            current_app.data_np = convert_to_numpy(df_normalized, config['nutritional_columns'])
            current_app.index = initialize_faiss_index(current_app.data_np)
            logging.debug(f"Initialized FAISS index: {current_app.index}")
        except Exception as e:
            logging.error(f"Failed to initialize FAISS index: {e}")
            raise

    # Register blueprints
    app.register_blueprint(search_route, url_prefix='/api')

    @app.route("/")
    def index():
        return "Hello, this is Faiss-Demo!"

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
