from flask import Flask,Blueprint
from src import apis
import pkgutil
from src.app.app import create_flask_app,db
from src.app.config import app_config

def register_apis(flask_app: Flask) -> None:
    """Registers all APIs for Flask app.
    
    Parameters:
    -----------
        flask_app (Flask): The Flask application instance to which the 
                           blueprints will be registered.
    """
    for loader, module_name, _ in pkgutil.walk_packages(apis.__path__):
        for blueprint in loader.find_module(module_name).load_module(module_name).__dict__.values():
            if isinstance(blueprint, Blueprint):
                flask_app.register_blueprint(blueprint)

#Defining the environment to be used
environment = 'development'  # or 'production'

# Ensure that the environment key exists in app_config
if environment not in app_config:
    raise ValueError(f"Invalid environment '{environment}'. Expected one of {list(app_config.keys())}.")

#Fetching the configuration based on environment
config = app_config[environment]()  

#Creating flask app based on configuration
app = create_flask_app(config=config)

# Register all APIs (discover Blueprint definitions in API modules)
register_apis(app)