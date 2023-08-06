from __future__ import annotations

import re
from abc import ABCMeta, abstractmethod
from os import PathLike
from typing import IO, Iterable, Type

from mutagen import FileType, flac, StreamInfo

from .util import verify_fileobj, verify_readable, verify_seekable, verify_writable

__all__ = ['TagWrapper', 'UnsupportedTagOperation']
TAG_SEP_PATTERN = re.compile('[;\x00]')


class UnsupportedTagOperation(KeyError):
    pass


class TagWrapper(metaclass=ABCMeta):
    """一个包装器，为下层的 Mutagen 标签（``mutagen.FileType`` 以及由其派生的实现）
    提供了基于属性的、高度统一的抽象接口。

    目前支持以下标签属性，这些属性将会映射到下层标签中对应的键（按首字母顺序排列）：
        - ``album``
        - ``albumartist``
        - ``artist``
        - ``comment``
        - ``composer``
        - ``contact``
        - ``copyright``
        - ``cover`` （某些实现可能不支持）
        - ``date``
        - ``description``
        - ``discnumber``
        - ``encoder``
        - ``genre``
        - ``ISRC``
        - ``label``
        - ``license``
        - ``organization``
        - ``performer``
        - ``pictures`` （某些实现可能不支持）
        - ``streaminfo`` （不可删除）
        - ``title``
        - ``tracknumber``
        - ``tracktotal``
        - ``version``
    可以对大多数标签属性直接进行访问/修改/删除操作，其后果都将会反映到下层标签中。
    除了 ``pictures`` 属性，可通过 ``add_picture()`` 和 ``clear_pictures()`` 进行修改和删除。

    此外，还有以下只读的非标签属性：
        - ``raw_tag_type`` - 下层标签的类
        - ``raw_tag`` - 下层标签
        - ``filething`` - 源文件，为路径或文件对象
        - ``field_names`` - TagWrapper 标签属性与 Mutagen 标签键之间的映射关系
    """

    @property
    @abstractmethod
    def raw_tag_type(self) -> Type[FileType]:
        pass

    @property
    def raw_tag(self) -> FileType:
        return self._raw_tag

    @property
    def filething(self) -> str | bytes | PathLike | IO[bytes]:
        return self._filething

    @property
    @abstractmethod
    def field_names(self) -> dict[str, str]:
        pass

    def get_raw_field_name(self, name: str) -> str:
        try:
            return self.field_names[name]
        except KeyError:
            raise UnsupportedTagOperation(name)

    def __init__(self, *args, **kwargs) -> None:
        try:
            filething: str | bytes | PathLike | IO[bytes] = args[0]
        except IndexError:
            filething: str | bytes | PathLike | IO[bytes] = kwargs.get('filething')

        if filething is not None:
            try:
                verify_fileobj(filething)
            except ValueError:
                filething_type = 'path'
            else:
                verify_readable(filething)
                verify_seekable(filething)
                verify_writable(filething)
                filething.seek(0, 0)
                filething_type = 'fileobj'
        else:
            filething_type = None

        self._raw_tag = self.raw_tag_type(*args, **kwargs)
        self._filething = filething
        if filething_type == 'fileobj':
            self._filething.seek(0, 0)

    def __repr__(self) -> str:
        ret = f'<{type(self).__name__}'
        for k, v in self.field_names.items():
            rv = self._raw_tag.get(v)
            if rv:
                ret += f', {k}={repr(list(rv))}'

        return ret + '>'

    def load_tag(self, tag: TagWrapper) -> None:
        for k, v in self.field_names.items():
            try:
                target_v = tag.get_raw_field_name(k)
            except UnsupportedTagOperation:
                continue

            target_data = tag.getter_hook(tag.raw_tag.get(target_v), k)
            if target_data is not None:
                self.raw_tag[v] = self.setter_hook(target_data, k)

        try:
            if tag.cover is not None:
                self.cover = tag.cover
        except UnsupportedTagOperation:
            pass

        try:
            for _ in tag.pictures:
                self.add_picture(_)
        except UnsupportedTagOperation:
            pass

    def load(self, filething: str | bytes | PathLike | IO[bytes], **kwargs) -> None:
        try:
            verify_fileobj(filething)
        except ValueError:
            pass
        else:
            verify_readable(filething)
            verify_seekable(filething)
            verify_writable(filething)
            filething.seek(0, 0)

        self._raw_tag.load(filething, **kwargs)

    def save(self, filething: str | bytes | PathLike | IO[bytes] = None, **kwargs) -> None:
        if filething is None:
            filething = self._filething

            try:
                verify_fileobj(filething)
            except ValueError:
                pass
            else:
                verify_readable(filething)
                verify_seekable(filething)
                verify_writable(filething)
                filething.seek(0, 0)

        self._raw_tag.save(filething, **kwargs)

    def getter_hook(self, value: Iterable | None, getter_name: str) -> list[str] | None:
        """在返回数据之前，对从底层标签中获取的数据进行最后的处理。"""
        bool(getter_name)
        if value is not None:
            pending: list[str] = [str(_) for _ in list(value)]
            ret = []
            for i in pending:
                ret.extend(TAG_SEP_PATTERN.split(i))

            return ret

    def setter_hook(self, value: str | list[str], setter_name: str) -> Iterable:
        """在向底层标签写入数据之前，对外部输入的数据进行最后的处理。"""
        if isinstance(value, str):
            final_values = TAG_SEP_PATTERN.split(value)
        elif isinstance(value, list):
            pending: list[str] = [str(_) for _ in value[:]]
            final_values: list[str] = []
            for i in pending:
                final_values.extend(TAG_SEP_PATTERN.split(i))
        else:
            raise TypeError(f"attribute '{setter_name}' must be str or list contained str, "
                            f" not {type(value).__name__}"
                            )
        return final_values

    @property
    def title(self) -> list[str] | None:
        return self.getter_hook(self._raw_tag.get(self.get_raw_field_name('title')), 'title')

    @title.setter
    def title(self, value: str | list[str]) -> None:
        self._raw_tag[self.get_raw_field_name('title')] = self.setter_hook(value, 'title')

    @title.deleter
    def title(self) -> None:
        del self._raw_tag[self.get_raw_field_name('title')]

    @property
    def artist(self) -> list[str] | None:
        return self.getter_hook(self._raw_tag.get(self.get_raw_field_name('artist')), 'artist')

    @artist.setter
    def artist(self, value: str | list[str]) -> None:
        self._raw_tag[self.get_raw_field_name('artist')] = self.setter_hook(value, 'artist')

    @artist.deleter
    def artist(self) -> None:
        del self._raw_tag[self.get_raw_field_name('artist')]

    @property
    def album(self) -> list[str] | None:
        return self.getter_hook(self._raw_tag.get(self.get_raw_field_name('album')), 'album')

    @album.setter
    def album(self, value: str | list[str]) -> None:
        self._raw_tag[self.get_raw_field_name('album')] = self.setter_hook(value, 'album')

    @album.deleter
    def album(self) -> None:
        del self._raw_tag[self.get_raw_field_name('album')]

    @property
    def albumartist(self) -> list[str] | None:
        return self.getter_hook(self._raw_tag.get(self.get_raw_field_name('albumartist')), 'albumartist')

    @albumartist.setter
    def albumartist(self, value: str | list[str]) -> None:
        self._raw_tag[self.get_raw_field_name('albumartist')] = self.setter_hook(value, 'albumartist')

    @albumartist.deleter
    def albumartist(self) -> None:
        del self._raw_tag[self.get_raw_field_name('albumartist')]

    @property
    def performer(self) -> list[str] | None:
        return self.getter_hook(self._raw_tag.get(self.get_raw_field_name('performer')), 'performer')

    @performer.setter
    def performer(self, value: str | list[str]) -> None:
        self._raw_tag[self.get_raw_field_name('performer')] = self.setter_hook(value, 'performer')

    @performer.deleter
    def performer(self) -> None:
        del self._raw_tag[self.get_raw_field_name('performer')]

    @property
    def composer(self) -> list[str] | None:
        return self.getter_hook(self._raw_tag.get(self.get_raw_field_name('composer')), 'composer')

    @composer.setter
    def composer(self, value: str | list[str]) -> None:
        self._raw_tag[self.get_raw_field_name('composer')] = self.setter_hook(value, 'composer')

    @composer.deleter
    def composer(self) -> None:
        del self._raw_tag[self.get_raw_field_name('composer')]

    @property
    def description(self) -> list[str] | None:
        return self.getter_hook(self._raw_tag.get(self.get_raw_field_name('description')), 'description')

    @description.setter
    def description(self, value: str | list[str]) -> None:
        self._raw_tag[self.get_raw_field_name('description')] = self.setter_hook(value, 'description')

    @description.deleter
    def description(self) -> None:
        del self._raw_tag[self.get_raw_field_name('description')]

    @property
    def comment(self) -> list[str] | None:
        return self.getter_hook(self._raw_tag.get(self.get_raw_field_name('comment')), 'comment')

    @comment.setter
    def comment(self, value: str | list[str]) -> None:
        self._raw_tag[self.get_raw_field_name('comment')] = self.setter_hook(value, 'comment')

    @comment.deleter
    def comment(self) -> None:
        del self._raw_tag[self.get_raw_field_name('comment')]

    @property
    def tracktotal(self) -> list[str] | None:
        return self.getter_hook(self._raw_tag.get(self.get_raw_field_name('tracktotal')), 'tracktotal')

    @tracktotal.setter
    def tracktotal(self, value: str | list[str]) -> None:
        self._raw_tag[self.get_raw_field_name('tracktotal')] = self.setter_hook(value, 'tracktotal')

    @tracktotal.deleter
    def tracktotal(self) -> None:
        del self._raw_tag[self.get_raw_field_name('tracktotal')]

    @property
    def tracknumber(self) -> list[str] | None:
        return self.getter_hook(self._raw_tag.get(self.get_raw_field_name('tracknumber')), 'tracknumber')

    @tracknumber.setter
    def tracknumber(self, value: str | list[str]) -> None:
        self._raw_tag[self.get_raw_field_name('tracknumber')] = self.setter_hook(value, 'tracknumber')

    @tracknumber.deleter
    def tracknumber(self) -> None:
        del self._raw_tag[self.get_raw_field_name('tracknumber')]

    @property
    def discnumber(self) -> list[str] | None:
        return self.getter_hook(self._raw_tag.get(self.get_raw_field_name('tracknumber')), 'discnumber')

    @discnumber.setter
    def discnumber(self, value: str | list[str]) -> None:
        self._raw_tag[self.get_raw_field_name('discnumber')] = self.setter_hook(value, 'discnumber')

    @discnumber.deleter
    def discnumber(self) -> None:
        del self._raw_tag[self.get_raw_field_name('discnumber')]

    @property
    def date(self) -> list[str] | None:
        return self.getter_hook(self._raw_tag.get(self.get_raw_field_name('date')), 'date')

    @date.setter
    def date(self, value: str | list[str]) -> None:
        self._raw_tag[self.get_raw_field_name('date')] = self.setter_hook(value, 'date')

    @date.deleter
    def date(self) -> None:
        del self._raw_tag[self.get_raw_field_name('date')]

    @property
    def genre(self) -> list[str] | None:
        return self.getter_hook(self._raw_tag.get(self.get_raw_field_name('genre')), 'genre')

    @genre.setter
    def genre(self, value: str | list[str]) -> None:
        self._raw_tag[self.get_raw_field_name('genre')] = self.setter_hook(value, 'genre')

    @genre.deleter
    def genre(self) -> None:
        del self._raw_tag[self.get_raw_field_name('genre')]

    @property
    def contact(self) -> list[str] | None:
        return self.getter_hook(self._raw_tag.get(self.get_raw_field_name('contact')), 'contact')

    @contact.setter
    def contact(self, value: str | list[str]) -> None:
        self._raw_tag[self.get_raw_field_name('contact')] = self.setter_hook(value, 'contact')

    @contact.deleter
    def contact(self) -> None:
        del self._raw_tag[self.get_raw_field_name('contact')]

    @property
    def copyright(self) -> list[str] | None:
        return self.getter_hook(self._raw_tag.get(self.get_raw_field_name('copyright')), 'copyright')

    @copyright.setter
    def copyright(self, value: str | list[str]) -> None:
        self._raw_tag[self.get_raw_field_name('copyright')] = self.setter_hook(value, 'copyright')

    @copyright.deleter
    def copyright(self) -> None:
        del self._raw_tag[self.get_raw_field_name('copyright')]

    @property
    def license(self) -> list[str] | None:
        return self.getter_hook(self._raw_tag.get(self.get_raw_field_name('license')), 'license')

    @license.setter
    def license(self, value: str | list[str]) -> None:
        self._raw_tag[self.get_raw_field_name('license')] = self.setter_hook(value, 'license')

    @license.deleter
    def license(self) -> None:
        del self._raw_tag[self.get_raw_field_name('license')]

    @property
    def organization(self) -> list[str] | None:
        return self.getter_hook(self._raw_tag.get(self.get_raw_field_name('organization')), 'organization')

    @organization.setter
    def organization(self, value: str | list[str]) -> None:
        self._raw_tag[self.get_raw_field_name('organization')] = self.setter_hook(value, 'organization')

    @organization.deleter
    def organization(self) -> None:
        del self._raw_tag[self.get_raw_field_name('organization')]

    @property
    def encoder(self) -> list[str] | None:
        return self.getter_hook(self._raw_tag.get(self.get_raw_field_name('encoder')), 'encoder')

    @encoder.setter
    def encoder(self, value: str | list[str]) -> None:
        self._raw_tag[self.get_raw_field_name('encoder')] = self.setter_hook(value, 'encoder')

    @encoder.deleter
    def encoder(self) -> None:
        del self._raw_tag[self.get_raw_field_name('encoder')]

    @property
    def version(self) -> list[str] | None:
        return self.getter_hook(self._raw_tag.get(self.get_raw_field_name('version')), 'version')

    @version.setter
    def version(self, value: str | list[str]) -> None:
        self._raw_tag[self.get_raw_field_name('version')] = self.setter_hook(value, 'version')

    @version.deleter
    def version(self) -> None:
        del self._raw_tag[self.get_raw_field_name('version')]

    @property
    def label(self) -> list[str] | None:
        return self.getter_hook(self._raw_tag.get(self.get_raw_field_name('label')), 'label')

    @label.setter
    def label(self, value: str | list[str]) -> None:
        self._raw_tag[self.get_raw_field_name('label')] = self.setter_hook(value, 'label')

    @label.deleter
    def label(self) -> None:
        del self._raw_tag[self.get_raw_field_name('label')]

    @property
    def ISRC(self) -> list[str] | None:
        return self.getter_hook(self._raw_tag.get(self.get_raw_field_name('ISRC')), 'ISRC')

    @ISRC.setter
    def ISRC(self, value: str | list[str]) -> None:
        self._raw_tag[self.get_raw_field_name('ISRC')] = self.setter_hook(value, 'ISRC')

    @ISRC.deleter
    def ISRC(self) -> None:
        del self._raw_tag[self.get_raw_field_name('ISRC')]

    @property
    def streaminfo(self) -> StreamInfo | None:
        return self.raw_tag.info

    @property
    def cover(self) -> flac.Picture | None:
        raise UnsupportedTagOperation('cover')

    @cover.setter
    def cover(self, obj: flac.Picture | bytes | dict[str, bytes | str | int]) -> None:
        raise UnsupportedTagOperation('cover')

    @cover.deleter
    def cover(self) -> None:
        raise UnsupportedTagOperation('cover')

    @property
    def pictures(self) -> list[flac.Picture]:
        raise UnsupportedTagOperation('pictures')

    def add_picture(self, obj: flac.Picture | bytes | dict[str, bytes | str | int]) -> None:
        raise UnsupportedTagOperation('add_picture')

    def clear_pictures(self) -> None:
        raise UnsupportedTagOperation('clear_pictures')
