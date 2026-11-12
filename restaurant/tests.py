import json
from datetime import date
from django.test import TestCase
from django.urls import reverse
from .models import Booking

class BookingTests(TestCase):
    def test_booking_api_filters_by_date(self):
        Booking.objects.create(first_name='Sam', reservation_date=date(2026, 11, 12), reservation_slot=10)
        response = self.client.get(reverse('bookings'), {'date': '2026-11-13'})
        self.assertEqual(response.json(), [])

    def test_duplicate_booking_rejected(self):
        payload = {'first_name': 'Sam', 'reservation_date': '2026-11-12', 'reservation_slot': 10}
        first = self.client.post(reverse('bookings'), data=json.dumps(payload), content_type='application/json')
        self.assertEqual(first.status_code, 201)
        second = self.client.post(reverse('bookings'), data=json.dumps(payload), content_type='application/json')
        self.assertEqual(second.status_code, 409)

    def test_booking_page(self):
        self.assertContains(self.client.get(reverse('book')), 'reservation_date')
