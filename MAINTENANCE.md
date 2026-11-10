# Manim maintenance audit

Audit date: 10 November 2026. Upstream baseline: `fafa083a4fb274bba9cabde0b6e2f50ba6da0622`.

Fork: https://github.com/MohammadMawed/manim

Working branch: `fix/critical-rendering-and-runtime`.

## Scope

The inventory contains 469 open issues and 50 open PRs. Open issues include historical backends, platform support requests, feature requests, and unverified reports. This pass prioritizes executable cache deserialization, incorrect mathematical output, installation failures, crashes, and reproducible rendering/runtime regressions on current master. It does not claim all 469 issues are repaired or that upstream PRs have been merged/closed.

21 upstream bug-fix PRs are integrated with contributor authorship preserved. Three further PR concerns are addressed through local security/workflow changes (#2560, #2449, #2537). The table records the disposition of all 50 open PRs. Integrating a PR into this branch does not change that PR's upstream status.

## Important fixes

- SVG disk-cache reads reject executable pickle/non-text entries before decoding, with both inline and file-backed malicious-entry tests and legacy text-cache compatibility. This uses the existing dependency instead of adopting an unreviewed replacement package.
- Failed LaTeX compiles cannot reuse stale DVI/XDV output; UTF-8 writes/log decoding work under a simulated non-UTF-8 locale. Nonzero compilers producing fresh output remain supported.
- Correct independent axis scaling, discontinuous-graph updates, Riemann sample spacing, 3D closest-point calculations, and ellipse radii.
- Fix empty-array shape preservation/interpolation, color-gradient edge cases, out-of-gamut interpolation, textured-surface partial creation, and image-boundary rejection.
- Load decorated scene modules from absolute paths and restore prior module registrations after execution failures.
- Export temporary audio as WAV, declare the mandatory av dependency, expand Pygments short colors before Pango rendering, and use monotonic frame-pacing clocks.
- Use supported Python versions for release builds and add a cross-platform behavioral regression workflow with read-only permissions and pinned actions.

## Validation recorded so far

- Original baseline test suite: 6 passed.
- Seven candidate regression suites against pre-fix code: 15 failed / 19 passed, demonstrating the reported faults.
- Additional security and failed-module regression tests before their local fixes: 5 failed / 3 passed; after fixes: 8 passed.
- Integrated behavioral suite: 73 passed on macOS / Python 3.12, including with wgpu 0.31.
- Package dependency validation: pip check passes after rebuilding editable metadata.
- 13 real Metal/wgpu 0.33 render cases match upstream exactly, including image/surface/gradient/code cases and every compared animation/video frame. Report: local ignored `.cache/render-report.log`.
- Further old-wgpu and remote CI results are recorded below when available.

The machine has no TeX installation. TeX failure/encoding behavior is tested using controlled subprocess fixtures; full TeX-rendered glyph-selection claims are not verified. No Windows/Linux result is claimed until its CI job has passed.

## All open PR dispositions

| PR | Subject | Decision |
| --- | --- | --- |
| [#2560](https://github.com/3b1b/manim/pull/2560) | Stop the Tex and Text disk cache from running pickled entries | Security concern fixed independently with a text-only disk adapter and malicious-entry regression tests; replacement dependency not adopted. |
| [#2558](https://github.com/3b1b/manim/pull/2558) | Fix : audio export format mismatch | Integrated with original commit authorship and cherry-pick provenance. |
| [#2556](https://github.com/3b1b/manim/pull/2556) | Stop failed LaTeX compiles reusing the previous output | Integrated with original commit authorship and cherry-pick provenance. |
| [#2555](https://github.com/3b1b/manim/pull/2555) | Read and write TeX files as UTF-8 | Integrated with original commit authorship and cherry-pick provenance. |
| [#2554](https://github.com/3b1b/manim/pull/2554) | fix: stop wgpu rejecting a smaller uniform block after a larger one | Integrated with original commit authorship and cherry-pick provenance. |
| [#2553](https://github.com/3b1b/manim/pull/2553) | fix: stop bound graphs with discontinuities losing their right end | Integrated with original commit authorship and cherry-pick provenance. |
| [#2551](https://github.com/3b1b/manim/pull/2551) | fix: correct NumberPlane y-axis unit size in coordinate_systems.py | Integrated with original commit authorship and cherry-pick provenance. |
| [#2550](https://github.com/3b1b/manim/pull/2550) | Adopt uv for installation, development, and CI | Deferred: broad package-manager/metadata migration; missing `av` dependency fixed separately. |
| [#2517](https://github.com/3b1b/manim/pull/2517) | fix(tex): strip environments whose argument is not a plain word | Integrated with original commit authorship and cherry-pick provenance. |
| [#2518](https://github.com/3b1b/manim/pull/2518) | fix(color): handle one reference color and one output sample in color_gradient | Integrated with original commit authorship and cherry-pick provenance. |
| [#2523](https://github.com/3b1b/manim/pull/2523) | Fix resizing an empty array | Integrated with original commit authorship and cherry-pick provenance. |
| [#2524](https://github.com/3b1b/manim/pull/2524) | Keep interpolated colors inside the gamut | Integrated with original commit authorship and cherry-pick provenance. |
| [#2532](https://github.com/3b1b/manim/pull/2532) | Honor the step given in get_riemann_rectangles' x_range | Integrated with original commit authorship and cherry-pick provenance. |
| [#2549](https://github.com/3b1b/manim/pull/2549) | fixdone | Not integrated: diff only appends `will test` to README; no bug fix. |
| [#2548](https://github.com/3b1b/manim/pull/2548) | Fix closest-point calculation for skew 3D lines | Integrated with original commit authorship and cherry-pick provenance. |
| [#2536](https://github.com/3b1b/manim/pull/2536) | Fix module exec crash with dataclass and other decorators | Integrated with original commit authorship and cherry-pick provenance. |
| [#2543](https://github.com/3b1b/manim/pull/2543) | Add av to install_requires | Integrated with original commit authorship and cherry-pick provenance. |
| [#2540](https://github.com/3b1b/manim/pull/2540) | Add missing class-level docstrings to ManimGL classes | Deferred: documentation expansion, outside the critical runtime fixes. |
| [#2525](https://github.com/3b1b/manim/pull/2525) | Add a native MCP server at manimlib.mcp | Deferred: optional native MCP feature requires its own integration and execution-boundary review. |
| [#2537](https://github.com/3b1b/manim/pull/2537) | [ci] Update GitHub Actions to latest major release | Current checkout/setup-python versions adopted and pinned; cross-platform regression workflow added. |
| [#2535](https://github.com/3b1b/manim/pull/2535) | feat: Enhance ⁠`add_sound`⁠ with spatial panning, relative trimming, looping, and fade | Deferred: new audio features; existing WAV export bug fixed independently. |
| [#2531](https://github.com/3b1b/manim/pull/2531) | Allow negative animation indices in -n render | Deferred: new animation-index feature and extra scene execution, outside the bug-fix baseline. |
| [#2530](https://github.com/3b1b/manim/pull/2530) | Fix Ellipse bounding box issue by using stretch instead of set_width/set_height | Integrated with original commit authorship and cherry-pick provenance. |
| [#2529](https://github.com/3b1b/manim/pull/2529) | Guard every point outside an image, not only some | Integrated with original commit authorship and cherry-pick provenance. |
| [#2527](https://github.com/3b1b/manim/pull/2527) | fix: publish wheels on supported Python versions | Integrated with original commit authorship and cherry-pick provenance. |
| [#2522](https://github.com/3b1b/manim/pull/2522) | Handle video device source in get_full_video_path | Deferred: camera/device-source feature requires decoding/backend validation. |
| [#2520](https://github.com/3b1b/manim/pull/2520) | fix(surface): fix NameError when partially creating a TexturedSurface | Integrated with original commit authorship and cherry-pick provenance. |
| [#2516](https://github.com/3b1b/manim/pull/2516) | fix: module names for absolute scene paths | Integrated with original commit authorship and cherry-pick provenance. |
| [#2512](https://github.com/3b1b/manim/pull/2512) | docs: correct custom_config keys and drop a dangling toctree entry | Deferred: configuration documentation correction, outside the current critical runtime set. |
| [#2515](https://github.com/3b1b/manim/pull/2515) | Use monotonic clocks for frame pacing | Integrated with original commit authorship and cherry-pick provenance. |
| [#2504](https://github.com/3b1b/manim/pull/2504) | Select the right glyph for a \frac argument | Deferred: fraction glyph-order selection needs TeX-backed visual validation unavailable in this environment. |
| [#2465](https://github.com/3b1b/manim/pull/2465) | Fix/code class pygments short hex #2355 | Integrated with original commit authorship and cherry-pick provenance. |
| [#2470](https://github.com/3b1b/manim/pull/2470) | Italian README Translation | Deferred: translation, outside the critical runtime set. |
| [#2466](https://github.com/3b1b/manim/pull/2466) | Fix/staticmethod callable python 3 10 #2263 | Not integrated: targets Python <3.10, below the package's supported minimum. |
| [#2458](https://github.com/3b1b/manim/pull/2458) | Move to 'uv' for environment and dependency management, add stdio FastMCP server  | Deferred: package-manager migration plus MCP feature; requires separate design review. |
| [#2455](https://github.com/3b1b/manim/pull/2455) | Introduce SampleScene class with animation example | Deferred: example addition, outside critical runtime fixes. |
| [#2449](https://github.com/3b1b/manim/pull/2449) | fix: harden GitHub Actions workflows | Action-pinning concern addressed with verified immutable SHAs and checkout credential restrictions. |
| [#2445](https://github.com/3b1b/manim/pull/2445) | This change is for fiximg spelling and gramatical mistakes in readme.md file. | Deferred: README wording, outside critical runtime fixes. |
| [#2433](https://github.com/3b1b/manim/pull/2433) | Remove redundant `kwargs` handling in `LaggedStartMap` | Deferred: redundant-code cleanup, without a demonstrated runtime fault. |
| [#2425](https://github.com/3b1b/manim/pull/2425) | Fix color leakage issue in shader rendering | Deferred: older shader correction needs a current-backend reproducer and render comparison. |
| [#2403](https://github.com/3b1b/manim/pull/2403) | Fix: remove gradient color artifacts by earcut-based triangulation | Deferred: alternate triangulation/dependency needs current-backend visual/performance validation. |
| [#2381](https://github.com/3b1b/manim/pull/2381) | Experimental Native Pyglet Windowing | Deferred: experimental windowing-backend replacement. |
| [#2361](https://github.com/3b1b/manim/pull/2361) | Made an attempt at creating a glow effect for mobjects. | Deferred: unfinished glow feature. |
| [#2377](https://github.com/3b1b/manim/pull/2377) | Add workaround for Pyglet 2.1 DPI scaling issues | Deferred: older Pyglet/DPI workaround needs current-backend platform validation. |
| [#2368](https://github.com/3b1b/manim/pull/2368) | Fix transparent objects rendering | Deferred: older transparency change needs current-backend regression cases; existing surface renders compared. |
| [#2369](https://github.com/3b1b/manim/pull/2369) | feat: integrate ImGui window into interactive embed loop for real-time | Deferred: ImGui feature and platform/dependency constraints. |
| [#2363](https://github.com/3b1b/manim/pull/2363) | docs: Update copyright information | Deferred: documentation metadata, outside critical runtime fixes. |
| [#2360](https://github.com/3b1b/manim/pull/2360) | Remove pkg_resources due to depracation Python >= 3.8 | Not needed for the tested baseline: no pkg_resources import in current manimlib; import succeeds with setuptools 84. |
| [#2357](https://github.com/3b1b/manim/pull/2357) | Added an option to rotate the numbers shown on NumberLine | Deferred: number-label orientation feature. |
| [#2319](https://github.com/3b1b/manim/pull/2319) | Create python-package.yml | Not integrated: older test-workflow proposal; a current supported-version workflow is provided instead. |

## Reproduce

Install a supported Python (3.10+) and native prerequisites, then:

```sh
python -m venv .venv
.venv/bin/python -m pip install -e . pytest
.venv/bin/python -m pytest tests -q
.venv/bin/python -m pip check
```

Rendering additionally needs an accessible GPU and FFmpeg. See `tests/render_compare.py` for baseline capture and comparison. Keep reference images tied to the baseline commit and runtime; cross-platform rasterization need not be byte-identical.
