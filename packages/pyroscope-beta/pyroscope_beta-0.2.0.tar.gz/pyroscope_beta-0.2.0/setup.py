import os
from setuptools import find_packages, setup
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
os.chdir(SCRIPT_DIR)
LIB_DIR = str(SCRIPT_DIR / "lib")

def build_native(spec):
    # Step 1: build the rust library
    build = spec.add_external_build(
        cmd=['cargo', 'build', '--release'],
        path=LIB_DIR
    )

    # Step 2: package the compiled library
    spec.add_cffi_module(module_path='pyroscope_beta._native',
            dylib=lambda: build.find_dylib('pyroscope_ffi',
                in_path='target/release'),
            header_filename=lambda:
            build.find_header('pyroscope_ffi.h',in_path='include'),
            rtld_flags=['NOW', 'NODELETE']
    )

setup(
    milksnake_tasks=[build_native],
)
