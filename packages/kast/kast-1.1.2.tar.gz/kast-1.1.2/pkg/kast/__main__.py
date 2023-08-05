#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright by: P.J. Grochowski

import argparse
import sys

from kast.KastApp import KastApp


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--debug", help="enable debug mode", action="store_true")
    parsedArgs = parser.parse_args()

    app = KastApp(debug=parsedArgs.debug)
    sys.exit(app.run())


if __name__ == "__main__":
    main()
