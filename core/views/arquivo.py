from drf_spectacular.utils import extend_schema
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from core.models import Arquivo
from core.serializers import ArquivoSerializer


class ArquivoViewSet(ModelViewSet):
    queryset = Arquivo.objects.all()
    serializer_class = ArquivoSerializer
    parser_classes = [MultiPartParser, FormParser]

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        arquivo = serializer.save()
        return Response(self.get_serializer(arquivo).data, status=201)

    @extend_schema(
        summary="Baixar arquivo",
        description="Download público de um arquivo anexado.",
    )
    def retrieve(self, request, *args, **kwargs):
        arquivo = self.get_object()
        from django.http import FileResponse

        return FileResponse(arquivo.arquivo, as_attachment=True, filename=arquivo.nome)
