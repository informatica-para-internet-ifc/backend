"""
Database models.
"""

from django.db import models
from django.utils.translation import gettext_lazy as _

from .atividade import Atividade


class Bloco(models.Model):
    """Bloco de conteúdo de uma atividade."""

    class Tipo(models.TextChoices):
        TEXTO = 'text', 'Texto'
        TITULO = 'heading', 'Título'
        MARKDOWN = 'markdown', 'Markdown'
        CODIGO = 'code', 'Código'
        TERMINAL = 'terminal', 'Terminal'
        IMAGEM = 'image', 'Imagem'
        GALERIA = 'gallery', 'Galeria'
        VIDEO = 'video', 'Vídeo'
        EMBED = 'embed', 'Embed'
        LISTA = 'list', 'Lista'
        PASSOS = 'steps', 'Passo a Passo'
        CHECKLIST = 'checklist', 'Checklista'
        TABELA = 'table', 'Tabela'
        CITACAO = 'quote', 'Citação'
        AVISO = 'alert', 'Aviso'
        LINK = 'link', 'Link'
        LINKS = 'links', 'Links Externos'
        DOWNLOAD = 'file', 'Download'
        ACORDEAO = 'accordion', 'Acordeão'
        DIVISOR = 'divider', 'Divisor'
        QUESTAO = 'question', 'Questão'

    atividade = models.ForeignKey(Atividade, on_delete=models.CASCADE, related_name='blocos')
    tipo = models.CharField(max_length=20, choices=Tipo.choices)
    ordem = models.PositiveIntegerField(default=0)
    dados = models.JSONField(default=dict)

    class Meta:
        ordering = ['ordem']
        verbose_name = 'Bloco'
        verbose_name_plural = 'Blocos'

    def __str__(self):
        return f'{self.atividade.titulo} · {self.get_tipo_display()}'
