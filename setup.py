from setuptools import setup, Extension
from Cython.Build import cythonize
import os

extensions = [
    Extension(
        "shared.bytes",
        ["shared/bytes.pyx"],
        include_dirs=[os.path.join(os.path.dirname(__file__), "shared")],
    ),
    Extension(
        "shared.packet",
        ["shared/packet.pyx"],
        include_dirs=[os.path.join(os.path.dirname(__file__), "shared")],
    ),
    Extension(
        "shared.glm",
        ["shared/glm.pyx", "shared/glm_c.cpp"],
        include_dirs=[os.path.join(os.path.dirname(__file__), "shared")],
        language="c++",
    )
]

setup(
    name="shared",
    ext_modules=cythonize(extensions, language_level=3),
    packages=["shared"],
    package_data={"shared": ["*.pxd"]},
)
