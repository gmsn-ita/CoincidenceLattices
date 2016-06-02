from distutils.core import setup, Extension

clattices_loop = Extension("clattices_loop", sources = ["clattices_loop.c", "loop.c"])

setup(
    name = "CLatticesLoop",
    version = '1.0',
    ext_modules=[clattices_loop],
)
