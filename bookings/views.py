from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from bookings.models import Booking
from bookings.permissions import IsBookingOwnerOrAdmin
from bookings.serializers import BookingSerializer


class BookingViewSet(viewsets.ModelViewSet):
    serializer_class = BookingSerializer
    permission_classes = (IsAuthenticated, IsBookingOwnerOrAdmin)

    def get_queryset(self):
        queryset = Booking.objects.select_related("user", "workshop")
        if self.request.user.is_admin_role:
            return queryset
        return queryset.filter(user=self.request.user)

    def perform_create(self, serializer) -> None:
        serializer.save(user=self.request.user)
