from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from urls import urls

app = Flask(__name__)
app.register_blueprint(urls)
database = 'database'
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://testdbuser:testdbpass@{database}:5432/testdb'
db = SQLAlchemy(app)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5005, debug=True)
