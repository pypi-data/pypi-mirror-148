"""通过底层的 ``mutagen.oggvorbis`` 模块读取和写入 Ogg Vorbis 注释。

这个模块处理包裹在 Ogg 比特流中的 Vorbis 文件，使用第一个找到的 Vorbis 流。

此模块可能不支持 Ogg FLAC 文件。如果碰到任何这方面的问题，请使用 ``mutagen.oggflac`` 模块代替。
"""
from __future__ import annotations

from base64 import b64decode, b64encode
from copy import deepcopy as dp
from typing import Type

from mutagen import flac, oggvorbis

from .common import TagWrapper
from .util import mkpicture


def unpack_vorbis_comment_picture(b64_encoded_data: str | bytes) -> flac.Picture:
    final_picture_data: bytes = b64decode(b64_encoded_data)

    return flac.Picture(final_picture_data)


def pack_vorbis_comment_picture(picture: flac.Picture) -> str:
    final_picture_data: bytes = picture.write()

    return b64encode(final_picture_data).decode()


class OggVorbis(TagWrapper):
    @property
    def raw_tag_type(self) -> Type[oggvorbis.OggVorbis]:
        return oggvorbis.OggVorbis

    @property
    def raw_tag(self) -> oggvorbis.OggVorbis:
        return self._raw_tag

    @property
    def field_names(self) -> dict[str, str]:
        return {
            'title': 'title',
            'artist': 'artist',
            'album': 'album',
            'albumartist': 'albumartist',
            'performer': 'performer',
            'composer': 'composer',
            'description': 'description',
            'comment': 'comment',
            'discnumber': 'discnumber',
            'tracknumber': 'tracknumber',
            'tracktotal': 'tracktotal',
            'date': 'date',
            'genre': 'genre',
            'contact': 'contact',
            'copyright': 'copyright',
            'label': 'label',
            'license': 'license',
            'organization': 'organization',
            'ISRC': 'ISRC',
            'version': 'version',
            'encoder': 'encoder'
        }

    @property
    def cover(self) -> flac.Picture:
        for picture in self.pictures:
            if picture.type == 3:
                return picture

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
        picture.type = 3

        if not self.pictures:
            self.add_picture(picture)
            return

        pictures = [_ for _ in self.pictures if _.type != 3] + [picture]
        self.clear_pictures()

        for _ in pictures:
            self.add_picture(_)

    @cover.deleter
    def cover(self) -> None:
        pictures = [_ for _ in self.pictures if _.type != 3]

        for _ in pictures:
            self.add_picture(_)

    @property
    def pictures(self) -> list[flac.Picture]:
        mbp: list[str] = self.raw_tag.get('metadata_block_picture', [])
        return [unpack_vorbis_comment_picture(_) for _ in mbp[:]]

    def add_picture(self, obj: flac.Picture | bytes | dict[str, bytes | str | int]) -> None:
        if isinstance(obj, flac.Picture):
            picture = dp(obj)
        elif isinstance(obj, bytes):
            picture = mkpicture(data=obj)
        elif isinstance(obj, dict):
            picture = mkpicture(**obj)
        else:
            raise TypeError(f"'{type(obj).__name__}' object cannot be interpreted as cover")

        pictures = self.pictures + [picture]

        self.raw_tag['metadata_block_picture'] = [
            pack_vorbis_comment_picture(_) for _ in pictures
        ]

    def clear_pictures(self) -> None:
        try:
            del self.raw_tag['metadata_block_picture']
        except KeyError:
            pass


OGG = OggVorbis
