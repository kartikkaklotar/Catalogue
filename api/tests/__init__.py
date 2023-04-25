from rest_framework.test import APITestCase
from django.db import connection
class BaseAPITestCase(APITestCase):
    @classmethod
    def setUpClass(cls):
        # Create a test database
        connection.creation.create_test_db()

    @classmethod
    def tearDownClass(cls):
        # Delete the test database
        connection.creation.destroy_test_db()