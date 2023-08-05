from setuptools import setup
import pathlib
import os

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

__version__ = "0.0.8"

packages = ["iro"]
ext_modules = None
console_scripts = [
    "iro=iro.Iro:main",
]
cmdclass = {}
data_files = None

if os.name == "nt":
    # from setuptools import Extension
    # from setuptools.command.build_ext import build_ext
    from pybind11.setup_helpers import Pybind11Extension, build_ext

    packages.append("toori")
    console_scripts.append("toori=toori.Toori:main")
    cmdclass = {"build_ext": build_ext}
    ext_modules = [
        Pybind11Extension(
            "_toori",  # PYBIND11_MODULE defined in toori.cpp
            ["src/toori/_toori.cpp"],
            include_dirs=["external/WinDivert-2.2.0-A/include"],
            library_dirs=["external/WinDivert-2.2.0-A/x64"],
            libraries=["WinDivert"],  # WinDivert.lib
        ),
    ]
    data_files = [
        "external/WinDivert-2.2.0-A/x64/WinDivert.dll",
        "external/WinDivert-2.2.0-A/x64/WinDivert64.sys",
        "external/WinDivert-2.2.0-A/x64/WinDivert.lib",
        "external/WinDivert-2.2.0-A/include/windivert.h",
    ]

setup(
    name="Toori",
    version=__version__,
    description="Simple Python/C++ library for tunneling network traffic over http(s).",
    long_description=README,
    long_description_content_type="text/markdown",
    # headers=["external/WinDivert-2.2.0-A/include/windivert.h"],
    packages=packages,
    package_dir={
        "": "src"
    },  # tell setuptools that all packages will be under the 'src' directory and nowhere else
    ext_modules=ext_modules,
    data_files=data_files,
    cmdclass=cmdclass,
    python_requires=">=3.7",
    zip_safe=False,
    entry_points={
        "console_scripts": console_scripts,
    },
    install_requires=["scapy", "aiohttp", "python-socketio", "python-engineio"]
)
