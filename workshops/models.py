from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models


class Workshop(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    starts_at = models.DateTimeField()
    duration_minutes = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
    )
    capacity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_workshops",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["starts_at", "title"]
        constraints = [
            models.CheckConstraint(
                check=models.Q(capacity__gte=1),
                name="workshop_capacity_gte_1",
            ),
            models.CheckConstraint(
                check=models.Q(duration_minutes__gte=1),
                name="workshop_duration_gte_1",
            ),
        ]

    def __str__(self) -> str:
        return self.title
