# myapp/tests.py

from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from .models import Category, Course
from users.models import CustomUser


class CategoryListViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(username='testuser', email='testuser@gmail.com', password='testpassword')
        self.client.force_authenticate(user=self.user)
        self.url = '/categories/'
        
        self.category1 = Category.objects.create(title='Category 1')
        self.category2 = Category.objects.create(title='Category 2', parent=self.category1)

    def test_list_categories(self):
        print('Testing list categories')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]['title'], 'Category 1')
        self.assertEqual(data[1]['title'], 'Category 2')

    def test_create_category(self):
        print('Testing create category')
        data = {
            'title': 'New Category',
            'parent': self.category1.id
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(Category.objects.count(), 3)
        self.assertEqual(Category.objects.latest('id').title, 'New Category')

    def test_create_category_missing_title(self):
        print('Testing missing title create category')
        data = {
            'title': ''
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('title', response.json())


class CategoryDetailViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(username='testuser', email='testuser@gmail.com', password='testpassword')
        self.client.force_authenticate(user=self.user)

        self.category1 = Category.objects.create(title='Category 1')
        self.category2 = Category.objects.create(title='Category 2', parent=self.category1)

        self.url = f'/categories/{self.category1.pk}/'

    def test_get_category(self):
        print('Testing get category by id')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Category 1')

    def test_update_category(self):
        print('Testing update category')
        data = {'title': 'Updated Category'}
        response = self.client.put(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.category1.refresh_from_db()
        self.assertEqual(self.category1.title, 'Updated Category')

    def test_not_found(self):
        print('Testing invalid id for category')
        url = '/categories/-1/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


# Other apis