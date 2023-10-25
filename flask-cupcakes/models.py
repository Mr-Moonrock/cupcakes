"""Models for Cupcake app."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
default_pic = 'https://tinyurl.com/demo-cupcake'

def connect_db(app):
    db.app = app
    db.init_app(app)

class Cupcake(db.Model):
    """ Cupcake model """

    __tablename__ = 'cupcakes'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    flavor = db.Column(db.String, nullable=False)
    size = db.Column(db.String, nullable=False)
    rating = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(4000), nullable=False, default= 'https://tinyurl.com/demo-cupcake')

    def __repr__(self):
        return f'<Cupcake id={self.id} flavor={self.flavor}>'
    
    def serialize(self):
        """ Serialize a Cupcake object to a dictionary """

        return {
            "id": self.id,
            "flavor": self.flavor,
            "size": self.size,
            "rating": self.rating,
            "image": self.image,
        }