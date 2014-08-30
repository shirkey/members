import uuid

from sqlalchemy.event import listens_for

from users.database import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    guid = db.Column(db.String(37), nullable=False, unique=True)
    name = db.Column(db.String(32), nullable=False)
    email = db.Column(db.String(254), nullable=False)
    website = db.Column(db.String(255), default="")
    email_updates = db.Column(db.Boolean(name="email_updates"),
                              default=False)
    date_added = db.Column(db.TIMESTAMP,
                           server_default=db.text("CURRENT_TIMESTAMP"))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)

    # one-to-one relationship
    social_account = db.relationship("SocialAccount",
                                     uselist=False,
                                     backref="user")


class SocialAccount(db.Model):
    __tablename__ = "social_accounts"

    id = db.Column(db.Integer, primary_key=True)
    guid = db.Column(db.Integer, db.ForeignKey("users.guid"))
    twitter = db.Column(db.String(15))


@listens_for(User, "before_insert")
def before_add_user(mapper, connection, target):
    target.guid = "{guid}".format(guid=uuid.uuid4())


@listens_for(User, "load")
def on_user_loaded(target, context):
    target.email_updates = 0 if not target.email_updates else 1


"""
def add_user(user_data):

    add_user(
        name=user_data.get('name'),
        email=user_data.get('email'),
        website=user_data.get('website'),
        longitude=user_data.get('longitude'),
        latitude=user_data.get('latitude'),
        email_updates=user_data.get('email_updates'),
        social_account=user_data.get('social_account')
    )
"""

def add_user(name, email, website, latitude, longitude,
             email_updates=False, social_account=None):
    social_account = social_account or {}

    user = User()
    user.name = name
    user.email = email
    user.website = website
    user.latitude = float(latitude)
    user.longitude = float(longitude)
    user.email_updates = bool(email_updates)

    models = [user]

    if social_account:
        account = SocialAccount()
        account.twitter = social_account.get("twitter", '')
        user.social_account = account
        models.append(account)

    db.session.add_all(models)
    db.session.commit()
    return user.guid


def edit_user(guid, name, email, website, latitude, longitude,
              email_updates, social_account=None):
    social_account = social_account or {}
    User.query.filter(User.guid == guid).update({
        User.name: name,
        User.email: email,
        User.website: website,
        User.latitude: latitude,
        User.longitude: longitude,
        User.email_updates: email_updates,
    })

    if social_account:
        SocialAccount.query.filter(SocialAccount.guid == guid).update({
            SocialAccount.twitter: social_account["twitter"],
        })
    db.session.commit()
    return guid


def delete_user(guid):
    SocialAccount.query.filter(SocialAccount.guid == guid).delete()
    User.query.filter(User.guid == guid).delete()
    db.session.commit()
    return True


def get_user(guid):
    return User.query.filter(User.guid == guid).first()


def get_user_by_email(email):
    return User.query.filter(User.email == email).first()


def get_all_users():
    return User.query.all()
