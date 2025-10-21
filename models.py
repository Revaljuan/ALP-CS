from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password_hash = db.Column(db.String, nullable=True)
    role = db.Column(db.String, default='user')  # admin / manager / user
    department = db.Column(db.String, default='general')
    subscription_active = db.Column(db.Boolean, default=False)
    google_sub = db.Column(db.String, nullable=True)

    def set_password(self, pw):
        self.password_hash = generate_password_hash(pw)

    def check_password(self, pw):
        if not self.password_hash:
            return False
        return check_password_hash(self.password_hash, pw)

    def to_dict(self):
        return dict(id=self.id, username=self.username, role=self.role,
                    department=self.department, subscription_active=self.subscription_active)

class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    content = db.Column(db.String)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    department = db.Column(db.String, default='general')
    premium = db.Column(db.Boolean, default=False)

    def to_dict(self):
        return dict(id=self.id, title=self.title, owner_id=self.owner_id,
                    department=self.department, premium=self.premium)

def seed_data(db):
    if User.query.first():
        return

    admin = User(username='admin', role='admin', department='IT', subscription_active=True)
    admin.set_password('adminpass')

    manager = User(username='manager', role='manager', department='Sales', subscription_active=True)
    manager.set_password('managerpass')

    alice = User(username='alice', role='user', department='Sales', subscription_active=False)
    alice.set_password('alicepass')

    bob = User(username='bob', role='user', department='IT', subscription_active=True)
    bob.set_password('bobpass')

    db.session.add_all([admin, manager, alice, bob])
    db.session.commit()

    doc1 = Document(title='Sales Plan', content='Q4 plan', owner_id=manager.id, department='Sales', premium=False)
    doc2 = Document(title='IT Secret', content='Server configs', owner_id=admin.id, department='IT', premium=True)
    db.session.add_all([doc1, doc2])
    db.session.commit()
