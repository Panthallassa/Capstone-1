import unittest
from flask_bcrypt import Bcrypt
from app import app, db
from models import User, Person, Film, Starship, Vehicle, Species, Planet

bcrypt = Bcrypt(app)

class SwapiRouteTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up test client and initialize database"""
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///test_star_wars'
        app.config['WTF_CSRF_ENABLED'] = False 
        cls.client = app.test_client()

        with app.app_context():
            db.create_all()

    @classmethod
    def tearDownClass(cls):
        """Clean up any leftover data"""
        with app.app_context():
            db.drop_all()

    def setUp(self):
        """Reset database and add sample data"""
        with app.app_context():
            db.session.remove()
            db.drop_all()
            db.create_all()
            
            # Correct password hashing for test user
            hashed_password = bcrypt.generate_password_hash("password").decode('utf-8')
            self.user = User(username="testuser", email='test@gmail.com', password=hashed_password)
            db.session.add(self.user)
            db.session.commit()
            self.login_test_user()

    def tearDown(self):
        """Remove session and drop all tables"""
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def login_test_user(self):
        """Log in the test user"""
        with self.client as client:
            return client.post('/login', data={'username': 'testuser', 'password': 'password'}, follow_redirects=True)

    # Test Characters
    def test_list_characters(self):
        """Test loading the list of characters"""
        with self.client as client:
            response = client.get('/characters')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Characters', response.data)

    def test_character_detail(self):
        """Test loading the detail page of a specific character"""
        with app.app_context():
            person = Person(name="Luke Skywalker")
            db.session.add(person)
            db.session.commit()

            person_id = person.id

        with self.client as client:
            response = client.get(f'/characters/{person_id}')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Luke Skywalker', response.data)

    # Test Films
    def test_list_films(self):
        """Test loading the list of films"""
        with self.client as client:
            response = client.get('/films')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Films', response.data)

    def test_film_detail(self):
        """Test loading the detail page of a specific film"""
        with app.app_context():
            film = Film(title="A New Hope")
            db.session.add(film)
            db.session.commit()

            film_id = film.id

        with self.client as client:
            response = client.get(f'/films/{film_id}')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'A New Hope', response.data)

    # Test Starships
    def test_list_starships(self):
        """Test loading the list of starships"""
        with self.client as client:
            response = client.get('/starships')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Starships', response.data)

    def test_starship_detail(self):
        """Test loading the detail page of a specific starship"""
        with app.app_context():
            starship = Starship(name="Millennium Falcon")
            db.session.add(starship)
            db.session.commit()

            starship_id = starship.id

        with self.client as client:
            response = client.get(f'/starships/{starship_id}')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Millennium Falcon', response.data)

    # Test Vehicles
    def test_list_vehicles(self):
        """Test loading the list of vehicles"""
        with self.client as client:
            response = client.get('/vehicles')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Vehicles', response.data)

    def test_vehicle_detail(self):
        """Test loading the detail page of a specific vehicle"""
        with app.app_context():
            vehicle = Vehicle(name="Speeder")
            db.session.add(vehicle)
            db.session.commit()

            vehicle_id = vehicle.id

        with self.client as client:
            response = client.get(f'/vehicles/{vehicle_id}')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Speeder', response.data)

    # Test Species
    def test_list_species(self):
        """Test loading the list of species"""
        with self.client as client:
            response = client.get('/species')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Species', response.data)

    def test_species_detail(self):
        """Test loading the detail page of a specific species"""
        with app.app_context():
            species = Species(name="Wookie")
            db.session.add(species)
            db.session.commit()

            species_id = species.id

        with self.client as client:
            response = client.get(f'/species/{species_id}')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Wookie', response.data)

    # Test Planets
    def test_list_planets(self):
        """Test loading the list of planets"""
        with self.client as client:
            response = client.get('/planets')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Planets', response.data)

    def test_planet_detail(self):
        """Test loading the detail page of a specific planet"""
        with app.app_context():
            planet = Planet(name="Tatooine")
            db.session.add(planet)
            db.session.commit()

            planet_id = planet.id

        with self.client as client:
            response = client.get(f'/planets/{planet_id}')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Tatooine', response.data)

if __name__ == '__main__':
    unittest.main()
