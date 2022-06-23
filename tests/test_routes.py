import unittest
from api.routes import app
import json
from db import DatabaseConnection


class TestUsers(unittest.TestCase):
    def setUp(self):
        """
        Setup our test Client
        """
        self.test_client = app.test_client()
        self.db = DatabaseConnection()

    def test_user_register(self):
        """
        Test registering a user with correct details
        """
        user = {
            'username': 'KengoWada',
            'email': 'kengowada@nasa.com',
            'password': 'kengowada'
        }

        response  = self.test_client.post(
            'api/v1/signup',
            content_type='application/json',
            data=json.dumps(user)
        )

        message = json.loads(response.data.decode())

        self.assertEqual(message['message'], 'KengoWada successfully registered.')
    
    def test_register_username_twice(self):
        """
        Test registering a user twice with the same username
        """
        user1 = {
            'username': 'KengoWada',
            'email': 'kengowada@apple.com',
            'password': 'kengowada'
        }

        self.test_client.post(
            'api/v1/signup',
            content_type='application/json',
            data=json.dumps(user1)
        )

        user2 = {
            'username': 'KengoWada',
            'email': 'kengowada@apple.com',
            'password': 'kengowada'
        }

        response2  = self.test_client.post(
            'api/v1/signup',
            content_type='application/json',
            data=json.dumps(user2)
        )

        message = json.loads(response2.data.decode())

        self.assertEqual(message['message'], 'Username is taken.')

    def test_register_email_twice(self):
        """
        Test registering a user with the same email twice
        """
        user1 = {
            'username': 'KengoWada',
            'email': 'kengowada@apple.com',
            'password': 'kengowada'
        }

        self.test_client.post(
            'api/v1/signup',
            content_type='application/json',
            data=json.dumps(user1)
        )

        user2 = {
            'username': 'WadaKengo',
            'email': 'kengowada@apple.com',
            'password': 'kengowada'
        }

        response2  = self.test_client.post(
            'api/v1/signup',
            content_type='application/json',
            data=json.dumps(user2)
        )

        message = json.loads(response2.data.decode())

        self.assertEqual(message['message'], 'Email already has an account.')

    def test_register_empty_username(self):
        """
        Test registering a user with the username field empty
        """
        user = {
            'username': '',
            'email': 'kengowada@nasa.com',
            'password': 'kengowada'
        }

        response  = self.test_client.post(
            'api/v1/signup',
            content_type='application/json',
            data=json.dumps(user)
        )

        message = json.loads(response.data.decode())

        self.assertEqual(message['Error'], 'Username field can not be left empty.')

    def test_register_empty_email(self):
        """
        Test registering a user with email field empty
        """
        user = {
            'username': 'kengowada',
            'email': '',
            'password': 'kengowada'
        }

        response  = self.test_client.post(
            'api/v1/signup',
            content_type='application/json',
            data=json.dumps(user)
        )

        message = json.loads(response.data.decode())

        self.assertEqual(message['Error'], 'Email field can not be left empty.')

    def test_register_empty_password(self):
        """
        Test registering a user with password field empty
        """
        user = {
            'username': 'kengowada',
            'email': 'kengowada@nasa.com',
            'password': ''
        }

        response  = self.test_client.post(
            'api/v1/signup',
            content_type='application/json',
            data=json.dumps(user)
        )

        message = json.loads(response.data.decode())

        self.assertEqual(message['Error'], 'Password field can not be left empty.')

    def test_register_invalid_email(self):
        """
        Test registering a user with wrong email format
        """
        user = {
            'username': 'kengowada',
            'email': 'kengonasa.com',
            'password': 'kengowada'
        }

        response  = self.test_client.post(
            'api/v1/signup',
            content_type='application/json',
            data=json.dumps(user)
        )

        message = json.loads(response.data.decode())

        self.assertEqual(message['Error'], 'Enter a valid email address.')

    def test_register_password_length(self):
        """
        Test registering a user with password less than 8 characters
        """
        user = {
            'username': 'kengowada',
            'email': 'kengowada@nasa.com',
            'password': 'keda'
        }

        response  = self.test_client.post(
            'api/v1/signup',
            content_type='application/json',
            data=json.dumps(user)
        )

        message = json.loads(response.data.decode())

        self.assertEqual(message['Error'], 'Password has to be longer than 8 characters.')

    def test_user_login(self):
        """
        Test login a user with correct details
        """
        user1 = {
            'username': 'KengoWada',
            'email': 'kengowada@apple.com',
            'password': 'kengowada'
        }

        self.test_client.post(
            'api/v1/signup',
            content_type='application/json',
            data=json.dumps(user1)
        )

        user = {
            'username': 'KengoWada',
            'password': 'kengowada'
        }

        response = self.test_client.post(
            'api/v1/login',
            content_type='application/json',
            data=json.dumps(user)
        )

        message = json.loads(response.data.decode())

        self.assertEqual(message['message'], 'KengoWada successfully logged in.')

    def test_user_login_empty_username(self):
        """
        Test login a user with empty username
        """
        user1 = {
            'username': 'KengoWada',
            'email': 'kengowada@apple.com',
            'password': 'kengowada'
        }

        self.test_client.post(
            'api/v1/signup',
            content_type='application/json',
            data=json.dumps(user1)
        )

        user = {
            'username': '',
            'password': 'kengowada'
        }

        response = self.test_client.post(
            'api/v1/login',
            content_type='application/json',
            data=json.dumps(user)
        )

        message = json.loads(response.data.decode())

        self.assertEqual(message['Error'], 'Username field can not be left empty.')

    def test_user_login_empty_password(self):
        """
        Test login a user with empty password
        """
        user1 = {
            'username': 'KengoWada',
            'email': 'kengowada@apple.com',
            'password': 'kengowada'
        }

        self.test_client.post(
            'api/v1/signup',
            content_type='application/json',
            data=json.dumps(user1)
        )

        user = {
            'username': 'KengoWada',
            'password': ''
        }

        response = self.test_client.post(
            'api/v1/login',
            content_type='application/json',
            data=json.dumps(user)
        )

        message = json.loads(response.data.decode())

        self.assertEqual(message['Error'], 'Password field can not be left empty.')
    
    def test_login_wrong_username(self):
        """
        Test login a user with username that doesn't exist
        """
        user1 = {
            'username': 'KengoWada',
            'email': 'kengowada@apple.com',
            'password': 'kengowada'
        }

        self.test_client.post(
            'api/v1/signup',
            content_type='application/json',
            data=json.dumps(user1)
        )

        user = {
            'username': 'Kengo Wada',
            'password': 'kengowada'
        }

        response = self.test_client.post(
            'api/v1/login',
            content_type='application/json',
            data=json.dumps(user)
        )

        message = json.loads(response.data.decode())

        self.assertEqual(message['message'], 'Wrong login credentials.')

    def test_login_wrong_password(self):
        """
        Test login a user with wrong password
        """
        user1 = {
            'username': 'KengoWada',
            'email': 'kengowada@apple.com',
            'password': 'kengowada'
        }

        self.test_client.post(
            'api/v1/signup',
            content_type='application/json',
            data=json.dumps(user1)
        )

        user = {
            'username': 'KengoWada',
            'password': 'kengowada1234'
        }

        response = self.test_client.post(
            'api/v1/login',
            content_type='application/json',
            data=json.dumps(user)
        )

        message = json.loads(response.data.decode())

        self.assertEqual(message['message'], 'Wrong login credentials.')

    def test_welcome(self):
        """
        Test accessing the protected route
        """
        user1 = {
            'username': 'KengoWada',
            'email': 'kengowada@apple.com',
            'password': 'kengowada'
        }

        response1 = self.test_client.post(
            'api/v1/signup',
            content_type='application/json',
            data=json.dumps(user1)
        )

        token = json.loads(response1.data.decode())

        response = self.test_client.get(
            'api/v1/welcome',
            headers={'Authorization': 'Bearer ' + token['access_token']},
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)

    
    def test_invalid_route(self):
        """
        Test for when invalid routes are used to make requests
        """
        user = {
            'username': 'KengoWada',
            'email': 'kengowada@apple.com',
            'password': 'kengowada'
        }

        response = self.test_client.post(
            'api/v1/auth/signup',
            content_type='application/json',
            data=json.dumps(user)
        )

        message = json.loads(response.data.decode())

        self.assertEqual(message['message'], 'Please contact Kengo Wada for more details on this API.')

    def tearDown(self):
        """
        Drop the user table very after a single test has run
        """
        self.db.drop_table('users')
    