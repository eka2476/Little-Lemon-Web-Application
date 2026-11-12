
from django.db import IntegrityError, transaction
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from .models import Menu, Booking
from .serializers import MenuSerializer, BookingSerializer


class MenuViewSet(viewsets.ModelViewSet):
    queryset = Menu.objects.all().order_by('id')
    serializer_class = MenuSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all().order_by(
        'reservation_date', 'reservation_slot'
    )
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        qs = super().get_queryset()
        date = self.request.query_params.get('date')
        if date:
            qs = qs.filter(reservation_date=date)
        return qs

    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            with transaction.atomic():
                self.perform_create(serializer)
        except IntegrityError:
            return Response(
                {'detail': 'This time slot is already booked.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=self.get_success_headers(serializer.data)
        )
