import os

from flask import Flask
from flask_security import (
    Security,
    SQLAlchemyUserDatastore,
    auth_required,
    hash_password,
)
from flask_security.models import fsqla_v2 as fsqla
from flask_sqlalchemy import SQLAlchemy

import folium

KANOP_COORDS = (48.83505261412694, 2.37097587670811)
EMAIL = os.environ["EMAIL"]
PASSWORD = os.environ["PASSWORD"]

app = Flask(__name__)
app.config["DEBUG"] = True

# Generate a nice key using secrets.token_urlsafe()
app.config["SECRET_KEY"] = os.environ["SECRET_KEY"]

# Bcrypt is set as default SECURITY_PASSWORD_HASH, which requires a salt
# Generate a good salt using: secrets.SystemRandom().getrandbits(128)
app.config["SECURITY_PASSWORD_SALT"] = os.environ["SECURITY_PASSWORD_SALT"]

# Use an in-memory db
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"
# As of Flask-SQLAlchemy 2.4.0 it is easy to pass in options directly to the
# underlying engine. This option makes sure that DB connections from the
# pool are still valid. Important for entire application since
# many DBaaS options automatically close idle connections.
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_pre_ping": True,
}
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Create database connection object
db = SQLAlchemy(app)

# Define models
fsqla.FsModels.set_db_info(db)


class Role(db.Model, fsqla.FsRoleMixin):
    pass


class User(db.Model, fsqla.FsUserMixin):
    pass


# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

# Create a user to test with
@app.before_first_request
def create_user():
    db.create_all()
    if not user_datastore.find_user(email=EMAIL):
        user_datastore.create_user(email=EMAIL, password=hash_password(PASSWORD))
    db.session.commit()


@app.route("/")
@auth_required()
def index():
    folium_map = folium.Map(location=KANOP_COORDS, zoom_start=14)
    folium.Marker(
        location=KANOP_COORDS,
        popup="Kanop",
    ).add_to(folium_map)
    return folium_map._repr_html_()
