"""
Database models.
"""

from django.db import models
from django.utils.translation import gettext_lazy as _

from uploader.helpers.storage import raw_storage

from .atividade import Atividade


class Arquivo(models.Model):
    """Arquivo anexado a uma atividade (download público)."""

    atividade = models.ForeignKey(
        Atividade,
        on_delete=models.CASCADE,
        related_name='arquivos',
        null=True,
        blank=True,
        verbose_name=_('Atividade'),
    )
    arquivo = models.FileField(upload_to='arquivos/%Y/%m/', storage=raw_storage, verbose_name=_('Arquivo'))
    nome = models.CharField(max_length=200, verbose_name=_('Nome de exibição'))
    tipo_arquivo = models.CharField(max_length=10, blank=True, verbose_name=_('Extensão'))
    tamanho = models.PositiveBigIntegerField(default=0, verbose_name=_('Tamanho em bytes'))
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-criado_em']
        verbose_name = 'Arquivo'
        verbose_name_plural = 'Arquivos'

    def __str__(self):
        return self.nome
