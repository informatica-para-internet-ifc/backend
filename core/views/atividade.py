from django.db import models
from django.http import HttpResponse
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from core.models import Atividade, Bloco
from core.serializers import AtividadeSerializer, BlocoSerializer


class BlocoViewSet(ModelViewSet):
    queryset = Bloco.objects.select_related('atividade').all()
    serializer_class = BlocoSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAuthenticated()]

    def get_queryset(self):
        qs = super().get_queryset()
        atividade = self.request.query_params.get('atividade')
        if atividade:
            qs = qs.filter(atividade_id=atividade)
        return qs


class AtividadeViewSet(ModelViewSet):
    queryset = (
        Atividade.objects.select_related('ano', 'disciplina', 'autor')
        .prefetch_related('blocos')
        .all()
    )
    serializer_class = AtividadeSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'exportar']:
            return [AllowAny()]
        return [IsAuthenticated()]

    def get_queryset(self):
        qs = super().get_queryset()
        params = self.request.query_params

        disciplina = params.get('disciplina')
        if disciplina:
            qs = qs.filter(disciplina__slug=disciplina)

        ano = params.get('ano')
        if ano:
            qs = qs.filter(ano_id=ano)

        status_f = params.get('status')
        if status_f:
            qs = qs.filter(status=status_f)

        categoria = params.get('categoria')
        if categoria:
            qs = qs.filter(categoria=categoria)

        autor = params.get('autor')
        if autor:
            qs = qs.filter(autor_id=autor)

        return qs

    def perform_create(self, serializer):
        serializer.save(autor=self.request.user)

    @extend_schema(
        methods=['GET'],
        summary="Listar blocos de uma atividade",
        responses={200: BlocoSerializer(many=True)},
    )
    @extend_schema(
        methods=['POST'],
        summary="Criar blocos em uma atividade",
        request=BlocoSerializer(many=True),
        responses={201: BlocoSerializer(many=True)},
    )
    @action(detail=True, methods=['get', 'post'])
    def blocos(self, request, pk=None):
        atividade = self.get_object()

        if request.method == 'GET':
            blocos = atividade.blocos.all().order_by('ordem')
            serializer = BlocoSerializer(blocos, many=True)
            return Response(serializer.data)

        serializer = BlocoSerializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        inicio = atividade.blocos.aggregate(max=models.Max('ordem')).get('ordem__max') or -1
        for offset, bloco in enumerate(serializer.validated_data):
            bloco['ordem'] = bloco.get('ordem', inicio + 1 + offset)
            Bloco.objects.create(atividade=atividade, **bloco)
        blocos = atividade.blocos.all().order_by('ordem')
        out = BlocoSerializer(blocos, many=True)
        return Response(out.data, status=status.HTTP_201_CREATED)

    @extend_schema(
        summary="Duplicar atividade",
        description="Copia a atividade com todos os blocos e metadados como rascunho.",
        responses={201: AtividadeSerializer},
    )
    @action(detail=True, methods=['post'])
    def duplicar(self, request, pk=None):
        original = self.get_object()
        copia = Atividade(
            titulo=f'Cópia de {original.titulo}',
            descricao=original.descricao,
            ano=original.ano,
            disciplina=original.disciplina,
            autor=request.user,
            categoria=original.categoria,
            dificuldade=original.dificuldade,
            tempo_estimado=original.tempo_estimado,
            tags=original.tags,
            pre_requisitos=original.pre_requisitos,
            prazo_recomendado=original.prazo_recomendado,
            status=Atividade.Status.RASCUNHO,
        )
        copia.save()
        for ordem, bloco in enumerate(original.blocos.all().order_by('ordem')):
            Bloco.objects.create(
                atividade=copia,
                tipo=bloco.tipo,
                ordem=ordem,
                dados=bloco.dados,
            )
        serializer = AtividadeSerializer(copia, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @extend_schema(
        summary="Exportar atividade",
        description="Exporta a atividade em Markdown ou PDF.",
        parameters=[OpenApiParameter('formato', str)],
        responses={200: str},
    )
    @action(detail=True, methods=['get'])
    def exportar(self, request, pk=None):
        atividade = self.get_object()
        formato = request.query_params.get('formato', 'markdown')

        if formato == 'pdf':
            return Response(
                {'detail': 'Exportação em PDF ainda não está disponível.'},
                status=status.HTTP_501_NOT_IMPLEMENTED,
            )

        md = [f'# {atividade.titulo}']
        if atividade.descricao:
            md.extend(['', atividade.descricao])
        md.append('')

        for bloco in atividade.blocos.all().order_by('ordem'):
            dados = bloco.dados or {}
            tipo = bloco.tipo
            if tipo == 'text':
                md.extend([dados.get('content', ''), ''])
            elif tipo == 'heading':
                level = dados.get('level', 2)
                md.extend([f"{'#' * level} {dados.get('content', '')}", ''])
            elif tipo == 'markdown':
                md.extend([dados.get('content', ''), ''])
            elif tipo == 'code':
                lang = dados.get('language', '')
                md.extend([f'```{lang}', dados.get('content', ''), '```', ''])
            elif tipo == 'list':
                marker = dados.get('ordered', False)
                for idx, item in enumerate(dados.get('items', [])):
                    md.append(f'{idx + 1}. {item}' if marker else f'- {item}')
                md.append('')
            elif tipo == 'quote':
                md.extend([f'> {dados.get("content", "")}', ''])
            elif tipo == 'question':
                modo = dados.get('modo', 'discursiva')
                md.extend([f'### Questão: {dados.get("enunciado", "")}'])
                if modo == 'multipla_escolha':
                    for ai, alt in enumerate(dados.get('alternativas', [])):
                        marca = '(x)' if ai == dados.get('correta') else '( )'
                        md.append(f'- {marca} {alt.get("texto", "")}')
                elif modo == 'verdadeiro_falso':
                    md.append(f'Resposta: {"Verdadeiro" if dados.get("respostaVf") else "Falso"}')
                elif modo == 'programacao':
                    md.extend([f'```{dados.get("linguagem", "")}', dados.get('codigoEsperado', ''), '```'])
                md.append('')
            elif tipo == 'divider':
                md.extend(['---', ''])
            else:
                md.append('')

        return HttpResponse('\n'.join(md).strip(), content_type='text/markdown; charset=utf-8')

    @extend_schema(
        summary="Importar atividade a partir de Markdown",
        description="Converte texto Markdown em blocos e cria a atividade como rascunho.",
        responses={201: AtividadeSerializer},
    )
    @action(detail=False, methods=['post'])
    def importar(self, request):
        titulo = request.data.get('titulo') or 'Atividade importada'
        disciplina_slug = request.data.get('disciplina')
        ano_id = request.data.get('ano')

        from core.models import Disciplina

        try:
            disciplina = Disciplina.objects.get(slug=disciplina_slug)
        except Disciplina.DoesNotExist:
            return Response(
                {'disciplina': 'Disciplina inválida.'}, status=status.HTTP_400_BAD_REQUEST
            )
        if ano_id and int(ano_id) != disciplina.ano_id:
            return Response(
                {'ano': 'O ano informado não corresponde à disciplina.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        ano = disciplina.ano

        markdown = request.data.get('markdown', '')
        if not markdown:
            return Response(
                {'markdown': 'Informe o conteúdo em Markdown.'}, status=status.HTTP_400_BAD_REQUEST
            )

        blocos = self._markdown_para_blocos(markdown)
        atividade = Atividade.objects.create(
            titulo=titulo,
            ano=ano,
            disciplina=disciplina,
            autor=request.user,
            status=Atividade.Status.RASCUNHO,
        )
        for ordem, bloco in enumerate(blocos):
            Bloco.objects.create(atividade=atividade, ordem=ordem, **bloco)

        serializer = AtividadeSerializer(atividade, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @staticmethod
    def _markdown_para_blocos(markdown):
        blocos = []
        lines = markdown.splitlines()
        i = 0
        while i < len(lines):
            line = lines[i].rstrip()

            if not line.strip():
                i += 1
                continue

            if line.strip().startswith('```'):
                lang = line.strip()[3:].strip()
                codigo = []
                i += 1
                while i < len(lines) and not lines[i].strip().startswith('```'):
                    codigo.append(lines[i])
                    i += 1
                i += 1  # pula a linha do ``` final
                blocos.append({'tipo': 'code', 'dados': {'content': '\n'.join(codigo), 'language': lang}})
                continue

            if line.startswith('#'):
                level = len(line) - len(line.lstrip('#'))
                blocos.append({'tipo': 'heading', 'dados': {'content': line.lstrip('# ').strip(), 'level': min(level, 6)}})
                i += 1
                continue

            if line.startswith('- ') or line.startswith('* '):
                itens = []
                while i < len(lines) and lines[i].strip().startswith(('- ', '* ')):
                    itens.append(lines[i].strip()[2:].strip())
                    i += 1
                blocos.append({'tipo': 'list', 'dados': {'items': itens, 'ordered': False}})
                continue

            if line.startswith('> '):
                blocos.append({'tipo': 'quote', 'dados': {'content': line[2:].strip(), 'author': ''}})
                i += 1
                continue

            paragrafo = [line]
            i += 1
            while i < len(lines) and lines[i].strip() and not lines[i].startswith(('#', '- ', '* ', '> ', '```')):
                paragrafo.append(lines[i].strip())
                i += 1
            blocos.append({'tipo': 'text', 'dados': {'content': ' '.join(paragrafo)}})

        return blocos
