import uuid

from sqlalchemy.event import listens_for

from users.database import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    guid = db.Column(db.String(37), nullable=False)
    name = db.Column(db.String(32), nullable=False)
    email = db.Column(db.String(254), nullable=False)
    website = db.Column(db.String(255), default="")
    email_updates = db.Column(db.Boolean(name="email_updates"),
                              default=False)
    date_added = db.Column(db.DateTime,
                           server_default=db.text("CURRENT_TIMESTAMP"))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)


@listens_for(User, "before_insert")
def before_add_user(mapper, connection, target):
    target.guid = "{guid}".format(guid=uuid.uuid4())
    target.email_updates = 0 if not target.email_updates else 1


@listens_for(User, "before_update")
def before_edit_user(mapper, connection, target):
    target.email_updates = 0 if not target.email_updates else 1


@listens_for(User, "load")
def on_user_loaded(target, context):
    target.email_updates = 0 if not target.email_updates else 1


def add_user(name, email, website, latitude, longitude, email_updates=False):
    user = User()
    user.name = name
    user.email = email
    user.website = website
    user.latitude = latitude
    user.longitude = longitude
    user.email_updates = email_updates

    db.session.add(user)
    db.session.commit()
    return user.guid


def edit_user(guid, name, email, website, latitude, longitude, email_updates):
    User.query.filter(User.guid == guid).update({
        User.name: name,
        User.email: email,
        User.website: website,
        User.latitude: latitude,
        User.longitude: longitude,
        User.email_updates: email_updates,
    })
    db.session.commit()
    return guid


def delete_user(guid):
    User.query.filter(User.guid == guid).delete()
    db.session.commit()
    return True


def get_user(guid):
    return User.query.filter(User.guid == guid).first()


def get_user_by_email(email):
    return User.query.filter(User.email == email).first()


def get_all_users():
    return User.query.all()
