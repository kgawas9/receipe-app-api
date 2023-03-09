"""
Tests for models.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model

from core.management.commands import wait_for_db

class TModelTest(TestCase):
    """Test models."""

    def test_create_with_email_successful(self):
        """Test creating a user with an email is successful"""
        email = 'test@example.com'
        password = 'testpass123'

        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
