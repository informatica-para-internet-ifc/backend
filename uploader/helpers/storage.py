from django.conf import settings
from django.core.files.storage import FileSystemStorage

# The project's default storage (settings.STORAGES['default']) is Cloudinary
# whenever CLOUDINARY_URL is set, so django.core.files.storage.default_storage
# is NOT local disk in that case. Local fallbacks must use an explicit
# FileSystemStorage instance instead.
_local_storage = FileSystemStorage()


def raw_storage():
    """Storage for arbitrary downloadable files (PDF, DOCX, ZIP...).

    Many Cloudinary accounts block public delivery of raw/PDF/ZIP files by
    default ("Restricted media types" in the console's Security settings),
    which makes uploads succeed but downloads return 401 "deny or ACL
    failure" regardless of resource_type or URL signing. Until that setting
    is enabled on the account, raw documents are kept on local disk (served
    directly by Django) so downloads actually work. Set
    CLOUDINARY_RAW_ENABLED=true in the environment once the Cloudinary
    account allows raw/PDF/ZIP delivery to switch documents back to
    Cloudinary storage.
    """
    if getattr(settings, "CLOUDINARY_URL", None) and getattr(settings, "CLOUDINARY_RAW_ENABLED", False):
        from cloudinary_storage.storage import RawMediaCloudinaryStorage

        return RawMediaCloudinaryStorage()
    return _local_storage


def video_storage():
    """Storage for video files, using Cloudinary's video resource type."""
    if getattr(settings, "CLOUDINARY_URL", None):
        from cloudinary_storage.storage import VideoMediaCloudinaryStorage

        return VideoMediaCloudinaryStorage()
    return _local_storage
