from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from restaurant.api import MenuViewSet, BookingViewSet

router = DefaultRouter()
router.register('menu-items', MenuViewSet, basename='menu-api')
router.register('bookings', BookingViewSet, basename='booking-api')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('', include('restaurant.urls')),
]
