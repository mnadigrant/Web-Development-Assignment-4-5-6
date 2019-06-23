#!/usr/bin/env python
from datetime import datetime, timedelta
import unittest
from app import app, db
from app.models import User, Post


class UserModelCase(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_password_hashing(self):
        u = User(username='georgette')
        u.set_password('lovesme')
        self.assertFalse(u.check_password('lovesu'))
        self.assertTrue(u.check_password('lovesme'))

    def test_avatar(self):
        u = User(username='mnadi', email='mnadi@gmail.com')
        self.assertEqual(u.avatar(128), ('https://www.gravatar.com/avatar/561805d7328663fdbc73a0507f3c6692?d=identicon&s=128'))
if __name__ == '__main__':
    unittest.main(verbosity=2)
