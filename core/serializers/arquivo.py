from pathlib import Path

from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from core.models import Arquivo


class ArquivoSerializer(ModelSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = Arquivo
        fields = ['id', 'atividade', 'nome', 'tipo_arquivo', 'tamanho', 'criado_em', 'url']
        read_only_fields = ['id', 'nome', 'tipo_arquivo', 'tamanho', 'criado_em', 'url']

    def get_url(self, obj):
        request = self.context.get('request')
        if not obj.arquivo:
            return None
        if request is not None:
            return request.build_absolute_uri(obj.arquivo.url)
        return obj.arquivo.url

    def create(self, validated_data):
        arquivo = validated_data['arquivo']
        nome = getattr(arquivo, 'name', '') or ''
        ext = Path(nome).suffix.lstrip('.').lower()
        validated_data['nome'] = Path(nome).stem or nome
        validated_data['tipo_arquivo'] = ext
        validated_data['tamanho'] = arquivo.size or 0
        return super().create(validated_data)
