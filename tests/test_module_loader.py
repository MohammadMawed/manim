import sys
from types import ModuleType

import pytest

from manimlib.module_loader import ModuleLoader


def test_absolute_scene_path_supports_dataclass_decorators(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    source = tmp_path / "decorated_scene.py"
    source.write_text(
        "from __future__ import annotations\n"
        "from dataclasses import dataclass\n"
        "@dataclass\n"
        "class Point:\n"
        "    x: float\n",
        encoding="utf-8",
    )
    monkeypatch.setitem(sys.modules, "decorated_scene", None)
    module = ModuleLoader.get_module(str(source))
    assert not module.__name__.startswith(".")
    assert module.Point(2).x == 2
    assert sys.modules[module.__name__] is module


@pytest.mark.parametrize("previous", [None, ModuleType("broken_scene")])
def test_failed_module_load_restores_previous_registration(tmp_path, monkeypatch, previous):
    monkeypatch.chdir(tmp_path)
    source = tmp_path / "broken_scene.py"
    source.write_text("raise RuntimeError('scene failed')\n", encoding="utf-8")
    monkeypatch.setitem(sys.modules, "broken_scene", previous)
    with pytest.raises(RuntimeError, match="scene failed"):
        ModuleLoader.get_module(str(source))
    assert sys.modules["broken_scene"] is previous


def test_failed_module_load_removes_new_registration(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    source = tmp_path / "new_broken_scene.py"
    source.write_text("raise RuntimeError('scene failed')\n", encoding="utf-8")
    monkeypatch.delitem(sys.modules, "new_broken_scene", raising=False)
    with pytest.raises(RuntimeError):
        ModuleLoader.get_module(str(source))
    assert "new_broken_scene" not in sys.modules
