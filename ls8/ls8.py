#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *

cpu = CPU()

# cpu.load("ls8/examples/mult.ls8")
# cpu.load("ls8/examples/stack.ls8")
cpu.load()
cpu.run()