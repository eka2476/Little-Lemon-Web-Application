from datetime import date
from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from .models import Booking, Menu


class APITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(username='tester', password='StrongPass123!')
        self.token = Token.objects.create(user=self.user)
        self.menu = Menu.objects.create(name='Greek Salad', price=12, menu_item_description='Fresh salad')

    def test_public_menu_read(self):
        response = self.client.get('/api/menu-items/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['name'], 'Greek Salad')

    def test_menu_write_requires_auth(self):
        response = self.client.post('/api/menu-items/', {'name': 'Soup', 'price': 9})
        self.assertIn(response.status_code, (401, 403))

    def test_authenticated_menu_crud(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.post('/api/menu-items/', {'name': 'Pasta', 'price': 20, 'menu_item_description': 'Fresh pasta'})
        self.assertEqual(response.status_code, 201)
        pk = response.data['id']
        self.assertEqual(self.client.put(f'/api/menu-items/{pk}/', {'name': 'Pasta', 'price': 22, 'menu_item_description': 'Updated'}).status_code, 200)
        self.assertEqual(self.client.delete(f'/api/menu-items/{pk}/').status_code, 204)

    def test_booking_date_filter_and_duplicates(self):
        Booking.objects.create(first_name='Sam', reservation_date=date(2026, 11, 12), reservation_slot=10)
        self.assertEqual(len(self.client.get('/api/bookings/?date=2026-11-13').data), 0)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.post('/api/bookings/', {'first_name': 'Alex', 'reservation_date': '2026-11-12', 'reservation_slot': 10})
        self.assertEqual(response.status_code, 400)

    def test_token_login(self):
        response = self.client.post('/auth/token/login/', {'username': 'tester', 'password': 'StrongPass123!'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('auth_token', response.data)
