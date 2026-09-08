from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from core.models import Disciplina


class DisciplinaSerializer(ModelSerializer):
    ano_numero = serializers.IntegerField(source='ano.numero', read_only=True)

    class Meta:
        model = Disciplina
        fields = ['id', 'slug', 'nome', 'descricao', 'icone', 'ano', 'ano_numero']
