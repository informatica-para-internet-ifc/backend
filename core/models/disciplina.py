"""
Database models.
"""

from django.db import models
from django.utils.translation import gettext_lazy as _

from .ano import Ano


class Disciplina(models.Model):
    """Disciplina pertencente a um ano do curso."""

    ano = models.ForeignKey(Ano, on_delete=models.CASCADE, related_name='disciplinas')
    slug = models.SlugField(max_length=50, unique=True, verbose_name=_('Slug'))
    nome = models.CharField(max_length=120, verbose_name=_('Nome'))
    descricao = models.TextField(blank=True, verbose_name=_('Descrição'))
    icone = models.CharField(max_length=50, blank=True, verbose_name=_('Ícone (@mdi)'))

    class Meta:
        ordering = ['ano', 'nome']
        unique_together = ('ano', 'nome')
        verbose_name = 'Disciplina'
        verbose_name_plural = 'Disciplinas'

    def __str__(self):
        return f'{self.ano} · {self.nome}'
