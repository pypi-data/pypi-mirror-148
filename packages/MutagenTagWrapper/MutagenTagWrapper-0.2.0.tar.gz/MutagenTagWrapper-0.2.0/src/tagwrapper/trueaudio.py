from __future__ import annotations

from os import PathLike
from typing import IO, Type

from mutagen import apev2
from mutagen import id3
from mutagen import trueaudio

from . import monkeysaudio as wrapper_monkeysaudio
from . import mp3 as wrapper_mp3
from .util import verify_fileobj, verify_readable, verify_seekable, verify_writable

__all__ = ['TrueAudio', 'TrueAudioWithID3', 'TrueAudioWithAPEv2']


class TrueAudioWithAPEv2(wrapper_monkeysaudio.MonkeysAudio):
    @property
    def raw_tag_type(self) -> Type[apev2.APEv2]:
        return apev2.APEv2

    @property
    def raw_tag(self) -> apev2.APEv2:
        return self._raw_tag

    def generate_TrueAudioWithID3(self) -> TrueAudioWithID3:
        return TrueAudioWithID3(self.filething)

    def save(self,
             filething: str | bytes | PathLike | IO[bytes] = None,
             delete_id3=False,
             **kwargs
             ) -> None:
        super().save(filething, **kwargs)
        if delete_id3:
            if filething is None:
                filething = self.filething

            self.delete_id3(filething)

    @staticmethod
    def delete_id3(filething: str | bytes | PathLike | IO[bytes]) -> None:
        try:
            verify_fileobj(filething)
        except ValueError:
            fileobj: IO[bytes] = open(filething, 'r+b')
            filething_type = 'path'
        else:
            verify_readable(filething)
            verify_seekable(filething)
            verify_writable(filething)
            fileobj: IO[bytes] = filething
            filething_type = 'fileobj'

        fileobj.seek(0, 0)
        try:
            id3_size = id3.ID3(fileobj).size
        except id3.ID3NoHeaderError:
            return
        fileobj.seek(id3_size, 0)
        data = fileobj.read()

        if not data.startswith((b'TTA1', b'TTA2')):
            raise ValueError(f'{filething} is not a TrueAudio file')

        fileobj.seek(0, 0)
        fileobj.truncate(0)
        fileobj.write(data)

        if filething_type == 'path':
            fileobj.close()


class TrueAudioWithID3(wrapper_mp3.MP3):
    @property
    def raw_tag_type(self) -> Type[trueaudio.TrueAudio]:
        return trueaudio.TrueAudio

    @property
    def raw_tag(self) -> trueaudio.TrueAudio:
        return self._raw_tag

    def generate_TrueAudioWithAPEv2(self) -> TrueAudioWithAPEv2:
        return TrueAudioWithAPEv2(self.filething)

    def save(self,
             filething: str | bytes | PathLike | IO[bytes] = None,
             delete_apev2=False,
             **kwargs
             ) -> None:
        super().save(filething, **kwargs)
        if delete_apev2:
            if filething is None:
                filething = self.filething

            self.delete_apev2(filething)

    @staticmethod
    def delete_apev2(filething: str | bytes | PathLike | IO[bytes]) -> None:
        try:
            verify_fileobj(filething)
        except ValueError:
            fileobj: IO[bytes] = open(filething, 'r+b')
            filething_type = 'path'
        else:
            verify_readable(filething)
            verify_seekable(filething)
            verify_writable(filething)
            fileobj: IO[bytes] = filething
            filething_type = 'fileobj'

        fileobj.seek(0, 0)
        data = fileobj.read()
        fileobj.seek(0, 0)

        try:
            id3_size = id3.ID3(fileobj).size
        except id3.ID3NoHeaderError:
            id3_size = 0
        if not data[id3_size:].startswith((b'TTA1', b'TTA2')):
            raise ValueError(f'{filething} is not a TrueAudio file')

        fileobj.seek(0, 0)
        if b'APETAGEX' in data:
            fileobj.truncate(data.index(b'APETAGEX'))

        if filething_type == 'path':
            fileobj.close()


TrueAudio = TrueAudioWithID3
