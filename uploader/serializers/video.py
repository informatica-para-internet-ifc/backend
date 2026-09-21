from rest_framework import serializers

from uploader.helpers.files import VIDEO_CONTENT_TYPES, get_content_type
from uploader.models import Video


class VideoUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ["attachment_key", "file", "description", "uploaded_on", "url"]
        read_only_fields = ["attachment_key", "uploaded_on", "url"]
        extra_kwargs = {"file": {"write_only": True}}

    def validate_file(self, value):
        if get_content_type(value) not in VIDEO_CONTENT_TYPES:
            raise serializers.ValidationError("Invalid or corrupted video.")
        return value


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ["url", "description", "uploaded_on", "attachment_key", "public_id"]
        read_only_fields = ["url", "attachment_key", "uploaded_on"]

    def create(self, validated_data):
        raise NotImplementedError("Use VideoUploadSerializer to create video files.")
