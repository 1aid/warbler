import unittest
from app import app, db
from models import User

class UserViewsTestCase(unittest.TestCase):
    def setUp(self):
        """Set up the test environment."""
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        app.config['TESTING'] = True
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        """Teardown the test environment."""
        db.session.remove()
        db.drop_all()

    def test_user_profile_page(self):
        """Test the user profile page."""
        user = User(username='testuser', email='test@example.com')
        db.session.add(user)
        db.session.commit()
        response = self.app.get(f'/users/{user.id}', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<h2>User Profile</h2>', response.data)

    def test_register_user(self):
        """Test the user registration process."""
        response = self.app.post('/register', data={'username': 'testuser', 'email': 'test@example.com', 'password': 'password'}, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<h2>User Profile</h2>', response.data)

    def test_login_logout(self):
        """Test the user login and logout process."""
        user = User(username='testuser', email='test@example.com', password='password')
        db.session.add(user)
        db.session.commit()

        # Test login
        response = self.app.post('/login', data={'username': 'testuser', 'password': 'password'}, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<h2>User Profile</h2>', response.data)

        # Test logout
        response = self.app.get('/logout', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<h2>Login</h2>', response.data)

if __name__ == '__main__':
    unittest.main()