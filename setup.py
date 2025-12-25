from setuptools import setup, Extension
from Cython.Build import cythonize

names = ['shared.bytes', 'shared.packet', 'shared.glm', 'aoslib.vxl', "aoslib.kv6", "aoslib.world"]
modules = []
include = []

link_args = []
compile_args = ['-std=c++11']

exclude_cpp = ['shared.bytes', 'shared.packet', 'aoslib.kv6', 'aoslib.world', 'aoslib.vxl']
# special_case = ['aoslib.world']  # Special case for world, includes vxl_c.cpp but not world_c.cpp
special_case = []

for name in names:
    if name in exclude_cpp:
        modules.append(Extension(
            name,
            [f"{name.replace('.', '/')}.pyx"],
            include_dirs=[f"{name.split('.')[0]}"],
        ))
    elif name in special_case:
        modules.append(Extension(
            name,
            [f"{name.replace('.', '/')}.pyx", 'aoslib/vxl_c.cpp'],  # Include vxl_c.cpp but not world_c.cpp
            language="c++",
            include_dirs=['.', f"{name.split('.')[0]}", 'shared'],
            extra_compile_args=compile_args
        ))
    else:
        modules.append(Extension(
            name,
            [f"{name.replace('.', '/')}.pyx", f"{name.replace('.', '/')}_c.cpp"],
            language="c++",
            include_dirs=['.', f"{name.split('.')[0]}", 'shared'],
            extra_compile_args=compile_args
        ))

setup(
    name='ext',
    ext_modules=cythonize(modules, annotate=True, compiler_directives={'language_level': 3})
)