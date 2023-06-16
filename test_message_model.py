from unittest import TestCase
from models import db, User, Message

# ... Existing code ...

class MessageModelTestCase(TestCase):
    # ... Existing code ...

    def test_message_model(self):
        """Does basic Message model work?"""

        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        m = Message(text="Test message", user_id=u.id)

        db.session.add_all([u, m])
        db.session.commit()

        # Message should be associated with the user
        self.assertEqual(m.user, u)

    def test_message_likes(self):
        """Test the relationship between Message and User for likes."""

        u1 = User(
            email="user1@test.com",
            username="user1",
            password="HASHED_PASSWORD"
        )

        u2 = User(
            email="user2@test.com",
            username="user2",
            password="HASHED_PASSWORD"
        )

        m = Message(text="Test message", user_id=u1.id)

        m.likes.append(u2)

        db.session.add_all([u1, u2, m])
        db.session.commit()

        # User 2 should have liked the message
        self.assertEqual(len(m.likes), 1)
        self.assertIn(u2, m.likes)

    def test_message_likers(self):
        """Test the relationship between Message and User for likers."""

        u1 = User(
            email="user1@test.com",
            username="user1",
            password="HASHED_PASSWORD"
        )

        u2 = User(
            email="user2@test.com",
            username="user2",
            password="HASHED_PASSWORD"
        )

        m1 = Message(text="Test message 1", user_id=u1.id)
        m2 = Message(text="Test message 2", user_id=u2.id)

        u1.liked_messages.append(m2)
        u2.liked_messages.append(m1)

        db.session.add_all([u1, u2, m1, m2])
        db.session.commit()

        # User 1 should have liked message 2
        self.assertEqual(len(u1.liked_messages), 1)
        self.assertIn(m2, u1.liked_messages)

        # User 2 should have liked message 1
        self.assertEqual(len(u2.liked_messages), 1)
        self.assertIn(m1, u2.liked_messages)
