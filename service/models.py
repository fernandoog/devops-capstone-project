"""
Account Model
"""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class Account(db.Model):
    """
    Account Model
    """
    __tablename__ = 'accounts'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    address = db.Column(db.String(200), nullable=True)
    phone_number = db.Column(db.String(20), nullable=True)
    date_joined = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Account {self.name}>'

    def serialize(self):
        """Serialize account to a dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'address': self.address,
            'phone_number': self.phone_number,
            'date_joined': self.date_joined.isoformat() if self.date_joined else None
        }

    def deserialize(self, data):
        """Deserialize account from a dictionary"""
        try:
            self.name = data.get('name')
            self.email = data.get('email')
            self.address = data.get('address')
            self.phone_number = data.get('phone_number')
        except KeyError as error:
            raise ValueError(f"Invalid account: missing {error}")
        except TypeError:
            raise ValueError("Invalid account: body of request contained bad or no data")
        return self

    def save(self):
        """Save account to database"""
        db.session.add(self)
        db.session.commit()

    def update(self):
        """Update account in database"""
        db.session.commit()

    def delete(self):
        """Delete account from database"""
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def all(cls):
        """Return all accounts"""
        return cls.query.all()

    @classmethod
    def find(cls, account_id):
        """Find account by ID"""
        return cls.query.get(account_id)

    @classmethod
    def find_by_email(cls, email):
        """Find account by email"""
        return cls.query.filter_by(email=email).first()
