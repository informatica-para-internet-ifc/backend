"""
Database models.
"""

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from .ano import Ano
from .disciplina import Disciplina


class Atividade(models.Model):
    """Atividade acadêmica com blocos de conteúdo."""

    class Dificuldade(models.TextChoices):
        FACIL = 'facil', 'Fácil'
        MEDIO = 'medio', 'Médio'
        DIFICIL = 'dificil', 'Difícil'

    class Status(models.TextChoices):
        RASCUNHO = 'rascunho', 'Rascunho'
        PUBLICADA = 'publicada', 'Publicada'
        ARQUIVADA = 'arquivada', 'Arquivada'

    titulo = models.CharField(max_length=200, verbose_name=_('Título'))
    descricao = models.TextField(blank=True, verbose_name=_('Descrição'))
    ano = models.ForeignKey(Ano, on_delete=models.PROTECT, related_name='atividades')
    disciplina = models.ForeignKey(Disciplina, on_delete=models.PROTECT, related_name='atividades')
    autor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='atividades',
        verbose_name=_('Autor'),
    )

    dificuldade = models.CharField(max_length=10, choices=Dificuldade.choices, blank=True)
    tempo_estimado = models.CharField(max_length=40, blank=True, verbose_name=_('Tempo estimado'))
    tags = models.JSONField(default=list, blank=True)
    pre_requisitos = models.TextField(blank=True)

    data_publicacao = models.DateTimeField(null=True, blank=True, verbose_name=_('Programar publicação'))
    prazo_recomendado = models.DateField(null=True, blank=True, verbose_name=_('Prazo recomendado'))
    fixada = models.BooleanField(default=False, verbose_name=_('Fixar atividade'))
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.RASCUNHO)

    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-fixada', '-atualizado_em']
        verbose_name = 'Atividade'
        verbose_name_plural = 'Atividades'

    def __str__(self):
        return self.titulo
