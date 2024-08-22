import unittest
from app import app, db, User
from fetch import fetch_all_data

class UserRouteTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Setup the test client and database"""
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///test_star_wars'
        app.config['WTF_CSRF_ENABLED'] = False 

        cls.client = app.test_client()
        
        with app.app_context():
            db.create_all()
            fetch_all_data
            cls.create_test_user()

    @classmethod
    def tearDownClass(cls):
        """Tear down the database"""
        with app.app_context():
            db.drop_all()

    @classmethod
    def create_test_user(cls):
        """Create a test user"""
        test_user = User.signup(username="testuser", email="testuser@example.com", password="password")
        db.session.add(test_user)
        db.session.commit()

    def test_signup(self):
        """Test user signup"""
        with self.client as client:
            response = client.post('/signup', data={
                'username': 'newuser',
                'email': 'newuser@example.com',
                'password': 'password',
                'confirm': 'password'
            }, follow_redirects=True)

            self.assertEqual(response.status_code, 200)


    def test_login(self):
        """Test user login"""
        with self.client as client:
            response = client.post('/login', data={
                'username': 'testuser',
                'password': 'password'
            }, follow_redirects=True)

            self.assertEqual(response.status_code, 200)

    def test_logout(self):
        """Test user logout"""
        with self.client as client:
            with client.session_transaction() as session:
                session['user_id'] = 1  

            response = client.get('/logout', follow_redirects=True)

            self.assertEqual(response.status_code, 200)

    def test_user_profile(self):
        """Test user profile access"""
        with self.client as client:
            client.post('/login', data={
            'username': 'testuser',
            'password': 'password'
            })

            response = client.get('/profile/1')

            self.assertEqual(response.status_code, 302)

    def test_unauthorized_user_profile_access(self):
        """Test that a user cannot access another user's profile"""
        with self.client as client:

            client.post('/login', data={
                'username': 'testuser',
                'password': 'password'
            })


            response = client.get('/profile/2', follow_redirects=True)

            self.assertEqual(response.status_code, 200) 
            self.assertIn(b'You do not have permission to view this profile.', response.data)

    def test_edit_user(self):
        """Test user edit"""
        with self.client as client:
            with client.session_transaction() as session:
                session['user_id'] = 1  

            response = client.post('/edit/1', data={
                'username': 'updateduser',
                'email': 'updateduser@example.com',
                'password': 'password',
                'new_password': 'newpassword'
            }, follow_redirects=True)

            self.assertEqual(response.status_code, 200)

    def test_edit_user_duplicate_username(self):
        """Test editing a user with a duplicate username"""
        with self.client as client:
            with client.session_transaction() as session:
                session['user_id'] = 1  

            response = client.post('/edit/1', data={
                'username': 'anotheruser',  
                'email': 'testuser@example.com',
                'password': 'password'
            }, follow_redirects=True)

            self.assertIn(b'Username already exists. Please choose a different one.', response.data)
            self.assertEqual(response.status_code, 200)

    def test_delete_user(self):
        """Test user delete"""
        with self.client as client:
            with client.session_transaction() as session:
                session['user_id'] = 1

            response = client.post('/edit/1/delete', follow_redirects=True)

            self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
