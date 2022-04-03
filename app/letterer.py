import queue
import time
import random
import toolz.itertoolz as itz
import itertools
import json

import alphaset

class Letterer:

    SPACE_LETTER = ' '

    def __init__(self, sidelobe_size=2):
        self._alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ 01234567890'
        self.alphaset = alphaset.AlphaSet(self._alphabet)
        self._accumulator = "..."
        self._alphaset_changed = True
        self._accumulator_changed = True

    def get_alphaset_changed(self):
        return self._alphaset_changed

    def get_accumulator_changed(self):
        return self._accumulator_changed

    def ack_changes(self):
        self._alphaset_changed = False
        self._accumulator_changed = False

    def advance_left(self):
        self.alphaset.advance_left()
        self.alphaset_changed = True

    def advance_right(self):
        self.alphaset.advance_right()
        self.alphaset_changed = True

    def get_accumulator(self):
        return self._accumulator

    def accumulate_letter(self):
        self._accumulator += self.alphaset.get_center_letter()
        self._accumulator_changed = True

    def accumulate_space(self):
        self._accumulator += self.SPACE_LETTER
        self._accumulator_changed = True

    def deaccumulate(self):
        if len(self._accumulator):
            self._accumulator = self._accumulator[:-1]
            self._accumulator_changed = True

if __name__ == '__main__':
    dut = Letterer()
