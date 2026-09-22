import mimetypes

from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import Storage
from django.utils.deconstruct import deconstructible


@deconstructible
class DatabaseStorage(Storage):
    """Guarda os arquivos enviados numa tabela do banco de dados.

    O disco do container é apagado a cada deploy, mas o banco (Postgres)
    persiste. Os arquivos são servidos por uploader.views.serve_stored_file.
    """

    @staticmethod
    def _normalize(name: str) -> str:
        return str(name).replace('\\', '/').lstrip('/')

    def _model(self):
        from uploader.models import StoredFile

        return StoredFile

    def _open(self, name, mode='rb'):
        try:
            stored = self._model().objects.get(name=self._normalize(name))
        except self._model().DoesNotExist as exc:
            raise FileNotFoundError(name) from exc
        return ContentFile(bytes(stored.content), name=stored.name)

    def _save(self, name, content):
        name = self._normalize(name)
        content.seek(0)
        data = content.read()
        content_type = (
            getattr(content, 'content_type', None)
            or mimetypes.guess_type(name)[0]
            or 'application/octet-stream'
        )
        self._model().objects.update_or_create(
            name=name,
            defaults={'content': data, 'content_type': content_type, 'size': len(data)},
        )
        return name

    def exists(self, name):
        return self._model().objects.filter(name=self._normalize(name)).exists()

    def delete(self, name):
        self._model().objects.filter(name=self._normalize(name)).delete()

    def size(self, name):
        return self._model().objects.values_list('size', flat=True).get(name=self._normalize(name))

    def url(self, name):
        return f'{settings.BACKEND_URL}/media/{self._normalize(name)}'
