from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from urls import urls
import os
from dotenv import load_dotenv

load_dotenv()

user = os.getenv('POSTGRES_USER')
password = os.getenv('POSTGRES_PASSWORD')
host = os.getenv('POSTGRES_HOST')
port = os.getenv('POSTGRES_PORT')
data_base_name = os.getenv('POSTGRES_DB')

app = Flask(__name__)
app.register_blueprint(urls)

app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{user}:{password}@{host}:{port}/{data_base_name}'
db = SQLAlchemy(app)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5005, debug=True)
