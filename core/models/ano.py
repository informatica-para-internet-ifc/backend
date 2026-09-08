"""
Database models.
"""

from django.db import models
from django.utils.translation import gettext_lazy as _


class Ano(models.Model):
    """Ano do curso (1º, 2º ou 3º)."""

    numero = models.PositiveSmallIntegerField(unique=True, verbose_name=_('Número do ano'))
    descricao = models.TextField(blank=True, verbose_name=_('Descrição'))

    class Meta:
        ordering = ['numero']
        verbose_name = 'Ano'
        verbose_name_plural = 'Anos'

    def __str__(self):
        return f'{self.numero}º Ano'
