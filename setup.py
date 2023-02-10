from os import path
from pathlib import Path

from patch import fromfile

# from setuptools.build_meta import build_sdist as setuptools_build_sdist
# from setuptools.build_meta import build_wheel as setuptools_build_wheel


def _post_install(_a=None, _b=None):
    patch = fromfile(
        path.join(
            Path(__file__).resolve().parent, "patches", "patch-orion.diff"
        )
    )
    if not patch:
        raise Exception("Failed to load patch")
    print("")
    patch.apply(strip=0, root=".")


_post_install()
