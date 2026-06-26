import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configuração base"""
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_SORT_KEYS = False
    
class DevelopmentConfig(Config):
    """Configuração de desenvolvimento"""
    DEBUG = True
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///machines.db')
    FLASK_ENV = 'development'
    
class ProductionConfig(Config):
    """Configuração de produção"""
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///machines.db')
    FLASK_ENV = 'production'
    
class TestingConfig(Config):
    """Configuração de testes"""
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    FLASK_ENV = 'testing'

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}