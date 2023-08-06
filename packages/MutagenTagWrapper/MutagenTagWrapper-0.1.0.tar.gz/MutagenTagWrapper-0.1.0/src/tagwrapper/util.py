from __future__ import annotations

import re
from typing import Any, Callable, IO

from mutagen import flac

HEADERS_MIMES_EXTS = {
    re.compile(b'^\xff\xd8\xff[\xdb\xe0\xee\xe1]'): ('image/jpeg', '.jpg'),
    re.compile(b'^\x89PNG\r\n\x1a\n'): ('image/png', '.png'),
    re.compile(b'^\x42\x4d'): ('image/bmp', '.bmp'),
    re.compile(b'^GIF8[79]a'): ('image/gif', '.gif'),
    re.compile(b'^\x49\x49\\x2a\x00'): ('image/tiff', '.tiff'),
    re.compile(b'^\x4d\x4d\x00\\x2a'): ('image/tiff', '.tiff'),
    re.compile(b'^RIFF.{4}WEBP'): ('image/webp', '.webp'),
    re.compile(b'FLIF'): ('image/flif', '.flif')
}


def verify_fileobj(obj: Any) -> None:
    if isinstance(obj, (str, bytes)) or hasattr(obj, '__fspath__'):
        raise ValueError(f"{repr(obj)} is not a file object")


def verify_readable(fileobj: IO[str] | IO[bytes], is_binary=True) -> None:
    verify_fileobj(fileobj)
    target_type = str
    if is_binary:
        target_type = bytes

    fileobj_readable: Callable[[], bool] | bool = getattr(fileobj, 'readable', None)
    if callable(fileobj_readable):
        if not fileobj_readable():
            raise ValueError(f"file {repr(fileobj)} is not readable")
    elif isinstance(fileobj, bool):
        if not fileobj_readable:
            raise ValueError(f"file {repr(fileobj)} is not readable")
    else:
        result = fileobj.read(0)
        if not isinstance(result, target_type):
            raise ValueError(
                f"incorrect type from file {repr(fileobj)} "
                f"(should be {target_type.__name__}, got {type(fileobj).__name__})"
            )


def verify_writable(fileobj: IO[str] | IO[bytes], is_binary=True) -> None:
    verify_fileobj(fileobj)
    target_type = str
    if is_binary:
        target_type = bytes

    fileobj_writable: Callable[[], bool] | bool = getattr(fileobj, 'writable', None)
    if callable(fileobj_writable):
        if not fileobj_writable():
            raise ValueError(f"file {repr(fileobj)} is not writable")
    elif isinstance(fileobj, bool):
        if not fileobj_writable:
            raise ValueError(f"file {repr(fileobj)} is not writable")
    else:
        fileobj.write(target_type())


def verify_seekable(fileobj: IO[str] | IO[bytes]) -> None:
    verify_fileobj(fileobj)

    fileobj_seekable: Callable[[], bool] | bool = getattr(fileobj, 'seekable', None)
    if callable(fileobj_seekable):
        if not fileobj_seekable():
            raise ValueError(f"file {repr(fileobj)} is not seekable")
    elif isinstance(fileobj, bool):
        if not fileobj_seekable:
            raise ValueError(f"file {repr(fileobj)} is not seekable")
    else:
        fileobj.seek(0, 1)


def mkpicture(data: bytes = b'',
              type: int = 0,
              mime: str = '',
              desc: str = '',
              code: int = 6,
              colors: int = 0,
              depth: int = 0,
              height: int = 0,
              width: int = 0
              ) -> flac.Picture:
    picture = flac.Picture()
    picture.data = data
    picture.type = type
    if not mime:
        mime = get_mimetype_from_data(data)
    picture.mime = mime
    picture.desc = desc
    picture.code = code
    picture.colors = colors
    picture.depth = depth
    picture.height = height
    picture.width = width

    return picture


def get_mimetype_from_data(data: bytes) -> str:
    for pattern, mime_ext in HEADERS_MIMES_EXTS.items():
        if pattern.search(data):
            return mime_ext[0]
    else:
        return ''


def get_extension_from_data(data: bytes) -> str:
    for pattern, mime_ext in HEADERS_MIMES_EXTS.items():
        if pattern.search(data):
            return mime_ext[1]
    else:
        return ''
