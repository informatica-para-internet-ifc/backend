"""
WSGI config for app project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')

application = get_wsgi_application()

# A plataforma de deploy não executa a fase "release" do Procfile (o
# `python manage.py migrate` de lá nunca chega a rodar), então as
# migrações são aplicadas aqui, automaticamente, sempre que um worker
# do gunicorn sobe. O Django protege `migrate` contra execução
# concorrente entre múltiplos workers, então é seguro mesmo com mais
# de um worker inicializando ao mesmo tempo.
print('=' * 70, flush=True)
print('APLICANDO MIGRAÇÕES DO BANCO DE DADOS (auto, no boot do app)', flush=True)
print('=' * 70, flush=True)
try:
    from django.core.management import call_command

    call_command('migrate', interactive=False, verbosity=2)
    print('MIGRAÇÕES: concluído com sucesso.', flush=True)
except Exception as exc:  # pylint: disable=broad-except
    print(f'MIGRAÇÕES: FALHOU -> {exc!r}', flush=True)
print('=' * 70, flush=True)
