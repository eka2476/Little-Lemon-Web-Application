import json
from datetime import date
from django.core import serializers
from django.db import IntegrityError, transaction
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_http_methods
from .forms import BookingForm
from .models import Booking, Menu


def home(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def reservations(request):
    return render(request, 'bookings.html', {'bookings': serializers.serialize('json', Booking.objects.all())})

def book(request):
    return render(request, 'book.html', {'form': BookingForm()})

def menu(request):
    return render(request, 'menu.html', {'menu': {'menu': Menu.objects.all()}})

def display_menu_item(request, pk=None):
    return render(request, 'menu_item.html', {'menu_item': get_object_or_404(Menu, pk=pk) if pk else ''})


@require_http_methods(['GET', 'POST'])
def bookings(request):
    if request.method == 'GET':
        qs = Booking.objects.order_by(
            'reservation_date', 'reservation_slot'
        )

        if request.GET.get('date'):
            try:
                chosen = date.fromisoformat(request.GET['date'])
            except ValueError:
                return JsonResponse(
                    {'error': 'Invalid date'}, status=400
                )
            qs = qs.filter(reservation_date=chosen)

        return JsonResponse(
            list(qs.values(
                'id', 'first_name',
                'reservation_date', 'reservation_slot'
            )),
            safe=False
        )

    try:
        data = json.loads(request.body)
    except (ValueError, UnicodeDecodeError):
        return JsonResponse(
            {'error': 'Invalid JSON'}, status=400
        )

    form = BookingForm(data)

    if not form.is_valid():
        reservation_date = data.get('reservation_date')
        reservation_slot = data.get('reservation_slot')

        if reservation_date and reservation_slot is not None:
            if Booking.objects.filter(
                reservation_date=reservation_date,
                reservation_slot=reservation_slot
            ).exists():
                return JsonResponse(
                    {'error': 'This time slot is already booked'},
                    status=409
                )

        return JsonResponse(
            {'errors': form.errors.get_json_data()},
            status=400
        )

    try:
        with transaction.atomic():
            booking = form.save()
    except IntegrityError:
        return JsonResponse(
            {'error': 'This time slot is already booked'},
            status=409
        )

    return JsonResponse(
        {'id': booking.pk, 'message': 'Reservation created'},
        status=201
    )
