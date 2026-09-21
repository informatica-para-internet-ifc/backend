from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ReadOnlyModelViewSet

from core.models import Ano
from core.serializers import AnoSerializer


class AnoViewSet(ReadOnlyModelViewSet):
    queryset = Ano.objects.prefetch_related('disciplinas').all()
    serializer_class = AnoSerializer
    permission_classes = [AllowAny]
