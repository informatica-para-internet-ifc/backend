from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ReadOnlyModelViewSet

from core.models import Disciplina
from core.serializers import DisciplinaSerializer


class DisciplinaViewSet(ReadOnlyModelViewSet):
    queryset = Disciplina.objects.select_related('ano').all()
    serializer_class = DisciplinaSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        qs = super().get_queryset()
        ano = self.request.query_params.get('ano')
        if ano:
            qs = qs.filter(ano_id=ano)
        return qs
