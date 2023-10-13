from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
CORS(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://othrknqc:U8CWFuHYH2Y4EArAtRsrn6FdbBBMSKxU@rain.db.elephantsql.com/othrknqc"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
app.app_context().push()

# @app.route('/')
# def hello():
#     return 'My First API !!'
