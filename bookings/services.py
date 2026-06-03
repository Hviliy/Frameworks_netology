from bookings.models import Booking


def user_has_booking(user, workshop, exclude_booking_id=None) -> bool:
    queryset = Booking.objects.filter(user=user, workshop=workshop)
    if exclude_booking_id is not None:
        queryset = queryset.exclude(id=exclude_booking_id)
    return queryset.exists()


def workshop_has_available_places(workshop, exclude_booking_id=None) -> bool:
    queryset = Booking.objects.filter(workshop=workshop)
    if exclude_booking_id is not None:
        queryset = queryset.exclude(id=exclude_booking_id)

    return queryset.count() < workshop.capacity
