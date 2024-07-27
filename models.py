"""Models for Star Wars application"""

from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_

bcrypt = Bcrypt()
db = SQLAlchemy()


class User(db.Model):
    """User model"""

    __tablename__ = 'users'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    username = db.Column(
        db.Text,
        nullable=False,
        unique=True
    )

    email = db.Column(
        db.Text,
        nullable=False,
        unique=True
    )

    password = db.Column(
        db.Text,
        nullable=False
    )

    comments = db.relationship('Comment', backref='user', lazy=True)
    

    @classmethod
    def signup(cls, username, email, password):
        """Sign up user, add them to the system, and hash password"""

        if not username or not email or not password:
            raise ValueError('Username, email, and password are required')
        
        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            username=username,
            email=email,
            password=hashed_pwd,
        )

        db.session.add(user)
        db.session.commit()
        return user
    
    @classmethod
    def authenticate(cls, username, password):
        """Find user with matching username and password and check if the
        variables are correct, if so return user object.
        
        If not found, return False."""

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user
            
        return False


class Comment(db.Model):
    """An individual comment"""

    __tablename__ = 'comments'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    text = db.Column(
        db.String(200),
        nullable=False
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False
    )

    person_id = db.Column(
        db.Integer,
        db.ForeignKey('people.id', ondelete='CASCADE'),
        nullable=True
    )

    film_id = db.Column(
        db.Integer,
        db.ForeignKey('films.id', ondelete='CASCADE'),
        nullable=True
    )

    starship_id = db.Column(
        db.Integer,
        db.ForeignKey('starships.id', ondelete='CASCADE'),
        nullable=True
    )

    vehicle_id = db.Column(
        db.Integer,
        db.ForeignKey('vehicles.id', ondelete='CASCADE'),
        nullable=True
    )

    species_id = db.Column(
        db.Integer,
        db.ForeignKey('species.id', ondelete='CASCADE'),
        nullable=True
    )
    
    planet_id = db.Column(
        db.Integer,
        db.ForeignKey('planets.id', ondelete='CASCADE'),
        nullable=True
    )

    upvotes = db.Column(
        db.Integer,
        default=0
    )

    downvotes = db.Column(
        db.Integer,
        default=0
    )


class CommentVote(db.Model):
    """Model to store upvote and downvotes for comments"""

    __tablename__ = 'comment_votes'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    comment_id = db.Column(
        db.Integer,
        db.ForeignKey('comments.id', ondelete='CASCADE'),
        nullable=False
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False
    )

    vote = db.Column(
        db.Boolean,
        nullable=False
    )




# *****************************************
#              SWAPI Models
# *****************************************




class Person(db.Model):
    """A character in the star wars universe"""

    __tablename__ = 'people'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String,
        unique=True
    )

    birth_year = db.Column(
        db.String
    )

    eye_color = db.Column(
        db.String
    )

    gender = db.Column(
        db.String
    )

    hair_color = db.Column(
        db.String
    )

    height = db.Column(
        db.String
    )

    mass = db.Column(
        db.String
    )

    skin_color = db.Column(
        db.String
    )

    homeworld_id = db.Column(db.Integer, db.ForeignKey('planets.id'))

    films = db.relationship('Film', secondary='people_films', back_populates='characters')

    species = db.relationship('Species', secondary='species_people', back_populates='people')

    starships = db.relationship('Starship', secondary='people_starships', back_populates='pilots')

    vehicles = db.relationship('Vehicle', secondary='people_vehicles', back_populates='pilots')

    comments = db.relationship('Comment', backref='person', lazy=True)



class Film(db.Model):
    """Film model"""

    __tablename__ = 'films'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    title = db.Column(
        db.String,
        unique=True
    )

    episode_id = db.Column(
        db.Integer
    )

    opening_crawl = db.Column(
        db.String
    )

    director = db.Column(
        db.String
    )

    producer = db.Column(
        db.String
    )

    release_date = db.Column(
        db.Date
    )

    species = db.relationship('Species', secondary='films_species', back_populates='films')

    starships = db.relationship('Starship', secondary='films_starships', back_populates='films')

    vehicles = db.relationship('Vehicle', secondary='films_vehicles', back_populates='films')

    characters = db.relationship('Person', secondary='people_films', back_populates='films')

    planets = db.relationship('Planet', secondary='films_planets', back_populates='films')

    comments = db.relationship('Comment', backref='film', lazy=True)


