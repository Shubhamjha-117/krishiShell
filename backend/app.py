from flask import Flask, jsonify
from flask_cors import CORS
from extentions import db
from models import (
    Farmer,
    Crop,
    Market,
    MarketPrice,
    Recommendation
)

from config import Config



def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    
    CORS(app)
    
    @app.get("/api/health")
    def health():
        return jsonify({
            "message": "KrishiShell backend is unning"
        }), 200
        
    with app.app_context():
        db.create_all()
        
    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)