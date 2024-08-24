import os, time
from datetime import timedelta

from flask import Flask
from dotenv import load_dotenv
from .extensions import prepare_extensions, celery_init_app

load_dotenv()
app = Flask(__name__)
db = prepare_extensions(app)

def create_app(db_uri=f"postgresql+psycopg2://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"):

    app.config['SECRET_KEY'] = os.getenv('APP_SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    
    prepare_directories(app)
    prepare_blueprints(app)
    prepare_database(app)
    
    celery_app = prepare_celery(app)
    
    return app, celery_app


def prepare_celery(app):
    app.config.from_mapping(
        CELERY=dict(
                broker_url=os.getenv('CELERY_BROKER'),
                result_backend=os.getenv('CELERY_RESULT_BACKEND'),
                task_ignore_result=False,
                task_track_started=True,
                task_serializer="json",
                result_serializer="json",
                accept_content=["json"]
            ),
    )
    celery_app = celery_init_app(app)
    
    return celery_app


def prepare_directories(app):
    # app directories
    app.config['STATIC_DIR'] = os.path.join(app.root_path, 'static')
    
    
def prepare_blueprints(app):
    # initializing blueprints
    from src.routes.tests import tests
    
    app.register_blueprint(tests, url_prefix='/tests/')
    

def prepare_database(app):
    db.init_app(app)
    # creates the models in the specified database
    with app.app_context():
        db.create_all()
        print('Database created successfully!')