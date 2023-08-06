"""通过底层的 ``mutagen.mp3`` 和 ``mutagen.id3`` 模块，处理 MPEG 音频流信息和标签。"""
from __future__ import annotations

from functools import partial
from typing import Type

from mutagen import flac, mp3
from mutagen import id3

from .common import TagWrapper
from .util import get_mimetype_from_data, mkpicture

__all__ = ['MP3']


class MP3(TagWrapper):
    @property
    def raw_tag_type(self) -> Type[mp3.MP3]:
        return mp3.MP3

    @property
    def raw_tag(self) -> mp3.MP3:
        return self._raw_tag

    @property
    def field_names(self) -> dict[str, str]:
        return {
            'title': 'TIT2',
            'artist': 'TPE1',
            'album': 'TALB',
            'albumartist': 'TPE2',
            'performer': 'TPE3',
            'composer': 'TCOM',
            'description': 'TXXX:COMMENT',
            'comment': 'COMM::XXX',
            'discnumber': 'TPOS',
            'tracknumber': 'TRCK',
            'tracktotal': 'TXXX:TRACKTOTAL',
            'date': 'TDRC',
            'genre': 'TCON',
            'contact': 'TXXX:CONTACT',
            'copyright': 'TCOP',
            'label': 'TXXX:LABEL',
            'license': 'TXXX:LICENSE',
            'organization': 'TXXX:ORGANIZATION',
            'ISRC': 'TXXX:ISRC',
            'version': 'TXXX:VERSION',
            'encoder': 'TSSE'
        }

    @property
    def field_names_frames(self) -> dict[str, Type[id3.Frame]]:
        return {
            'title': id3.TIT2,
            'artist': id3.TPE1,
            'album': id3.TALB,
            'albumartist': id3.TPE2,
            'performer': id3.TPE3,
            'composer': id3.TCOM,
            'description': partial(id3.TXXX, desc='comment'),
            'comment': id3.COMM,
            'discnumber': id3.TPOS,
            'tracknumber': id3.TRCK,
            'tracktotal': partial(id3.TXXX, desc='tracktotal'),
            'date': id3.TDRC,
            'genre': id3.TCON,
            'contact': partial(id3.TXXX, desc='contact'),
            'copyright': id3.TCOP,
            'label': partial(id3.TXXX, desc='label'),
            'license': partial(id3.TXXX, desc='license'),
            'organization': partial(id3.TXXX, desc='organization'),
            'ISRC': partial(id3.TXXX, desc='ISRC'),
            'version': partial(id3.TXXX, desc='version'),
            'encoder': id3.TSSE
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        captializes: dict[str, id3.Frame] = {}
        for k, v in self._raw_tag.items():
            captializes[k.upper()] = v
        self._raw_tag.clear()
        self._raw_tag.update(captializes)

        orig_COMM_XXX_key: str | None = None
        orig_COMM_XXX: id3.COMM | None = None
        for k, v in self._raw_tag.items():
            if k.startswith('COMM::'):
                orig_COMM_XXX_key = k
                orig_COMM_XXX = v
                break

        if orig_COMM_XXX_key:
            del self._raw_tag[orig_COMM_XXX_key]
            orig_COMM_XXX.lang = 'XXX'
            self._raw_tag['COMM::XXX'] = orig_COMM_XXX

    def setter_hook(self, value: str | list[str], setter_name: str) -> id3.Frame:
        text = super().setter_hook(value, setter_name)
        return self.field_names_frames[setter_name](text=text)

    @property
    def cover(self) -> flac.Picture | None:
        apic: id3.APIC | None = self.raw_tag.get('APIC:')
        if apic is None:
            return

        desc: str | None = getattr(apic, 'desc', None)
        mime: str | None = getattr(apic, 'mime', None)
        data: bytes | None = getattr(apic, 'data', None)

        picture = flac.Picture()
        picture.type = 3
        picture.desc = desc
        picture.mime = mime
        picture.data = data

        return mkpicture(data=data, type=3, desc=desc, mime=mime)

    @cover.setter
    def cover(self, obj: flac.Picture | bytes | dict[str, bytes | str | int]) -> None:
        if isinstance(obj, flac.Picture):
            data = obj.data
            desc = obj.desc
            mime = obj.mime
        elif isinstance(obj, bytes):
            data = obj
            desc = ''
            mime = get_mimetype_from_data(obj)
        elif isinstance(obj, dict):
            data: bytes = obj['data']
            desc: str = obj.get('desc', '')
            mime: str = get_mimetype_from_data(data) if not obj.get('mime') else obj.get('mime')
        else:
            raise TypeError(f"'{type(obj).__name__}' object cannot be interpreted as cover")
        picture_type = 3

        apic = id3.APIC(encoding=3, mime=mime, type=picture_type, desc=desc, data=data)

        self.raw_tag['APIC:'] = apic

    @cover.deleter
    def cover(self):
        del self.raw_tag['APIC:']
