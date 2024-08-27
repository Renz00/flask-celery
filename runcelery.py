from src import create_app

app, celery_app = create_app()

if __name__ == '__main__':
    with app.app_context():
        celery_app.start()