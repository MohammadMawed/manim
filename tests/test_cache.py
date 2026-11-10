from diskcache import Cache, Disk
from diskcache.core import MODE_TEXT
import pytest

from manimlib.utils import cache


planted_calls = []


def planted():
    planted_calls.append(True)
    return "<svg>poisoned</svg>"


class Planted:
    def __reduce__(self):
        return planted, ()


@pytest.mark.parametrize("min_file_size", [1, 1_000_000])
def test_pickled_cache_value_is_a_miss_without_execution(tmp_path, monkeypatch, min_file_size):
    planted_calls.clear()
    with Cache(str(tmp_path), disk=type(cache._cache.disk),
               disk_min_file_size=min_file_size) as temp_cache:
        monkeypatch.setattr(cache, "_cache", temp_cache)
        renders = []

        @cache.cache_on_disk
        def to_svg(text):
            renders.append(text)
            return f"<svg>{text}</svg>"

        assert to_svg("x") == to_svg("x") == "<svg>x</svg>"
        key, = list(temp_cache)
        with Cache(str(tmp_path), disk=Disk,
                   disk_min_file_size=min_file_size) as writer:
            writer.set(key, Planted())

        assert to_svg("x") == "<svg>x</svg>"
        assert to_svg("x") == "<svg>x</svg>"
        assert renders == ["x", "x"]
        assert planted_calls == []


@pytest.mark.parametrize("value", ["<svg>legacy</svg>", "<svg>" + "x" * 40_000 + "</svg>"])
def test_existing_text_cache_remains_readable(tmp_path, monkeypatch, value):
    with Cache(str(tmp_path), disk=type(cache._cache.disk)) as temp_cache:
        monkeypatch.setattr(cache, "_cache", temp_cache)

        @cache.cache_on_disk
        def to_svg():
            return "<svg>original</svg>"

        to_svg()
        key, = list(temp_cache)
        with Cache(str(tmp_path), disk=Disk) as writer:
            writer.set(key, value)
        assert to_svg() == value


def test_tampered_filename_cannot_read_or_delete_outside_cache(tmp_path, monkeypatch):
    outside = tmp_path / "outside.svg"
    outside.write_text("<svg>outside</svg>", encoding="utf-8")
    with Cache(str(tmp_path / "cache"), disk=type(cache._cache.disk)) as temp_cache:
        monkeypatch.setattr(cache, "_cache", temp_cache)

        @cache.cache_on_disk
        def to_svg():
            return "<svg>computed</svg>"

        to_svg()
        key, = list(temp_cache)
        temp_cache._sql(
            'UPDATE Cache SET mode = ?, filename = ?, value = NULL WHERE key = ?',
            (MODE_TEXT, str(outside), key),
        )
        assert to_svg() == "<svg>computed</svg>"
        assert outside.read_text(encoding="utf-8") == "<svg>outside</svg>"
