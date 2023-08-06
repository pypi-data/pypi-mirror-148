"""MutagenTagWrapper 依托于多媒体标签库 Mutagen，
旨在减少大批量、不同格式的多媒体标签编辑和转换的工作量。

MutagenTagWrapper 目前支持 4 种多媒体标签：FLAC、MP3、Ogg Vorbis、Monkey's Audio（APE）
"""
from __future__ import annotations

import re
from os import PathLike
from typing import IO, Type

import mutagen

from . import common
from . import flac
from . import monkeysaudio
from . import mp3
from . import ogg
from .util import verify_fileobj, verify_readable, verify_seekable

__all__ = ['openfile']

_FILE_HEADERS_FORMATS: dict[re.Pattern, Type[common.TagWrapper]] = {
    re.compile(b'^fLaC'): flac.FLAC,
    re.compile(b'^ID3.{,1021}fLaC'): flac.FLAC,
    re.compile(b'^ID3'): mp3.MP3,
    re.compile(b'^\xff[\xf2\xf3\xfb]'): mp3.MP3,
    re.compile(b'^OggS'): ogg.OggVorbis,
    re.compile(b'^MAC '): monkeysaudio.MonkeysAudio
}


def openfile(filething: str | bytes | PathLike | IO[bytes],
             *args,
             **kwargs
             ) -> common.TagWrapper | mutagen.FileType | None:
    """根据音频文件的前 2048 个字节，猜测文件的格式，并尝试读取它的标签（元数据）。

    MutagenTagWrapper 包装器目前支持的音频文件格式：MP3、FLAC、OGG、APE。

    如果猜出了文件的格式，将会返回一个包装器对象，
    这个包装器是基于 ``TagWrapper`` 的、针对此文件格式的实现。

    如果未能猜出文件的格式，将会调用 ``mutagen.File()`` 返回一个 Mutagen 标签对象（或 ``None``）。

    Parameters:
        filething (file): 要打开的源文件，可为路径或文件对象；
            如果为文件对象，必须可读、可写、可跳转
        args: 要传递给下层标签实现的位置参数
        kwargs: 要传递给下层标签实现的关键字参数"""
    try:
        verify_fileobj(filething)
    except ValueError:
        with open(filething, mode='rb') as f:
            header_data = f.read(2048)
    else:
        verify_readable(filething)
        verify_seekable(filething)
        filething.seek(0, 0)
        header_data = filething.read(2048)
        filething.seek(0, 0)

    args = list(args)
    if len(args) >= 1:
        args[0] = filething
    else:
        args = [filething]

    for expression, wrapper in _FILE_HEADERS_FORMATS.items():
        if expression.search(header_data):
            return wrapper(*args, **kwargs)
    else:
        return mutagen.File(*args, **kwargs)
