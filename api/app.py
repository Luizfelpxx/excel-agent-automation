import os
from flask import Flask, jsonify
from flask_cors import CORS
from config import config
from models import db
from routes import api_bp

def create_app(config_name=None):
    """Factory para criar a aplicação Flask"""
    
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')
    
    app = Flask(__name__)
    
    # Carregar configuração
    app.config.from_object(config[config_name])
    
    # Inicializar extensões
    db.init_app(app)
    CORS(app)
    
    # Registrar blueprints
    app.register_blueprint(api_bp)
    
    # Criar tabelas
    with app.app_context():
        db.create_all()
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Endpoint não encontrado'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return jsonify({'error': 'Erro interno do servidor'}), 500
    
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({'error': 'Requisição inválida'}), 400
    
    return app


if __name__ == '__main__':
    app = create_app()
    
    # Configurações de execução
    host = os.getenv('API_HOST', 'localhost')
    port = int(os.getenv('API_PORT', 5000))
    debug = os.getenv('FLASK_ENV', 'development') == 'development'
    
    print(f"\n{'='*50}")
    print(f"🚀 Excel Agent Automation API")
    print(f"{'='*50}")
    print(f"Server: http://{host}:{port}")
    print(f"Environment: {os.getenv('FLASK_ENV', 'development')}")
    print(f"Debug: {debug}")
    print(f"{'='*50}\n")
    
    app.run(host=host, port=port, debug=debug)