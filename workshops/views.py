from rest_framework import viewsets

from workshops.models import Workshop
from workshops.permissions import IsAdminRoleOrReadOnly
from workshops.serializers import WorkshopSerializer


class WorkshopViewSet(viewsets.ModelViewSet):
    queryset = Workshop.objects.select_related("created_by")
    serializer_class = WorkshopSerializer
    permission_classes = (IsAdminRoleOrReadOnly,)

    def perform_create(self, serializer) -> None:
        serializer.save(created_by=self.request.user)
