import os
from src import create_app

from dotenv import load_dotenv
load_dotenv()

app, _ = create_app()

if __name__ == '__main__':
    app.run(debug=os.getenv('DEBUG'), host=os.getenv('APP_HOST'), port=os.getenv('APP_PORT'))