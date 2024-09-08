import os
from src import create_app

from dotenv import load_dotenv
load_dotenv()

app, celery_app = create_app() # access the celery_app using this file

app.app_context().push() # allow celery_app to access app context

if __name__ == '__main__':
    app.run(debug=os.getenv('DEBUG'), host=os.getenv('APP_HOST'), port=os.getenv('APP_PORT'))