"""
Django admin customization.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from core import models


class UserAdmin(BaseUserAdmin):
    """Define the admin pages for users."""

    ordering = ('id',)
    list_display = ('email', 'name')
    search_fields = ('email', 'name', 'groups__name')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal Info'), {'fields': ('name',)}),
        (
            _('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                )
            },
        ),
        (_('Important dates'), {'fields': ('last_login',)}),
        (_('Groups'), {'fields': ('groups',)}),
        (_('User Permissions'), {'fields': ('user_permissions',)}),
    )
    readonly_fields = ['last_login']
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': (
                    'email',
                    'password1',
                    'password2',
                    'name',
                    'is_active',
                    'is_staff',
                    'is_superuser',
                ),
            },
        ),
    )


class DisciplinaInline(admin.TabularInline):
    model = models.Disciplina
    extra = 0


class BlocoInline(admin.TabularInline):
    model = models.Bloco
    extra = 0
    fields = ('tipo', 'ordem', 'dados')


@admin.register(models.Ano)
class AnoAdmin(admin.ModelAdmin):
    list_display = ('numero', 'descricao')
    search_fields = ('numero', 'descricao')
    inlines = [DisciplinaInline]


@admin.register(models.Disciplina)
class DisciplinaAdmin(admin.ModelAdmin):
    list_display = ('slug', 'nome', 'ano', 'icone')
    list_filter = ('ano',)
    search_fields = ('nome', 'slug', 'descricao')
    list_editable = ('icone',)


@admin.register(models.Atividade)
class AtividadeAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'disciplina', 'ano', 'autor', 'categoria', 'status', 'dificuldade', 'fixada', 'atualizado_em')
    list_filter = ('categoria', 'status', 'dificuldade', 'ano', 'disciplina', 'fixada')
    search_fields = ('titulo', 'descricao', 'tags')
    date_hierarchy = 'criado_em'
    inlines = [BlocoInline]


@admin.register(models.Bloco)
class BlocoAdmin(admin.ModelAdmin):
    list_display = ('atividade', 'tipo', 'ordem')
    list_filter = ('tipo',)
    search_fields = ('atividade__titulo',)


@admin.register(models.Arquivo)
class ArquivoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'atividade', 'tipo_arquivo', 'tamanho', 'criado_em')
    search_fields = ('nome',)
    list_filter = ('tipo_arquivo',)


admin.site.register(models.User, UserAdmin)
