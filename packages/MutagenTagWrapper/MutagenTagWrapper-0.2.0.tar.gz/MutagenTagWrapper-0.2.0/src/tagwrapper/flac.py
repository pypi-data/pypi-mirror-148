"""通过底层的 ``mutagen.flac`` 模块，读取和写入 FLAC Vorbis 的评论和数据流信息。

阅读更多关于 FLAC 的信息，请访问 http://flac.sourceforge.net。

FLAC 支持任意的元数据块。最常见的两个是 FLAC 流信息块和 Vorbis 注释块；这也是
MutagenTagWrapper（也是 Mutagen）目前唯一可以读取的。

此模块不支持 Ogg Flac 文件（因为底层的 ``mutagen.flac`` 模块也不支持）。
请使用 ``mutagen.oggflac`` 模块。
"""
from __future__ import annotations

from copy import deepcopy as dp
from typing import Type

from mutagen import flac

from .common import TagWrapper
from .util import mkpicture

__all__ = ['FLAC']

class FLAC(TagWrapper):
    @property
    def raw_tag_type(self) -> Type[flac.FLAC]:
        return flac.FLAC

    @property
    def raw_tag(self) -> flac.FLAC:
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
    def cover(self) -> flac.Picture | None:
        for picture in self.picture:
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
        pictures = [picture] + [_ for _ in self.picture if _.type != 3]

        self.clear_pictures()
        for _ in pictures:
            self.add_picture(_)

    @cover.deleter
    def cover(self) -> None:
        pictures = [_ for _ in self.picture if _.type != 3]

        self.clear_pictures()
        for _ in pictures:
            self.add_picture(_)

    @property
    def picture(self) -> list[flac.Picture]:
        return self.raw_tag.pictures[:]

    def add_picture(self, obj: flac.Picture | bytes | dict[str, bytes | str | int]) -> None:
        if isinstance(obj, flac.Picture):
            picture = dp(obj)
        elif isinstance(obj, bytes):
            picture = mkpicture(data=obj)
        elif isinstance(obj, dict):
            picture = mkpicture(**obj)
        else:
            raise TypeError(f"'{type(obj).__name__}' object cannot be interpreted as cover")

        self.raw_tag.add_picture(picture)

    def clear_pictures(self) -> None:
        self.raw_tag.clear_pictures()
