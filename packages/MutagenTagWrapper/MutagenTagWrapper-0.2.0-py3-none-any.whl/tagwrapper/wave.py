from __future__ import annotations

from typing import Type

from mutagen import wave

from . import mp3 as wrapper_mp3

__all__ = ['WAVE']


class WAVE(wrapper_mp3.MP3):
    @property
    def raw_tag_type(self) -> Type[wave.WAVE]:
        return wave.WAVE

    @property
    def raw_tag(self) -> wave.WAVE:
        return self._raw_tag
