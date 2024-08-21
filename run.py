import os
from flask_cors import CORS
from app import create_app

app = create_app()

CORS(app, resources={r"/*": {"origins": "*"}})

if __name__ == "__main__":
    port = int(os.getenv("FLASK_RUN_PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
