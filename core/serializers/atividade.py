from django.db import transaction
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from core.models import Atividade, Bloco, Disciplina


class BlocoSerializer(ModelSerializer):
    class Meta:
        model = Bloco
        fields = ['id', 'atividade', 'tipo', 'ordem', 'dados']
        read_only_fields = ['id', 'atividade']
        extra_kwargs = {'ordem': {'required': False, 'default': 0}}


class BlocoNestedSerializer(ModelSerializer):
    class Meta:
        model = Bloco
        fields = ['id', 'tipo', 'ordem', 'dados']
        read_only_fields = ['id']
        extra_kwargs = {'ordem': {'required': False, 'default': 0}}


class AtividadeSerializer(ModelSerializer):
    blocos = BlocoNestedSerializer(many=True, required=False)
    disciplina = serializers.SlugRelatedField(slug_field='slug', queryset=Disciplina.objects.all())
    autor = serializers.PrimaryKeyRelatedField(read_only=True)
    autor_nome = serializers.CharField(source='autor.name', read_only=True)
    disciplina_slug = serializers.CharField(source='disciplina.slug', read_only=True)
    ano_numero = serializers.IntegerField(source='ano.numero', read_only=True)

    class Meta:
        model = Atividade
        fields = [
            'id',
            'titulo',
            'descricao',
            'ano',
            'disciplina',
            'autor',
            'autor_nome',
            'disciplina_slug',
            'ano_numero',
            'dificuldade',
            'tempo_estimado',
            'tags',
            'pre_requisitos',
            'data_publicacao',
            'prazo_recomendado',
            'fixada',
            'status',
            'criado_em',
            'atualizado_em',
            'blocos',
        ]
        read_only_fields = ['id', 'autor', 'criado_em', 'atualizado_em']

    def validate(self, attrs):
        ano = attrs.get('ano', getattr(self.instance, 'ano', None))
        disciplina = attrs.get('disciplina', getattr(self.instance, 'disciplina', None))
        if ano and disciplina and disciplina.ano_id != ano.id:
            raise serializers.ValidationError(
                {'disciplina': 'A disciplina não pertence ao ano informado.'}
            )

        fixada = attrs.get('fixada', getattr(self.instance, 'fixada', False))
        status = attrs.get('status', getattr(self.instance, 'status', None))
        if fixada and status != Atividade.Status.PUBLICADA:
            raise serializers.ValidationError(
                {'fixada': 'Apenas atividades publicadas podem ser fixadas.'}
            )
        return attrs

    @transaction.atomic
    def create(self, validated_data):
        blocos = validated_data.pop('blocos', [])
        atividade = Atividade.objects.create(**validated_data)
        self._set_blocos(atividade, blocos)
        return atividade

    @transaction.atomic
    def update(self, instance, validated_data):
        blocos = validated_data.pop('blocos', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if blocos is not None:
            self._set_blocos(instance, blocos)
        return instance

    @staticmethod
    def _set_blocos(atividade, blocos):
        atividade.blocos.all().delete()
        for ordem, bloco in enumerate(blocos):
            bloco.pop('ordem', None)
            Bloco.objects.create(atividade=atividade, ordem=ordem, **bloco)
