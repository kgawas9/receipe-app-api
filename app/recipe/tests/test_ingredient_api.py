"""
Test cases for ingredient API functionality.
"""
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Ingredient

from recipe.serializers import IngredientSerializer


INGREDIENTS_URL = reverse('recipe:ingredient-list')


def detail_url(ingredient_id):
    """Create and return ingredient detail URL."""
    return reverse('recipe:ingredient-detail', args=[ingredient_id])


def create_user(email='user@example.com', password='TestPass123'):
    """Create and return user."""
    return get_user_model().objects.create_user(
        email=email, password=password
    )


class PublicIngredientsAPITest(TestCase):
    """Test unauthenticated API request for ingredients."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test authentication is required for requesting ingredients APIs."""
        res = self.client.get(INGREDIENTS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateIngredientAPITest(TestCase):
    """Test authenticated API request."""

    def setUp(self):
        self.user = create_user()
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_ingredients(self):
        """Test to retrieve ingredient list."""
        Ingredient.objects.create(user=self.user, name='Kale')
        Ingredient.objects.create(user=self.user, name='Vanilla')

        res = self.client.get(INGREDIENTS_URL)

        ingredients = Ingredient.objects.all().order_by('-name')
        serializer = IngredientSerializer(ingredients, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer.data, res.data)

    def test_user_based_limited_ingredients(self):
        """Test list of ingredients which is limited to user."""
        user1 = create_user(email='user1@example.com', password='Pass123@')

        Ingredient.objects.create(user=self.user, name='Ingredient1')
        Ingredient.objects.create(user=user1, name='Ingredient2')
        Ingredient.objects.create(user=self.user, name='Ingredient3')

        res = self.client.get(INGREDIENTS_URL)

        ingredients = Ingredient.objects.filter(
            user=self.user
            ).order_by('-name')
        serializer = IngredientSerializer(ingredients, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

        # ========= created by Mark =========
        # Ingredient.objects.create(user=user1, name='Salt')
        # ingredient = Ingredient.objects.create(user=self.user, name='Pepper')

        # res = self.client.get(INGREDIENTS_URL)

        # self.assertEqual(res.status_code, status.HTTP_200_OK)
        # self.assertEqual(len(res.data), 1)
        # self.assertEqual(res.data[0]['name'], ingredient.name)
        # self.assertEqual(res.data[0]['id'], ingredient.id)

    def test_update_ingredients(self):
        """Test case for updating an ingredient API."""
        ingredient = Ingredient.objects.create(
            user=self.user,
            name='Ingredient_1'
        )

        payload = {'name': 'Ingredient_updated_name'}
        url = detail_url(ingredient.id)

        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        ingredient.refresh_from_db()
        self.assertEqual(ingredient.name, payload['name'])

    def test_delete_ingredients(self):
        """Test to delete ingredients."""
        ingredient = Ingredient.objects.create(
            user=self.user,
            name='Ingredient_1',
        )

        url = detail_url(ingredient_id=ingredient.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        ingredients = Ingredient.objects.filter(user=self.user)
        self.assertFalse(ingredients.exists())
