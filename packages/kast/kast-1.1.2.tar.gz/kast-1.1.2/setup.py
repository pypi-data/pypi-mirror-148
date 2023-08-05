#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright by: P.J. Grochowski

import shutil
import sys
from pathlib import Path
from typing import Type

from setuptools import Command, find_packages
from setuptools import setup
from setuptools.command.build_py import build_py

NAME_PACKAGE_ROOT = 'pkg'

DIR_ROOT = Path(__file__).resolve().parent
DIR_PACKAGE_ROOT = DIR_ROOT / NAME_PACKAGE_ROOT

REL_PATH_DATA_FILES = Path('build') / 'data_files'

sys.path.append(str(DIR_PACKAGE_ROOT))

from kast import __app_description__, __app_name__, __email__, __version__, __author__, __package_name__, __app_url__


def assert_working_dir():
    currDir = Path().resolve()
    if currDir != DIR_ROOT:
        print(f"[ERROR]: Please change working directory: '{currDir}' -> '{DIR_ROOT}'")
        sys.exit(1)


def get_requirements():
    fileRequirements = DIR_ROOT / 'requirements.txt'

    if not fileRequirements.exists():
        print(f"<!> Could not find '{fileRequirements.name}' file. It will be generated.")
        from generate_requirements import generate
        generate()

    with open(fileRequirements) as fInput:
        return fInput.read().splitlines()


def get_long_description():
    fileReadme = DIR_ROOT / 'README.md'

    with open(fileReadme) as fInput:
        return fInput.read()


def prepare_data_files():
    dirDataFiles = DIR_ROOT / REL_PATH_DATA_FILES

    dirDataFiles.mkdir(parents=True, exist_ok=True)

    fileIconSrc = DIR_PACKAGE_ROOT / __package_name__ / 'assets' / 'appicon.png'
    fileIconDst = dirDataFiles / f'{__package_name__}.png'
    shutil.copyfile(fileIconSrc, fileIconDst)

    fileDesktop = dirDataFiles / f'{__package_name__}.desktop'
    with open(fileDesktop, 'w') as fOutput:
        fOutput.write(
            "[Desktop Entry]\n"
            "Type=Application\n"
            "Encoding=UTF-8\n"
            f"Name={__app_name__}\n"
            f"Icon={fileIconDst.name}\n"
            f"Exec={__package_name__}\n"
            "Categories=AudioVideo;\n"
            "Terminal=false\n"
        )


assert_working_dir()

kwargs = {'cmdclass': {}}


def add_cmd(cmd: str, cmdType: Type) -> None:
    kwargs['cmdclass'][cmd] = cmdType


try:
    from setup_qt import build_qt

    add_cmd('build_qt', build_qt)
    kwargs['options'] = {
        'build_qt': {
            'packages': [f'{NAME_PACKAGE_ROOT}/{__package_name__}'],
            'filename_ui': '{name}.py',
        },
    }

except ImportError:
    print("<!> Could not import 'setup_qt'. Some development feature will not be available!")


class CmdDistclean(Command):
    description = "removes 'build' and 'dist' dirs regardless of their contents"
    user_options = []

    def initialize_options(self) -> None:
        pass

    def finalize_options(self) -> None:
        pass

    def run(self) -> None:
        self.removeIfExists(DIR_ROOT / 'build')
        self.removeIfExists(DIR_ROOT / 'dist')

    def removeIfExists(self, path: Path) -> None:
        if path.exists():
            print(f"Removing: {path}")
            shutil.rmtree(path)


class CmdBuild(build_py):
    def run(self):
        prepare_data_files()
        super().run()


add_cmd('distclean', CmdDistclean)
add_cmd('build_py', CmdBuild)

setup(
    name=__package_name__,
    version=__version__,
    license="MIT",
    url=__app_url__,
    author=__author__,
    author_email=__email__,
    description=__app_description__,
    long_description=get_long_description(),
    long_description_content_type='text/markdown',
    package_dir={'': NAME_PACKAGE_ROOT},
    packages=find_packages(NAME_PACKAGE_ROOT),
    include_package_data=True,
    zip_safe=False,
    install_requires=get_requirements(),
    scripts=[f'script/{__package_name__}'],
    data_files=[
        ('share/applications', [str(REL_PATH_DATA_FILES / f'{__package_name__}.desktop')]),
        ('share/pixmaps', [str(REL_PATH_DATA_FILES / f'{__package_name__}.png')]),
    ],
    python_requires='>=3.7',
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    **kwargs
)
