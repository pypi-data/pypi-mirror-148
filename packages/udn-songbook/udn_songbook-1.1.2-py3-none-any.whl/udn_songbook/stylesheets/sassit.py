#!/usr/bin/env python3
import sass
import sys

with open(sys.argv[1]) as sassfile:
    sass.compile(string=sassfile.read())
