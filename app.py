import os
from flask import Flask, render_template, request, flash, redirect, url_for, session, g, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from flask_bcrypt import Bcrypt
from functools import wraps
from dotenv import load_dotenv
from flask_migrate import Migrate
from fetch import fetch_all_data
from models import db, connect_db, User, Comment, Person, Film, Starship, Vehicle, Species, Planet, CommentVote, search_elements
from forms import SignUpForm, LoginForm, EditUserForm, AddCommentForm

CURR_USER_KEY = "curr_user"

load_dotenv()

app = Flask(__name__)
bcrypt = Bcrypt(app)
migrate = Migrate(app, db)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

toolbar = DebugToolbarExtension(app)
connect_db(app)

with app.app_context():
    # db.drop_all()
    db.create_all()
    # fetch_all_data()


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not g.user:
            flash('You need to be logged in to access this page!', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


@app.before_request
def load_user():
    """Load user if logged in"""
    user_id = session.get("user_id")
    if user_id:
        g.user = User.query.get(user_id)
    else:
        g.user = None
                            

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/search', methods=['GET'])
def search():
    search_query = request.args.get('query', '')

    res = search_elements(search_query)

    return jsonify(res)


# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#            User routes
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """Route to add a user to the database"""
    form = SignUpForm()
    if form.validate_on_submit():
        try:
            username = form.username.data
            email = form.email.data
            password = form.password.data

            existing_user = User.query.filter_by(username=username).first()
            existing_email = User.query.filter_by(email=email).first()

            if existing_user:
                flash('Username already exists, please choose a different one.', 'danger')
            elif existing_email:
                flash('Email address is already registered, please use a different one', 'danger')
            else:
                user = User.signup(username=username, email=email, password=password)
                db.session.add(user)
                db.session.commit()
                flash('Account created successfully!', 'success')
                return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback() 
            flash(f'An error occurred: {e}', 'danger')
    
    return render_template('/users/signup.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Route for user login"""
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            session['user_id'] = user.id
            g.user = user

            flash('Login successful!', 'success')
            print(g.user)
            return redirect(url_for('home'))
        else:
            flash('Login unsuccessful. Please check your username and password.', 'danger')

    return render_template('/users/login.html', form=form)


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    """Route to log out user"""
    session.pop('user_id', None)
    flash('You have logged out!', 'success')
    return redirect(url_for('home'))


@app.route('/profile/<int:user_id>', methods=['GET'])
@login_required
def user_profile(user_id):
    """Show user profile"""
    if g.user.id != user_id:
        flash('You do not have permission to view this profile', 'danger')
        return redirect(url_for('user_profile', user_id=g.user.id))

    user = User.query.get_or_404(user_id)
    comments_with_associations = []

    for comment in user.comments:
        associated_element = None
        if comment.person_id:
            associated_element = Person.query.get(comment.person_id)
        elif comment.film_id:
            associated_element = Film.query.get(comment.film_id)
        elif comment.starship_id:
            associated_element = Starship.query.get(comment.starship_id)
        elif comment.vehicle_id:
            associated_element = Vehicle.query.get(comment.vehicle_id)
        elif comment.species_id:
            associated_element = Species.query.get(comment.species_id)
        elif comment.planet_id:
            associated_element = Planet.query.get(comment.planet_id)

        comments_with_associations.append((comment, associated_element))

    return render_template('/users/profile.html', user=user, comments_with_associations=comments_with_associations)



@app.route('/edit/<int:user_id>', methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
    """Edit own information"""
    user = User.query.get_or_404(user_id)
    form = EditUserForm(obj=user)

    if form.validate_on_submit():
        if not bcrypt.check_password_hash(user.password, form.password.data):
            flash('Incorrect current password. Changes not saved.', 'danger')
            return redirect(url_for('edit_user', user_id=user.id))
        # Check if new username already exists
        if User.query.filter_by(username=form.username.data).first() and form.username.data != user.username:
            flash('Username already exists. Please choose a differene one.', 'danger')
            return redirect(url_for('edit_user', user_id=user.id))

        user.username = form.username.data
        user.email = form.email.data

        if form.new_password.data:
            user.password = bcrypt.generate_password_hash(form.new_password.data).decode('UTF-8')

        db.session.commit()
        flash('Your information has been updated!', 'success')
        return redirect(url_for('user_profile', user_id=user.id))
    
    return render_template('/users/edit_user.html', form=form, user=user)


@app.route('/edit/<int:user_id>/delete', methods=['POST'])
@login_required
def delete_user(user_id):
    """Delete user"""
    user = User.query.get_or_404(user_id)

    if g.user.id != user.id:
        flash('You do not have permission to delete this user.', 'danger')
        return redirect(url_for('user_profile', user_id=user.id))
    
    db.session.delete(user)
    db.session.commit()

    flash('Your account has been deleted successfully.', 'success')
    return redirect(url_for('home'))




# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#   Swapi request and render routes
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


@app.route('/characters', methods=['GET'])
def list_characters():
    """Load list of characters"""
    people = Person.query.all()
    return render_template('swapi/people_list.html', people=people)

@app.route('/characters/<int:person_id>', methods=['GET', 'POST'])
def person_detail(person_id):
    """Load details of one specific person"""
    person = Person.query.get_or_404(person_id)
    form = AddCommentForm()

    if form.validate_on_submit():
        comment = Comment(
            text=form.text.data,
            user_id=g.user.id,
            person_id=person.id
        )
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('person_detail', person_id=person.id))
    comments = Comment.query.filter_by(person_id=person.id).all()
    return render_template('swapi/person_detail.html', person=person, form=form, comments=comments)

@app.route('/films', methods=['GET'])
def list_films():
    """Load list of films"""
    films = Film.query.all()
    return render_template('swapi/films_list.html', films=films)

@app.route('/films/<int:film_id>', methods=['GET', 'POST'])
def film_detail(film_id):
    """Load details of a film"""
    film = Film.query.get_or_404(film_id)
    form = AddCommentForm()

    if form.validate_on_submit():
        comment = Comment(
            text=form.text.data,
            user_id=g.user.id,
            film_id=film.id
        )
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('film_detail', film_id=film.id))
    comments = Comment.query.filter_by(film_id=film.id).all()
    return render_template('swapi/film_detail.html', film=film, form=form, comments=comments)

@app.route('/starships', methods=['GET'])
def list_starships():
    """Load list of starships"""
    starships = Starship.query.all()
    return render_template('/swapi/starships_list.html', starships=starships)

@app.route('/starships/<int:starship_id>', methods=['GET', 'POST'])
def starship_detail(starship_id):
    """Load details of a starship"""
    form = AddCommentForm()

    starship = Starship.query.get_or_404(starship_id)
    if form.validate_on_submit():
        comment = Comment(
            text=form.text.data,
            user_id=g.user.id,
            starship_id=starship.id
        )
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('starship_detail', starship_id=starship.id))
    comments = Comment.query.filter_by(starship_id=starship.id).all()
    return render_template('/swapi/starship_detail.html', starship=starship, form=form, comments=comments)

