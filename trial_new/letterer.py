import enum
import queue
import time
import random
import toolz.itertoolz as itz
import itertools
import json

import alphaset

class Letterer:
    def __init__(self, sidelobe_size=2):
        self._alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ 01234567890'
        self._alpha_set = alphaset.AlphaSet(self._alphabet)
        self._accumulated = "Wiggle"

if __name__ == '__main__':
    dut = Letterer()
