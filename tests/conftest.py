"""Keep pytest's command-line options out of Manim's import-time CLI parser."""
import sys

saved_argv = sys.argv
try:
    sys.argv = sys.argv[:1]
    import manimlib  # noqa: F401
finally:
    sys.argv = saved_argv