@app.route('/vehicles', methods=['GET'])
def list_vehicles():
    """Load list of vehicles"""
    vehicles = Vehicle.query.all()
    return render_template('/swapi/vehicles_list.html', vehicles=vehicles)

@app.route('/vehicles/<int:vehicle_id>', methods=['GET', 'POST'])
def vehicle_detail(vehicle_id):
    """Load details of a vehicle"""
    form = AddCommentForm()

    vehicle = Vehicle.query.get_or_404(vehicle_id)
    if form.validate_on_submit():
        comment = Comment(
            text=form.text.data,
            user_id=g.user.id,
            vehicle_id=vehicle.id
        )
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('vehicle_detail', vehicle_id=vehicle.id))
    comments = Comment.query.filter_by(vehicle_id=vehicle.id).all()
    return render_template('/swapi/vehicle_detail.html', vehicle=vehicle, form=form, comments=comments)

@app.route('/species', methods=['GET'])
def list_species():
    """Load list of species"""
    species = Species.query.all()
    return render_template('/swapi/species_list.html', species=species)

@app.route('/species/<int:species_id>', methods=['GET', 'POST'])
def species_detail(species_id):
    """Load details of a species"""
    form = AddCommentForm()

    species = Species.query.get_or_404(species_id)
    if form.validate_on_submit():
        comment = Comment(
            text=form.text.data,
            user_id=g.user.id,
            species_id=species.id
        )
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('species_detail', species_id=species.id))
    comments = Comment.query.filter_by(species_id=species.id).all()
    return render_template('/swapi/species_detail.html', species=species, form=form, comments=comments)

@app.route('/planets', methods=['GET'])
def list_planets():
    """Load list of planets"""
    planets = Planet.query.all()
    return render_template('/swapi/planets_list.html', planets=planets)

@app.route('/planets/<int:planet_id>', methods=['GET', 'POST'])
def planet_detail(planet_id):
    """Load a details of a planet"""
    form = AddCommentForm()

    planet = Planet.query.get_or_404(planet_id)
    if form.validate_on_submit():
        comment = Comment(
            text=form.text.data,
            user_id=g.user.id,
            planet_id=planet.id
        )
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('planet_detail', planet_id=planet.id))
    comments = Comment.query.filter_by(planet_id=planet.id).all()
    return render_template('/swapi/planet_detail.html', planet=planet, form=form, comments=comments)


# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#            Comment Routes
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


@app.route('/comment/<int:comment_id>/vote', methods=['POST'])
@login_required
def vote_comment(comment_id):
    """Handle voting on a comment"""
    comment = Comment.query.get_or_404(comment_id)
    vote_type = request.form.get('vote')

    if comment.user_id == g.user.id:
        flash('You cannot vote on your own comment.', 'warning')
        return redirect(request.referrer)

    existing_vote = CommentVote.query.filter_by(comment_id=comment.id, user_id=g.user.id).first()

    if existing_vote:
        if (vote_type == 'up' and existing_vote.vote) or (vote_type == 'down' and not existing_vote.vote):
            db.session.delete(existing_vote)
            if vote_type == 'up':
                comment.upvotes -= 1
            else:
                comment.downvotes -= 1

        else:
            existing_vote.vote = vote_type =='up'
            if vote_type == 'up':
                comment.upvotes += 1
                comment.downvotes -= 1
            else:
                comment.upvotes -= 1
                comment.downvotes += 1
    else:
        new_vote = CommentVote(
            comment_id=comment.id,
            user_id=g.user.id,
            vote=vote_type == 'up'
        )
        db.session.add(new_vote)
        if vote_type == 'up':
            comment.upvotes += 1
        else:
            comment.downvotes += 1

    db.session.commit()
    return redirect(request.referrer)


@app.route('/comment/<int:comment_id>/delete', methods=['POST'])
@login_required
def delete_comment(comment_id):
    """Delete a comment"""
    comment = Comment.query.get_or_404(comment_id)

    if comment.user_id != g.user.id:
        flash('You do not have permission to delete this comment.', 'danger')
        return redirect(url_for('user_profile', user_id=g.user.id))
    
    if request.method == 'POST':
        db.session.delete(comment)
        db.session.commit()
        flash('Comment deleted successfully.', 'success')

    return redirect(url_for('user_profile', user_id=g.user.id))


if __name__ == "__main__":
    app.run(debug=True)