from django.db import models


class StoredFile(models.Model):
    """Conteúdo binário de um arquivo enviado, guardado no próprio banco."""

    name = models.CharField(max_length=500, unique=True)
    content = models.BinaryField()
    content_type = models.CharField(max_length=127, default='application/octet-stream')
    size = models.PositiveBigIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name
