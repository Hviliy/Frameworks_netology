from rest_framework import serializers

from workshops.models import Workshop


class WorkshopSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Workshop
        fields = (
            "id",
            "title",
            "description",
            "starts_at",
            "duration_minutes",
            "capacity",
            "created_by",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "created_by", "created_at", "updated_at")
