"""通过底层的 ``mutagen.monkeysaudio`` 和 ``mutagen.apev2`` 模块，
处理带有 APEv2 标签的 Monkey's Audio 数据流。

Monkey's Audio 是一个非常高效的无损音频压缩器，由 Matt Ashland 开发。

欲了解更多信息，请参见：http://www.monkeysaudio.com/
"""
from __future__ import annotations

from copy import deepcopy as dp
from typing import Type

from mutagen import apev2, flac
from mutagen import monkeysaudio

from .common import TagWrapper
from .util import get_extension_from_data, mkpicture

__all__ = ['MonkeysAudio']


class MonkeysAudio(TagWrapper):
    @property
    def raw_tag_type(self) -> Type[monkeysaudio.MonkeysAudio]:
        return monkeysaudio.MonkeysAudio

    @property
    def field_names(self) -> dict[str, str]:
        return {
            'contact': 'CONTACT',
            'copyright': 'COPYRIGHT',
            'encoder': 'ENCODER',
            'ISRC': 'ISRC',
            'label': 'LABEL',
            'license': 'LICENSE',
            'performer': 'PERFORMER',
            'tracktotal': 'TRACKTOTAL',
            'version': 'VERSION',
            'description': 'DESCRIPTION',
            'organization': 'PUBLISHER',
            'title': 'TITLE',
            'artist': 'ARTIST',
            'album': 'ALBUM',
            'date': 'YEAR',
            'tracknumber': 'TRACK',
            'genre': 'GENRE',
            'comment': 'COMMENT',
            'albumartist': 'ALBUMARTIST',
            'composer': 'COMPOSER',
            'discnumber': 'DISCNUMBER'
        }

    @property
    def field_names_apevalues(self) -> dict[str, Type[apev2.APETextValue]]:
        return {
            'contact': apev2.APETextValue,
            'copyright': apev2.APETextValue,
            'encoder': apev2.APETextValue,
            'ISRC': apev2.APETextValue,
            'label': apev2.APETextValue,
            'license': apev2.APETextValue,
            'performer': apev2.APETextValue,
            'tracktotal': apev2.APETextValue,
            'version': apev2.APETextValue,
            'description': apev2.APETextValue,
            'organization': apev2.APETextValue,
            'title': apev2.APETextValue,
            'artist': apev2.APETextValue,
            'album': apev2.APETextValue,
            'date': apev2.APETextValue,
            'tracknumber': apev2.APETextValue,
            'genre': apev2.APETextValue,
            'comment': apev2.APETextValue,
            'albumartist': apev2.APETextValue,
            'composer': apev2.APETextValue,
            'discnumber': apev2.APETextValue
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        captialize = {}
        for k, v in self._raw_tag.items():
            captialize[k.upper()] = v
        self._raw_tag.clear()
        self._raw_tag.update(captialize)

    def setter_hook(self, value: str | list[str], setter_name: str) -> apev2.APETextValue:
        text = super().setter_hook(value, setter_name)
        return self.field_names_apevalues[setter_name]('\x00'.join(text))

    @property
    def cover(self) -> flac.Picture | None:
        ape_binary_value: apev2.APEBinaryValue = self.raw_tag.get('COVER ART (FRONT)')
        if ape_binary_value is None:
            return

        pic_data = bytes(ape_binary_value)
        splitted = pic_data.split(b'\x00', maxsplit=1)
        if splitted[0].upper().startswith(b'COVER ART (FRONT)'):
            if len(splitted) > 1:
                pic_data = b'\x00'.join(splitted[1:])
            elif len(splitted) == 0:
                return

        picture = flac.Picture()
        picture.data = pic_data
        picture.type = 3

        return mkpicture(data=pic_data, type=3)

    @cover.setter
    def cover(self, obj: flac.Picture | bytes | dict[str, bytes | str | int]) -> None:
        if isinstance(obj, flac.Picture):
            picture = dp(obj)
        elif isinstance(obj, bytes):
            picture = mkpicture(data=obj)
        elif isinstance(obj, dict):
            picture = mkpicture(**obj)
        else:
            raise TypeError(f"'{type(obj).__name__}' object cannot be interpreted as cover")
        pic_data = picture.data

        target_data = b'\x00'.join(
            [
                b'COVER ART (FRONT)' + get_extension_from_data(pic_data).encode().upper(),
                pic_data
            ]
        )
        self.raw_tag['COVER ART (FRONT)'] = apev2.APEBinaryValue(target_data)

    @cover.deleter
    def cover(self) -> None:
        del self.raw_tag['COVER ART (FRONT)']
