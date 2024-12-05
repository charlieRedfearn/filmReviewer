from flask import render_template, flash, redirect, url_for, request, jsonify
from app import app, db, models, admin, bcrypt, login_manager
from flask_admin.contrib.sqla import ModelView
from .models import User, Film, Genre, Review, Like
from .forms import LoginForm, RegisterForm
from flask_login import UserMixin, login_user, login_required, logout_user, current_user
import json

admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Film, db.session))
admin.add_view(ModelView(Genre, db.session))
admin.add_view(ModelView(Review, db.session))
admin.add_view(ModelView(Like, db.session))

login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html', title='Home')

@app.route('/account')
def account():
    user_reviews = []
    if current_user.is_authenticated:
        user_reviews = Review.query.filter_by(user_id=current_user.id).all()
    return render_template('account.html', user=current_user, reviews=user_reviews, title='account')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('home'))
    return render_template('login.html', form=form, title='login')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('register.html',form=form)

@app.route('/logout', methods=['GET','POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/movies')
def movies():
    movies = Film.query.all()
    return render_template('movies.html', movies = movies, title='movies')

@app.route('/api/films', methods=['GET'])
def get_films():
    # Get query parameters for filtering and sorting
    sort_by = request.args.get('sort_by', 'title')
    order = request.args.get('order', 'asc')
    genre = request.args.get('genre')

    # Query the films
    query = Film.query
    if genre:
        query = query.join(Film.genres).filter(Genre.name == genre)
    
    if order == 'desc':
        query = query.order_by(db.desc(getattr(Film, sort_by)))
    else:
        query = query.order_by(getattr(Film, sort_by))

    films = query.all()
    response = []
    for film in films:
        response.append({
            'id': film.id,
            'title': film.title,
            'release_year': film.release_year,
            'description': film.description,
            'reviews': [{
                'id': review.id,
                'content': review.content,
                'rating': review.rating,
                'username': review.author.username, 
                'likes_count': review.likes_count,
            }for review in film.reviews]
        })
    return jsonify(response)

@app.route('/api/reviews', methods=['POST'])
@login_required
def submit_review():
    data = request.json
    film_id = data.get('film_id')
    content = data.get('content')
    rating = data.get('rating')

    # Save the review
    review = Review(
        user_id=current_user.id,
        film_id=film_id,
        content=content,
        rating=rating
    )
    db.session.add(review)
    db.session.commit()

    return jsonify({
        'id': review.id,
        'content': review.content,
        'rating': review.rating,
        'likes_count': review.likes_count,
        'username': current_user.username
    })

@app.route('/api/reviews/<int:review_id>/like', methods=['POST'])
@login_required
def like_review(review_id):
    #query to see whether current_user has already liked this review, send flash message back
    liked = False
    like_exists = Like.query.filter_by(user_id=current_user.id, review_id=review_id).first()
    if like_exists:
        return jsonify({'liked': liked})
    else:
        review = Review.query.get_or_404(review_id)
        review.likes_count += 1
        like = Like(user_id=current_user.id, review_id=review_id)
        db.session.add(like)
        db.session.commit()
        liked=True
        return jsonify({'likes_count': review.likes_count, 'liked': liked})

@app.route('/api/reviews/<int:review_id>/unLike', methods=['POST'])
@login_required
def unLike_review(review_id):
    unLiked = False
    like_to_delete = Like.query.filter_by(user_id=current_user.id, review_id=review_id).first()
    if like_to_delete:
        review = Review.query.get_or_404(review_id)
        review.likes_count -= 1
        db.session.delete(like_to_delete)
        db.session.commit()
        unLiked = True
        return jsonify({'likes_count': review.likes_count, 'unLiked': unLiked})
    else:
        return jsonify({'unLiked': unLiked})

