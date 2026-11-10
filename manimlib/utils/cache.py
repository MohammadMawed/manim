from __future__ import annotations

import os
from diskcache import Cache, Disk
from diskcache.core import MODE_RAW, MODE_TEXT
from contextlib import contextmanager
from functools import wraps

from manimlib.utils.directories import get_cache_dir
from manimlib.utils.simple_functions import hash_string

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    T = TypeVar('T')


CACHE_SIZE = 1e9  # 1 Gig


class InvalidCacheEntry(ValueError):
    """An entry cannot be decoded as the plain SVG text this cache stores."""


class SvgDisk(Disk):
    """Keep existing string entries readable without deserializing Python objects."""

    def get(self, key, raw):
        if not raw or type(key) is not str:
            raise InvalidCacheEntry("SVG cache keys must be plain strings")
        return key

    def fetch(self, mode, filename, value, read):
        # Check before Disk.fetch: its pickle mode executes a decoder before
        # the caller has any opportunity to inspect the resulting value.
        if mode not in (MODE_RAW, MODE_TEXT):
            raise InvalidCacheEntry("SVG cache values must be plain text")
        result = super().fetch(mode, filename, value, read)
        if type(result) is not str:
            raise InvalidCacheEntry("SVG cache values must be strings")
        return result

    def store(self, value, read, key=None):
        if read or type(value) is not str:
            raise TypeError("Only SVG strings can be stored in the render cache")
        return super().store(value, read, key=key)


_cache = Cache(get_cache_dir(), size_limit=CACHE_SIZE, disk=SvgDisk)


def cache_on_disk(func: Callable[..., T]) -> Callable[..., T]:
    @wraps(func)
    def wrapper(*args, **kwargs):
        key = hash_string(f"{func.__name__}{args}{kwargs}")
        try:
            value = _cache.get(key)
        except InvalidCacheEntry:
            # A legacy/tampered non-text entry is a miss, never executable data.
            _cache.delete(key)
            value = None
        if value is None:
            value = func(*args, **kwargs)
            _cache.set(key, value)
        return value
    return wrapper


def clear_cache():
    _cache.clear()
