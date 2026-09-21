import mimetypes
from pathlib import Path

from django.http import FileResponse
from rest_framework import mixins, parsers, viewsets

from uploader.models import Document, Image, Video
from uploader.serializers import DocumentUploadSerializer, ImageUploadSerializer, VideoUploadSerializer


class CreateViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    pass


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
