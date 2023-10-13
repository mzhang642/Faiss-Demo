from flask import Flask
from backend.api.routes import search_route

app = Flask(__name__)

# Register the search route
app.register_blueprint(search_route, url_prefix='/api')

if __name__ == "__main__":
    app.run(debug=True)

