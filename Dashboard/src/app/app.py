from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from flask import Flask

# Initialize SQLAlchemy instance with required configuration
db: SQLAlchemy = SQLAlchemy(
    metadata=MetaData(
        naming_convention={
            "ck": "ck_%(table_name)s_%(constraint_name)s",
            "pk": "pk_%(table_name)s",
        }
    ),
)

# Initialize the Flask-Migrate extension for handling database migrations
migrate: Migrate = Migrate()

def create_flask_app(config) -> Flask:
    """
    Create and configure a Flask application instance.

    Parameters
    ----------
    config: str
        The configuration class to use for the Flask application. 

    Returns
    -------
    Flask:
        An instance of the Flask application with the specified configuration applied.
    """

    #Initialize a Flask application instance.
    flask_app = Flask(import_name=__name__, instance_relative_config=True)

    #Load configuration settings into the Flask app 
    flask_app.config.from_object(obj=config)
    
    # Initialize SQLAlchemy instance with created flask app
    db.init_app(app=flask_app)

    #Initialize the Flask-Migrate instance with created flask app
    migrate.init_app(app=flask_app, db=db)

    return flask_app


    