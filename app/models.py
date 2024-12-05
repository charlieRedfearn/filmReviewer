from app import db
from flask_login import UserMixin

# association table for genres
film_genres = db.Table(
    'film_genres',
    db.Column('film_id', db.Integer, db.ForeignKey('films.id', ondelete="CASCADE"), primary_key=True),
    db.Column('genre_id', db.Integer, db.ForeignKey('genres.id', ondelete="CASCADE"), primary_key=True)
)

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    # Relationships
    reviews = db.relationship('Review', back_populates='author', cascade="all, delete-orphan")
    likes = db.relationship('Like', back_populates='user', cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User {self.username}>"

class Film(db.Model):
    __tablename__ = 'films'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    release_year = db.Column(db.Integer, nullable=True)

    # Relationships
    genres = db.relationship('Genre', secondary=film_genres, back_populates='films')
    reviews = db.relationship('Review', back_populates='film', cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Film {self.title}>"

class Genre(db.Model):
    __tablename__ = 'genres'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    # Relationships
    films = db.relationship('Film', secondary=film_genres, back_populates='genres')

    def __repr__(self):
        return f"<Genre {self.name}>"

class Review(db.Model):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    likes_count = db.Column(db.Integer, default=0)

    # Foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="CASCADE"), nullable=False)
    film_id = db.Column(db.Integer, db.ForeignKey('films.id', ondelete="CASCADE"), nullable=False)

    # Relationships
    author = db.relationship('User', back_populates='reviews')
    film = db.relationship('Film', back_populates='reviews')
    likes = db.relationship('Like', back_populates='review', cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Review {self.content[:30]} by User {self.user_id}>"

class Like(db.Model):
    __tablename__ = 'likes'

    id = db.Column(db.Integer, primary_key=True)

    # Foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="CASCADE"), nullable=False)
    review_id = db.Column(db.Integer, db.ForeignKey('reviews.id', ondelete="CASCADE"), nullable=False)

    # Relationships
    user = db.relationship('User', back_populates='likes')
    review = db.relationship('Review', back_populates='likes')

    def __repr__(self):
        return f"<Like by User {self.user_id} on Review {self.review_id}>"