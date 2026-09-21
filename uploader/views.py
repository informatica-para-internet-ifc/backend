import mimetypes
from pathlib import Path

import re

from django.http import FileResponse, Http404, HttpResponse
from django.views.decorators.http import require_GET
from rest_framework import mixins, parsers, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated

from uploader.models import Document, Image, StoredFile, Video
from uploader.serializers import DocumentUploadSerializer, ImageUploadSerializer, VideoUploadSerializer


class CreateViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    def get_permissions(self):
        if self.action == 'create':
            return [IsAuthenticated()]
        return [AllowAny()]


_RANGE_RE = re.compile(r'bytes=(\d*)-(\d*)')


@require_GET
def serve_stored_file(request, path):
    """Serve um arquivo guardado no banco (imagens, vídeos, documentos)."""
    try:
        stored = StoredFile.objects.get(name=path)
    except StoredFile.DoesNotExist as exc:
        raise Http404 from exc

    data = bytes(stored.content)
    total = len(data)
    status = 200
    headers = {'Accept-Ranges': 'bytes', 'Cache-Control': 'public, max-age=31536000, immutable'}

    match = _RANGE_RE.fullmatch(request.headers.get('Range', '').strip())
    if match and (match.group(1) or match.group(2)):
        if match.group(1):
            start = int(match.group(1))
            end = min(int(match.group(2)), total - 1) if match.group(2) else total - 1
        else:
            start = max(total - int(match.group(2)), 0)
            end = total - 1
        if start > end or start >= total:
            return HttpResponse(status=416, headers={'Content-Range': f'bytes */{total}'})
        data = data[start:end + 1]
        status = 206
        headers['Content-Range'] = f'bytes {start}-{end}/{total}'

    response = HttpResponse(data, status=status, content_type=stored.content_type)
    for key, value in headers.items():
        response[key] = value
    return response


class DocumentUploadViewSet(CreateViewSet, mixins.RetrieveModelMixin):
    queryset = Document.objects.all() #  pylint: disable=no-member
    serializer_class = DocumentUploadSerializer
    parser_classes = [parsers.FormParser, parsers.MultiPartParser]

    def retrieve(self, request, *args, **kwargs):
        document = self.get_object()
        extension = Path(document.file.name).suffix
        content_type = mimetypes.guess_type(document.file.name)[0] or 'application/octet-stream'
        filename = f"{document.description or document.public_id}{extension}"
        return FileResponse(
            document.file.open('rb'),
            as_attachment=True,
            filename=filename,
            content_type=content_type,
        )


class ImageUploadViewSet(CreateViewSet):
    queryset = Image.objects.all() #  pylint: disable=no-member
    serializer_class = ImageUploadSerializer
    parser_classes = [parsers.FormParser, parsers.MultiPartParser]


class VideoUploadViewSet(CreateViewSet):
    queryset = Video.objects.all() #  pylint: disable=no-member
    serializer_class = VideoUploadSerializer
    parser_classes = [parsers.FormParser, parsers.MultiPartParser]
