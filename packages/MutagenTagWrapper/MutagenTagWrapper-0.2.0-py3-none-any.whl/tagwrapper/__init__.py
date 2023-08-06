"""MutagenTagWrapper 依托于多媒体标签库 Mutagen，
旨在减少大批量、不同格式的多媒体标签编辑和转换的工作量。

MutagenTagWrapper 目前支持以下多媒体格式：
MP3、FLAC、Ogg Vorbis、APE（Monkey's Audio）、TTA（True Audio）、WAV（WAVE）。
"""
from __future__ import annotations

import re
from os import PathLike
from typing import IO, Type

from mutagen import File, FileType
from mutagen import flac as raw_flac
from mutagen import monkeysaudio as raw_monkeysaudio
from mutagen import mp3 as raw_mp3
from mutagen import oggvorbis as raw_oggvorbis
from mutagen import trueaudio as raw_trueaudio
from mutagen import wave as raw_wave

from . import common, flac, monkeysaudio, mp3, ogg, trueaudio, wave
from . import util

__all__ = ['openfile']

_FILE_HEADERS_FORMATS: dict[re.Pattern, Type[common.TagWrapper]] = {
    re.compile(b'^fLaC'): flac.FLAC,
    re.compile(b'^ID3.{,1021}fLaC'): flac.FLAC,
    re.compile(b'^ID3'): mp3.MP3,
    re.compile(b'^\xff[\xf2\xf3\xfb]'): mp3.MP3,
    re.compile(b'^OggS'): ogg.OggVorbis,
    re.compile(b'^MAC '): monkeysaudio.MonkeysAudio
}

_RAWTAGS_WRAPPERS: dict[Type[FileType], Type[common.TagWrapper]] = {
    raw_flac.FLAC: flac.FLAC,
    raw_monkeysaudio.MonkeysAudio: monkeysaudio.MonkeysAudio,
    raw_mp3.MP3: mp3.MP3,
    raw_oggvorbis.OggVorbis: ogg.OggVorbis,
    raw_trueaudio.TrueAudio: trueaudio.TrueAudioWithID3,
    raw_wave.WAVE: wave.WAVE
}


def openfile(filething: str | bytes | PathLike | IO[bytes],
             raw_tag_fallback=False,
             *args,
             **kwargs
             ) -> common.TagWrapper | FileType | None:
    """猜测文件的格式，并尝试读取它的标签（元数据）。

    MutagenTagWrapper 包装器目前支持的音频文件格式：
    MP3、FLAC、Ogg Vorbis、APE（Monkey's Audio）、TTA（True Audio）、WAV（WAVE）。

    如果猜出的文件格式是受支持的，将会返回一个包装器对象，
    这个包装器是基于 ``TagWrapper`` 的、针对此文件格式的实现。

    如果未能猜出文件的格式，或文件格式不受支持，根据 ``raw_raw_tag_fallback`` 的值，
    可能会返回一个 Mutagen 标签对象（或 ``None``）。

    Parameters:
        filething (file): 要打开的源文件，可为路径或文件对象；
            如果为文件对象，必须可读、可写、可跳转
        raw_tag_fallback: 在上层包装器不支持或不可用时，返回下层 Mutagen 标签对象；否则返回 None
        args: 要传递给下层标签实现的位置参数
        kwargs: 要传递给下层标签实现的关键字参数"""
    fallback_tag = File(filething, *args, **kwargs)
    ret = _RAWTAGS_WRAPPERS.get(type(fallback_tag))

    if ret is None:
        if raw_tag_fallback:
            return fallback_tag
        return
    return ret(filething, *args, **kwargs)
