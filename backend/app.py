from flask import Flask, jsonify, request
from flask_cors import CORS
from extentions import db
from models import (
    Farmer,
    Crop,
    Market,
    MarketPrice,
    Recommendation
)
from routes.market_routes import market_bp

from config import Config



def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.register_blueprint(market_bp)
    
    db.init_app(app)
    
    CORS(app)
    
    @app.get("/api/health")
    def health():
        return jsonify({
            "message": "KrishiShell backend is unning"
        }), 200
        
    # @app.route("/api/crops", methods=["GET"])
    # def crops():
    #     data = request.get_json()
    #     id = data.id
        
    #     crop = Crop.query.filter_by(
    #         id=id
    #     ).first()
        
    #     if not crop:
    #         return jsonify("error": "crop not found")
        
    with app.app_context():
        db.create_all()
        
    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)