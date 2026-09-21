from django.db.models import Q
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from core.models import Atividade
from core.serializers import AtividadeSerializer


@extend_schema(
    summary="Buscar atividades",
    description=(
        "Busca por título, descrição, tags e conteúdo. Filtros opcionais: "
        "disciplina, dificuldade, ano."
    ),
    parameters=[
        OpenApiParameter('q', str),
        OpenApiParameter('disciplina', str),
        OpenApiParameter('dificuldade', str),
        OpenApiParameter('ano', int),
    ],
)
class BuscaView(ListAPIView):
    serializer_class = AtividadeSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        qs = (
            Atividade.objects.select_related('ano', 'disciplina', 'autor')
            .prefetch_related('blocos')
            .all()
        )

        termo = self.request.query_params.get('q', '').strip()
        if len(termo) >= 2:
            qs = qs.filter(
                Q(titulo__icontains=termo)
                | Q(descricao__icontains=termo)
                | Q(tags__icontains=termo)
                | Q(blocos__dados__icontains=termo)
            ).distinct()

        disciplina = self.request.query_params.get('disciplina')
        if disciplina:
            qs = qs.filter(disciplina__slug=disciplina)

        dificuldade = self.request.query_params.get('dificuldade')
        if dificuldade:
            qs = qs.filter(dificuldade=dificuldade)

        ano = self.request.query_params.get('ano')
        if ano:
            qs = qs.filter(ano_id=ano)

        return qs.order_by('-fixada', '-atualizado_em')

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = AtividadeSerializer(
            queryset, many=True, context={'request': request}
        )
        return Response(serializer.data)
