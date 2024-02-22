from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile


def in_memory_uploaded_file_to_bytes(file):
    file_name: str = file.name
    file.seek(0)
    file_data: bytes = file.read()
    return file_data, file_name


def bytes_to_in_memory_uploaded_file(file_data, file_name, content_type):
    buffer = BytesIO(file_data)
    file = InMemoryUploadedFile(
        buffer, None, file_name, content_type, buffer.tell(), None
    )
    return file
