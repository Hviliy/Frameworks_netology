from rest_framework import serializers

from bookings.models import Booking
from bookings.services import user_has_booking, workshop_has_available_places
from workshops.serializers import WorkshopSerializer


class BookingSerializer(serializers.ModelSerializer):
    workshop_detail = WorkshopSerializer(source="workshop", read_only=True)

    class Meta:
        model = Booking
        fields = ("id", "workshop", "workshop_detail", "created_at")
        read_only_fields = ("id", "workshop_detail", "created_at")

    def validate(self, attrs: dict) -> dict:
        request = self.context["request"]
        workshop = attrs.get("workshop", getattr(self.instance, "workshop", None))
        booking_id = getattr(self.instance, "id", None)
        booking_user = getattr(self.instance, "user", request.user)

        if user_has_booking(booking_user, workshop, booking_id):
            raise serializers.ValidationError(
                {"workshop": "Вы уже забронировали этот мастер-класс."}
            )

        if not workshop_has_available_places(workshop, booking_id):
            raise serializers.ValidationError(
                {"workshop": "На этот мастер-класс больше нет свободных мест."}
            )

        return attrs
