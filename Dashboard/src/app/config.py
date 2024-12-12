from abc import ABC
import os

class Config(ABC):
    """Base configuration class."""

    # General
    CSRF_ENABLED = True

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Providing local Database information to SQLALCHEMY 
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql+psycopg2://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@"
        f"{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT', '5432')}/"
        f"{os.getenv('POSTGRES_DB')}"
    )

class DevelopmentConfig(Config):
    """Development configuration class."""
    DEBUG = True

class ProductionConfig(Config):
    """Production configuration class."""
    DEBUG = False

app_config = {"development": DevelopmentConfig, "production": ProductionConfig}