class Starship(db.Model):
    """Starship model"""

    __tablename__ = 'starships'

    id = db.Column(
        db.Integer, 
        primary_key=True
    )

    name = db.Column(
        db.String,
        unique=True
    )

    model = db.Column(
        db.String
    )

    starship_class = db.Column(
        db.String
    )

    manufacturer = db.Column(
        db.String
    )

    cost_in_credits = db.Column(
        db.String
    )

    length = db.Column(
        db.String
    )

    crew = db.Column(
        db.String
    )

    passengers = db.Column(
        db.String
    )

    max_atmosphering_speed = db.Column(
        db.String
    )

    hyperdrive_rating = db.Column(
        db.String
    )

    MGLT = db.Column(
        db.String
    )

    cargo_capacity = db.Column(
        db.String
    )

    consumables = db.Column(
        db.String
    )

    pilots = db.relationship('Person', secondary='people_starships', back_populates='starships')

    films = db.relationship('Film', secondary='films_starships', back_populates='starships')

    comments = db.relationship('Comment', backref='starship', lazy=True)



class Vehicle(db.Model):
    """Vehicle model"""

    __tablename__ = 'vehicles'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String,
        unique=True
    )

    model = db.Column(
        db.String
    )

    vehicle_class = db.Column(
        db.String
    )

    manufacturer = db.Column(
        db.String
    )

    length = db.Column(
        db.String
    )

    cost_in_credits = db.Column(
        db.String
    )

    crew = db.Column(
        db.String
    )

    passengers = db.Column(
        db.String
    )

    max_atmosphering_speed = db.Column(
        db.String
    )

    cargo_capacity = db.Column(
        db.String
    )

    consumables = db.Column(
        db.String
    )


    pilots = db.relationship('Person', secondary='people_vehicles', back_populates='vehicles')

    films = db.relationship('Film', secondary='films_vehicles', back_populates='vehicles')

    comments = db.relationship('Comment', backref='vehicle', lazy=True)



class Species(db.Model):
    """Species model"""

    __tablename__ = 'species'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String,
        unique=True
    )

    classification = db.Column(
        db.String
    )

    designation = db.Column(
        db.String
    )

    average_height = db.Column(
        db.String
    )

    average_lifespan = db.Column(
        db.String
    )

    eye_colors = db.Column(
        db.String
    )

    hair_colors = db.Column(
        db.String
    )

    skin_colors = db.Column(
        db.String
    )

    language = db.Column(
        db.String
    )

    homeworld_id = db.Column(db.Integer, db.ForeignKey('planets.id'))

    homeworld = db.relationship('Planet', backref='species')

    films = db.relationship('Film', secondary='films_species', back_populates='species')

    people = db.relationship('Person', secondary='species_people', back_populates='species')

    comments = db.relationship('Comment', backref='species', lazy=True)


class Planet(db.Model):
    """Planet Model"""

    __tablename__ = 'planets'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String,
        unique=True
    )

    diameter = db.Column(
        db.String
    )

    rotation_period = db.Column(
        db.String
    )

    orbital_period = db.Column(
        db.String
    )

    gravity = db.Column(
        db.String
    )

    population = db.Column(
        db.String
    )

    climate = db.Column(
        db.String
    )

    terrain = db.Column(
        db.String
    )

    surface_water = db.Column(
        db.String
    )

    residents = db.relationship('Person', backref='homeworld')

    films = db.relationship('Film', secondary='films_planets', back_populates='planets')

    comments = db.relationship('Comment', backref='planet', lazy=True)

# *****************************************
#          Relationship tables
# *****************************************


