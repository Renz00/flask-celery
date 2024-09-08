import os, time
from datetime import timedelta

from flask import Flask
from dotenv import load_dotenv
from .extensions import prepare_extensions, celery_init_app

load_dotenv()
app = Flask(__name__)
db = prepare_extensions(app)

def create_app(db_uri=f"postgresql+psycopg2://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_HOST')}/{os.getenv('POSTGRES_DB')}"):

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
        from .models import User, Post
        db.create_all()
        try: # will fail after 2nd build because database data persists
            new_user1 = User(email='renz@gmail.com')
            new_user2 = User(email='may@gmail.com')
            db.session.add(new_user1)
            db.session.add(new_user2)
            new_post1 = Post(title='Test Post 1', user_id=1)
            new_post2 = Post(title='Test Post 2', user_id=1)
            new_post3 = Post(title='Test Post 3', user_id=2)
            db.session.add(new_post1)
            db.session.add(new_post2)
            db.session.add(new_post3)
            db.session.commit()
        except:
            pass
        print('Database created successfully!')