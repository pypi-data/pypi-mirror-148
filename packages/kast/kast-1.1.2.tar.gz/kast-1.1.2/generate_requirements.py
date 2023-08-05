#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright by: P.J. Grochowski

import argparse
import sys
from collections import OrderedDict
from dataclasses import dataclass
from enum import Enum, auto
from pathlib import Path
from typing import Dict, Optional, Tuple, Any, List

DIR_ROOT = Path(__file__).resolve().parent


def makeReqFilePath(suffix: Optional[str] = None) -> Path:
    suffix = f'_{suffix}' if suffix else ''
    return DIR_ROOT / f'requirements{suffix}.txt'


@dataclass
class Package:
    name: str
    version: Optional[str] = None
    osName: Optional[str] = None


Packages = Dict[str, Package]


def pkg(*args, **kwargs) -> Tuple[str, Package]:
    package = Package(*args, **kwargs)
    return package.name, package


@dataclass
class Requirements:
    filePath: Path
    packages: Packages


requirementsPkg = Requirements(
    filePath=makeReqFilePath(),
    packages=OrderedDict([
        pkg('typing_extensions', '3.10.0', 'posix'),  # Exists because of MPRIS Server.
        pkg('mpris_server', '0.3.4', 'posix'),

        pkg('winrt', '1.0.21033.1', 'nt'),

        pkg('tendo', '0.2.15'),
        pkg('psutil', '5.9.0'),
        pkg('av', '9.2.0'),
        pkg('pysubs2', '1.4.2'),
        pkg('pycaption', '2.0.8'),
        pkg('bottle', '0.12.19'),
        pkg('zeroconf', '0.30.0'),  # Exists because of PyChromecast.
        pkg('pychromecast', '11.0.0'),
        pkg('dataclasses-json', '0.5.7'),
        pkg('setproctitle', '1.2.3'),
        pkg('pyqt5', '5.15.6'),
    ]))

requirementsDev = Requirements(
    filePath=makeReqFilePath('dev'),
    packages=OrderedDict([
        pkg('setuptools'),
        pkg('setup-qt', '1.0.0'),
    ]))

requirementsDist = Requirements(
    filePath=makeReqFilePath('dist'),
    packages=OrderedDict([
        pkg('twine'),
        pkg('PyInstaller'),

        pkg('Pillow', osName='nt'),
    ]))


class EnumBase(Enum):

    def __str__(self):
        return self.name.lower()

    def __call__(self, *args, **kwargs):
        return str(self)

    @classmethod
    def all(cls):
        return [target() for target in cls]


class Arg(EnumBase):
    Target = 'use stable (default) dependencies or try latest'
    Pkg = 'create package requirements file'
    Dev = 'create development requirements file'
    Dist = 'create distribution requirements file'

    def help(self):
        return self.value


class Target(EnumBase):
    Stable = auto()
    Latest = auto()


REQUIREMENTS = {
    Arg.Pkg(): requirementsPkg,
    Arg.Dev(): requirementsDev,
    Arg.Dist(): requirementsDist,
}


def generate(*args: Any) -> None:
    parser = argparse.ArgumentParser()

    parser.add_argument(Arg.Target(), help=Arg.Target.help(), choices=Target.all(), nargs='?', default=Target.Stable())
    parser.add_argument(f'--{Arg.Pkg()}', help=Arg.Pkg.help(), action="store_true")
    parser.add_argument(f'--{Arg.Dev()}', help=Arg.Dev.help(), action="store_true")
    parser.add_argument(f'--{Arg.Dist()}', help=Arg.Dist.help(), action="store_true")

    parsedArgs = parser.parse_args(args)

    parsedArgsDict = vars(parsedArgs)
    genRegRequests = [parsedArgsDict[reqName] for reqName in REQUIREMENTS.keys()]
    if not any(genRegRequests):
        print("<!> No requirements files were selected!\n(Will fall back to generate package requirements file.)")
        parsedArgsDict[Arg.Pkg()] = True

    target = parsedArgsDict[Arg.Target()]
    separator = '==' if target == Target.Stable() else '>='

    print(f" -> Dependencies versions: {target}")

    def packageToLine(package: Package) -> str:
        return f'{package.name}' \
            + (f' {separator} {package.version}' if package.version else '') \
            + (f'; os_name == "{package.osName}"' if package.osName else '') \
            + '\n'

    def packgesToLines(packages: Packages) -> List[str]:
        return [packageToLine(package) for package in packages.values()]

    def linesToFile(filePath: Path, lines: List[str]) -> None:
        print(f" -> Generating file: '{filePath.name}'")
        with open(filePath, 'w') as fOutput:
            fOutput.writelines(lines)

    for reqName, requirements in REQUIREMENTS.items():
        if not parsedArgsDict[reqName]:
            continue

        linesToFile(requirements.filePath, packgesToLines(requirements.packages))


if __name__ == "__main__":
    generate(*sys.argv[1:])