people_films = db.Table('people_films',
    db.Column('person_id', db.Integer, db.ForeignKey('people.id')),
    db.Column('film_id', db.Integer, db.ForeignKey('films.id'))
)

species_people = db.Table('species_people',
    db.Column('species_id', db.Integer, db.ForeignKey('species.id')),
    db.Column('person_id', db.Integer, db.ForeignKey('people.id'))
)

people_starships = db.Table('people_starships',
    db.Column('person_id', db.Integer, db.ForeignKey('people.id')),
    db.Column('starship_id', db.Integer, db.ForeignKey('starships.id'))
)

people_vehicles = db.Table('people_vehicles',
    db.Column('person_id', db.Integer, db.ForeignKey('people.id')),
    db.Column('vehicle_id', db.Integer, db.ForeignKey('vehicles.id'))
)


films_species = db.Table('films_species',
    db.Column('film_id', db.Integer, db.ForeignKey('films.id')),
    db.Column('species_id', db.Integer, db.ForeignKey('species.id'))
)

films_starships = db.Table('films_starships',
    db.Column('film_id', db.Integer, db.ForeignKey('films.id')),
    db.Column('starship_id', db.Integer, db.ForeignKey('starships.id'))
)

films_vehicles = db.Table('films_vehicles',
    db.Column('film_id', db.Integer, db.ForeignKey('films.id')),
    db.Column('vehicle_id', db.Integer, db.ForeignKey('vehicles.id'))
)

films_planets = db.Table('films_planets',
    db.Column('film_id', db.Integer, db.ForeignKey('films.id')),
    db.Column('planet_id', db.Integer, db.ForeignKey('planets.id'))
)



def search_elements(search_query):
    """Search database"""
    search_query = search_query.strip()

    people_exact = Person.query.filter(Person.name.ilike(f"%{search_query}%")).all()

    films_exact = Film.query.filter(Film.title.ilike(f"%{search_query}%")).all()

    starships_exact = Starship.query.filter(Starship.name.ilike(f"%{search_query}%")).all()

    vehicles_exact = Vehicle.query.filter(Vehicle.name.ilike(f"%{search_query}%")).all()

    planets_exact = Planet.query.filter(Planet.name.ilike(f"%{search_query}%")).all()

    species_exact = Species.query.filter(Species.name.ilike(f"%{search_query}%")).all()


    people_partial = Person.query.filter(Person.name.ilike(f"%{search_query}%")).all()

    films_partial = Film.query.filter(Film.title.ilike(f"%{search_query}%")).all()

    starships_partial = Starship.query.filter(Starship.name.ilike(f"%{search_query}%")).all()

    vehicles_partial = Vehicle.query.filter(Vehicle.name.ilike(f"%{search_query}%")).all()

    planets_partial = Planet.query.filter(Planet.name.ilike(f"%{search_query}%")).all()

    species_partial = Species.query.filter(Species.name.ilike(f"%{search_query}%")).all()


    people = list(dict.fromkeys(people_exact + people_partial))
    films = list(dict.fromkeys(films_exact + films_partial))
    starships = list(dict.fromkeys(starships_exact + starships_partial))
    vehicles = list(dict.fromkeys(vehicles_exact + vehicles_partial))
    planets = list(dict.fromkeys(planets_exact + planets_partial))
    species = list(dict.fromkeys(species_exact + species_partial))

    results = {
        'people': [{'name': person.name, 'type': 'person', 'id': person.id} for person in people],
        'films': [{'title': film.title, 'type': 'film', 'id': film.id} for film in films],
        'starships': [{'name': starship.name, 'type': 'starship', 'id': starship.id} for starship in starships],
        'vehicles': [{'name': vehicle.name, 'type': 'vehicle', 'id': vehicle.id} for vehicle in vehicles],
        'planets' : [{'name': planet.name, 'type': 'planet', 'id': planet.id} for planet in planets],
        'species' : [{'name': species.name, 'type': 'species', 'id': species.id} for species in species]
    }

    return results 


def connect_db(app):
    """Connect to database"""

    db.app = app
    db.init_app(app)