import toolz.itertoolz as itz
import itertools

class AlphaSet:
    """Models bi-sliding window over full alphabet."""

    def __init__(self,
            alphabet='ABCDEFGHIJKLMNOPQRSTUVWXYZ 01234567890',
            sidelobe_size=2):
        self._alphabet = alphabet
        self._sidelobe_size = sidelobe_size
        self._update_window_indices()
        self._iterator = itz.sliding_window(5, itertools.cycle(list(alphabet)))
        self._current = next(self._iterator)

    def _update_window_indices(self):
        self._window_size = 2 * self._sidelobe_size + 1
        self._window_center_index = self._sidelobe_size

    def get_center_letter(self):
        return self._current[self._window_center_index]

    def get_left_letters(self):
        return self._current[:self._window_center_index]

    def get_right_letters(self):
        return self._current[(1 + self._window_center_index):]

    def advance_left(self):
        for _ in range(len(self._alphabet) - 1):
            self._current = next(self._iterator)

    def advance_right(self):
        self._current = next(self._iterator)

if __name__ == '__main__':
    dut = AlphaSet()
    assert(dut.get_left_letters()[0] == 'A')
    assert(dut.get_left_letters()[1] == 'B')
    assert(dut.get_center_letter() == 'C')
    assert(dut.get_right_letters()[0] == 'D')
    assert(dut.get_right_letters()[1] == 'E')
    dut.advance_left()
    assert(dut.get_center_letter() == 'B')
    dut.advance_left()
    assert(dut.get_center_letter() == 'A')
    dut.advance_right()
    assert(dut.get_center_letter() == 'B')
    dut.advance_right()
    assert(dut.get_center_letter() == 'C')
    dut.advance_right()
    assert(dut.get_center_letter() == 'D')
    dut.advance_right()
    assert(dut.get_center_letter() == 'E')
