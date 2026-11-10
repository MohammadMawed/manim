import numpy as np
import pytest

from manimlib.constants import BLUE, GREEN, RED
from manimlib.utils.color import color_gradient
from manimlib.utils.color import color_to_rgb, hex_to_rgb, interpolate_color, rgb_to_hex
from manimlib.utils.rate_functions import overshoot, running_start, wiggle


def test_single_reference_color_repeats_instead_of_raising():
    # floors[-1] became -1 while the earlier entries stayed 0, so
    # reference_colors[i + 1] indexed past the end and raised IndexError.
    assert [str(c) for c in color_gradient([RED], 3)] == [str(RED).lower()] * 3


def test_single_reference_color_accepts_a_tuple():
    assert len(color_gradient((RED,), 5)) == 5


def test_one_sample_takes_the_first_reference_color():
    # linspace(0, n - 1, 1) samples alpha 0, i.e. the first color. Forcing the
    # end edge case unconditionally returned the last one.
    assert [str(c) for c in color_gradient([RED, GREEN, BLUE], 1)] == [str(RED).lower()]


def test_multi_sample_gradient_still_spans_both_ends():
    result = [str(c) for c in color_gradient([RED, BLUE], 3)]

    assert result[0] == str(RED).lower()
    assert result[-1] == str(BLUE).lower()
    assert len(result) == 3


@pytest.mark.parametrize("colors", [[RED], [RED, BLUE], [RED, GREEN, BLUE]])
def test_zero_length_output_is_empty(colors):
    assert color_gradient(colors, 0) == []


def test_rgb_to_hex_clips_to_gamut():
    """An out-of-gamut channel must not be written into the hex string.

    `rgb2hex` formats a negative channel as text, producing something like
    "#132-197F" that `hex_to_rgb` then refuses to read back.
    """
    assert rgb_to_hex(np.array([1.2, -0.1, 0.5])) == rgb_to_hex(np.array([1.0, 0.0, 0.5]))
    np.testing.assert_allclose(
        hex_to_rgb(rgb_to_hex(np.array([1.2, -0.1, 0.5]))),
        [1.0, 0.0, 0.498039],
        atol=1e-5,
    )
    # In-gamut values are untouched.
    assert rgb_to_hex(np.array([1.0, 0.0, 0.5])) == "#FF007F"


def test_interpolate_color_saturates_outside_the_unit_interval():
    """`overshoot`, `running_start` and `wiggle` leave [0, 1] by design.

    The squared interpolation then goes negative, `sqrt` yields nan, and the
    colour reads back white — losing the interpolation entirely.
    """
    for rate_func, t in ((overshoot, 0.8), (running_start, 0.2), (wiggle, 0.75)):
        alpha = rate_func(t)
        rgb = color_to_rgb(interpolate_color("#FF0000", "#0000FF", alpha))
        assert not np.isnan(rgb).any(), f"{rate_func.__name__} produced {rgb}"
        assert (rgb >= 0).all() and (rgb <= 1).all()

    # Past either end it saturates at that endpoint rather than going white.
    np.testing.assert_allclose(color_to_rgb(interpolate_color("#FF0000", "#0000FF", 1.5)), [0, 0, 1], atol=1e-6)
    np.testing.assert_allclose(color_to_rgb(interpolate_color("#FF0000", "#0000FF", -0.5)), [1, 0, 0], atol=1e-6)
    # Ordinary interpolation is unchanged.
    np.testing.assert_allclose(
        color_to_rgb(interpolate_color("#FF0000", "#0000FF", 0.5)),
        [np.sqrt(0.5), 0.0, np.sqrt(0.5)],
        atol=1e-6,
    )
