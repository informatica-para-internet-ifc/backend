from django.conf import settings

from uploader.storage import DatabaseStorage


def _cloudinary_enabled() -> bool:
    return bool(getattr(settings, "USE_CLOUDINARY", False))


def raw_storage():
    """Storage para arquivos baixáveis (PDF, DOCX, ZIP...).

    Por padrão os arquivos ficam no banco de dados (persistem entre deploys).
    Com USE_CLOUDINARY=true e CLOUDINARY_RAW_ENABLED=true, usa o Cloudinary.
    """
    if _cloudinary_enabled() and getattr(settings, "CLOUDINARY_RAW_ENABLED", False):
        from cloudinary_storage.storage import RawMediaCloudinaryStorage

        return RawMediaCloudinaryStorage()
    return DatabaseStorage()


def video_storage():
    """Storage para vídeos: banco de dados, ou Cloudinary com USE_CLOUDINARY=true."""
    if _cloudinary_enabled():
        from cloudinary_storage.storage import VideoMediaCloudinaryStorage

        return VideoMediaCloudinaryStorage()
    return DatabaseStorage()
