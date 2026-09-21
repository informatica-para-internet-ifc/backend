import magic

CONTENT_TYPE_ICO = "image/x-icon"
CONTENT_TYPE_JPG = "image/jpeg"
CONTENT_TYPE_PNG = "image/png"
CONTENT_TYPE_WEBP = "image/webp"
CONTENT_TYPE_GIF = "image/gif"

CONTENT_TYPE_PDF = "application/pdf"
CONTENT_TYPE_DOC = "application/msword"
CONTENT_TYPE_DOCX = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
CONTENT_TYPE_XLS = "application/vnd.ms-excel"
CONTENT_TYPE_XLSX = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
CONTENT_TYPE_PPT = "application/vnd.ms-powerpoint"
CONTENT_TYPE_PPTX = "application/vnd.openxmlformats-officedocument.presentationml.presentation"
CONTENT_TYPE_ZIP = "application/zip"
CONTENT_TYPE_TXT = "text/plain"

CONTENT_TYPE_MP4 = "video/mp4"
CONTENT_TYPE_WEBM = "video/webm"
CONTENT_TYPE_MOV = "video/quicktime"
CONTENT_TYPE_AVI = "video/x-msvideo"
CONTENT_TYPE_MKV = "video/x-matroska"

DOCUMENT_CONTENT_TYPES = [
    CONTENT_TYPE_PDF,
    CONTENT_TYPE_DOC,
    CONTENT_TYPE_DOCX,
    CONTENT_TYPE_XLS,
    CONTENT_TYPE_XLSX,
    CONTENT_TYPE_PPT,
    CONTENT_TYPE_PPTX,
    CONTENT_TYPE_ZIP,
    CONTENT_TYPE_TXT,
]

IMAGE_CONTENT_TYPES = [
    CONTENT_TYPE_JPG,
    CONTENT_TYPE_PNG,
    CONTENT_TYPE_WEBP,
    CONTENT_TYPE_GIF,
]

VIDEO_CONTENT_TYPES = [
    CONTENT_TYPE_MP4,
    CONTENT_TYPE_WEBM,
    CONTENT_TYPE_MOV,
    CONTENT_TYPE_AVI,
    CONTENT_TYPE_MKV,
]


def get_content_type(file):
    if hasattr(file, "temporary_file_path"):
        content_type = magic.from_file(file.temporary_file_path(), mime=True)
    else:
        content_type = magic.from_buffer(file.read(), mime=True)

    if hasattr(file, "seek") and callable(file.seek):
        file.seek(0)

    return content_type
