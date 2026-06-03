from datetime import timedelta

from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from workshops.models import Workshop


User = get_user_model()


class WorkshopBookingApiTests(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(
            username="user",
            password="password12345",
        )
        self.other_user = User.objects.create_user(
            username="other",
            password="password12345",
        )
        self.admin = User.objects.create_user(
            username="admin",
            password="password12345",
            role=User.Role.ADMIN,
        )
        self.workshop = Workshop.objects.create(
            title="Python basics",
            description="Intro workshop",
            starts_at=timezone.now() + timedelta(days=1),
            duration_minutes=90,
            capacity=2,
            created_by=self.admin,
        )

    def workshop_payload(self) -> dict:
        return {
            "title": "Django REST",
            "description": "API workshop",
            "starts_at": (timezone.now() + timedelta(days=2)).isoformat(),
            "duration_minutes": 120,
            "capacity": 10,
        }

    def test_anonymous_user_can_view_workshops(self):
        response = self.client.get(reverse("workshop-list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["title"], self.workshop.title)

    def test_regular_user_cannot_create_workshop(self):
        self.client.force_authenticate(self.user)

        response = self.client.post(
            reverse("workshop-list"),
            self.workshop_payload(),
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_create_workshop(self):
        self.client.force_authenticate(self.admin)

        response = self.client.post(
            reverse("workshop-list"),
            self.workshop_payload(),
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["created_by"], self.admin.username)

    def test_user_can_create_booking_once(self):
        self.client.force_authenticate(self.user)

        first_response = self.client.post(
            reverse("booking-list"),
            {"workshop": self.workshop.id},
            format="json",
        )
        second_response = self.client.post(
            reverse("booking-list"),
            {"workshop": self.workshop.id},
            format="json",
        )

        self.assertEqual(first_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(second_response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_sees_only_own_bookings(self):
        self.client.force_authenticate(self.other_user)
        self.client.post(
            reverse("booking-list"),
            {"workshop": self.workshop.id},
            format="json",
        )

        self.client.force_authenticate(self.user)
        self.client.post(
            reverse("booking-list"),
            {"workshop": self.workshop.id},
            format="json",
        )
        response = self.client.get(reverse("booking-list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
