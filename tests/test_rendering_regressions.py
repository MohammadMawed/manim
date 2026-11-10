from types import SimpleNamespace

import numpy as np
from PIL import Image
import pytest

from manimlib import Code, Ellipse, ImageMobject, NumberPlane
from manimlib.mobject.types.surface import ParametricSurface, TexturedSurface
from manimlib.renderer.gpu import Gpu
from manimlib.scene.scene import Scene
import manimlib.mobject.svg.text_mobject as text_mobject
import manimlib.scene.scene as scene_module


def test_number_plane_uses_each_axis_scale():
    plane = NumberPlane(x_range=(-2, 2), y_range=(-4, 4), width=12, height=8)
    assert plane.get_x_unit_size() == pytest.approx(3)
    assert plane.get_y_unit_size() == pytest.approx(1)


@pytest.mark.parametrize("axis", [0, 1])
def test_textured_surface_partial_updates_real_texture_coordinates(tmp_path, axis):
    image = tmp_path / "texture.png"
    Image.new("RGB", (2, 2), "white").save(image)
    surface = ParametricSurface(lambda u, v: [u, v, 0], resolution=(3, 3))
    source = TexturedSurface(surface, str(image))
    partial = source.copy()
    original_coords = source.data["im_coords"].copy()

    partial.pointwise_become_partial(source, 0, 0.5, axis=axis)

    grid = partial.data["im_coords"].reshape(3, 3, 2)
    assert np.isfinite(grid).all()
    if axis == 0:
        np.testing.assert_allclose(grid[-1], grid[1])
    else:
        np.testing.assert_allclose(grid[:, -1], grid[:, 1])
    np.testing.assert_array_equal(source.data["im_coords"], original_coords)
    partial.pointwise_become_partial(source, 0, 1, axis=axis)
    np.testing.assert_array_equal(partial.data["im_coords"], original_coords)


@pytest.mark.parametrize("offset", [[10, 0, 0], [0, 10, 0], [10, 10, 0], [0, -10, 0]])
def test_image_rejects_all_outside_points(tmp_path, offset):
    image = tmp_path / "image.png"
    Image.new("RGB", (2, 2), "red").save(image)
    mobject = ImageMobject(str(image), height=2)
    with pytest.raises(Exception, match="Cannot sample color from outside an image"):
        mobject.point_to_rgb(mobject.get_center() + offset)
    np.testing.assert_allclose(mobject.point_to_rgb(mobject.get_center()), [1, 0, 0])


def test_ellipse_keeps_requested_radii():
    ellipse = Ellipse(width=6, height=2)
    anchors = ellipse.get_anchors()
    np.testing.assert_allclose(np.max(np.abs(anchors[:, :2]), axis=0), [3, 1], atol=1e-6)


def test_code_short_hex_colors_reach_pango_as_valid_markup(monkeypatch):
    monkeypatch.setattr(text_mobject.pygments, "highlight",
                        lambda *args: '<tt><span foreground="#abc">x</span></tt>')
    code = Code("x", font="monospace")
    assert '#aabbcc' in code.string
    assert len(code.submobjects) > 0


def test_uniform_layouts_separate_sizes_and_share_resource_layouts():
    groups = []
    def layout(**kwargs):
        result = SimpleNamespace(**kwargs)
        groups.append(result)
        return result

    gpu = Gpu.__new__(Gpu)
    gpu.device = SimpleNamespace(create_bind_group_layout=layout, create_pipeline_layout=layout)
    gpu.frame_layout = object()
    gpu.layouts = {}
    gpu.mobject_layouts = {}
    gpu.resource_layouts = {}
    small_resources, small_pipeline = gpu.bind_layouts(112, ())
    large_resources, large_pipeline = gpu.bind_layouts(192, ())

    assert small_resources is large_resources
    assert small_pipeline is not large_pipeline
    assert gpu.mobject_layout(112) is gpu.mobject_layout(112)
    assert gpu.mobject_layout(112).entries[0]["buffer"]["min_binding_size"] == 112
    assert gpu.mobject_layout(192).entries[0]["buffer"]["min_binding_size"] == 192


def test_frame_pacing_uses_elapsed_time_not_wall_clock(monkeypatch):
    delays = []
    scene = Scene.__new__(Scene)
    scene.skip_animations = False
    scene.window = SimpleNamespace()
    scene.camera = SimpleNamespace(capture=lambda *args: None)
    scene.mobjects = []
    scene.time = 10.0
    scene.virtual_animation_start_time = 0.0
    scene.real_animation_start_time = 100.0
    scene.is_window_closing = lambda: False
    monkeypatch.setattr(scene_module.time, "perf_counter", lambda: 109.9)
    monkeypatch.setattr(scene_module.time, "time", lambda: -1_000_000.0)
    monkeypatch.setattr(scene_module.time, "sleep", delays.append)
    scene.draw_frame(dt=1 / 30)
    assert delays == pytest.approx([0.1])
