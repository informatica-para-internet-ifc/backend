from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from core.models import Ano, Disciplina


class DisciplinaResumidaSerializer(ModelSerializer):
    class Meta:
        model = Disciplina
        fields = ['id', 'slug', 'nome', 'descricao', 'icone']


class AnoSerializer(ModelSerializer):
    disciplinas = DisciplinaResumidaSerializer(many=True, read_only=True)

    class Meta:
        model = Ano
        fields = ['id', 'numero', 'descricao', 'disciplinas']
