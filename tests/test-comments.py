import unittest
from app import app, db, User, Comment
from fetch import fetch_all_data

class CommentRouteTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Setup the test client and database"""
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF for testing

        cls.client = app.test_client()
        
        with app.app_context():
            fetch_all_data()
            db.create_all()
            cls.create_test_data()

    @classmethod
    def tearDownClass(cls):
        """Tear down the database"""
        with app.app_context():
            db.drop_all()

    @classmethod
    def create_test_data(cls):
        """Create test data"""
        # Create test user
        test_user = User.signup(username="testuser", email="testuser@example.com", password="password")
        db.session.add(test_user)
        
        # Create another test user
        another_user = User.signup(username="anotheruser", email="anotheruser@example.com", password="password")
        db.session.add(another_user)
        db.session.commit()

        # Create test comments
        comment1 = Comment(text="This is a test comment", user_id=test_user.id)
        comment2 = Comment(text="This is another test comment", user_id=another_user.id)
        db.session.add_all([comment1, comment2])
        db.session.commit()

        print("%%%%%%%%%%%%%%%%%%%%%%%%")
        print(f"Created comments: {[c.id for c in Comment.query.all()]}")

    def login_test_user(self):
        """Helper method to log in test user"""
        self.client.post('/login', data={
            'username': 'testuser',
            'password': 'password'
        })

def test_vote_comment(self):
    """Test voting on a comment"""
    with self.client as client:
        # Log in a test user
        self.login_test_user()

        # Ensure the comment with ID 2 exists
        comment = Comment.query.get(2)
        self.assertIsNotNone(comment, "Comment with ID 2 does not exist")

        # Upvote a comment
        response = client.post('/comment/2/vote', data={'vote': 'up'}, follow_redirects=True)

        # Refresh the comment object to check updated values
        comment = Comment.query.get(2)
        self.assertEqual(comment.upvotes, 1, "Upvote count did not increment correctly")

        # Downvote the same comment
        response = client.post('/comment/2/vote', data={'vote': 'down'}, follow_redirects=True)

        # Refresh the comment object to check updated values
        comment = Comment.query.get(2)
        self.assertEqual(comment.upvotes, 0, "Upvote count did not decrement correctly")
        self.assertEqual(comment.downvotes, 1, "Downvote count did not increment correctly")

        # Remove downvote
        response = client.post('/comment/2/vote', data={'vote': 'down'}, follow_redirects=True)

        # Refresh the comment object to check updated values
        comment = Comment.query.get(2)
        self.assertEqual(comment.downvotes, 0, "Downvote count did not decrement correctly")


    def test_delete_comment(self):
        """Test deleting a comment"""
        with self.client as client:
            self.login_test_user()
            
            # Delete the user's own comment
            response = client.post('/comment/1/delete', follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIsNone(Comment.query.get(1))

            # Try to delete another user's comment
            response = client.post('/comment/2/delete', follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'You do not have permission to delete this comment.', response.data)
            self.assertIsNotNone(Comment.query.get(2))


if __name__ == '__main__':
    unittest.main()
