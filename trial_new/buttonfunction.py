import enum
import toolz.itertoolz as itz

class ButtonFunction(enum.IntEnum):
    LEFT = 1
    RIGHT = 2
    GO = 3
    SPACE = 4
    BACKSPACE = 5
    NOP = 6

    def get_next(self):
        for (testName, testObj), (succName, succObj) in \
                itz.sliding_window(2,
                        list(self.__class__.__members__.items()) * 2):
            if testObj == self:
                return succObj

    def to_labelchar(self):
        if self == ButtonFunction.LEFT:
            return '⇦' # '◀'
        elif self == ButtonFunction.RIGHT:
            return '⇨' # '▶'
        elif self == ButtonFunction.GO:
            return '↧' # '✔'
        elif self == ButtonFunction.SPACE:
            return '□ '
        elif self == ButtonFunction.BACKSPACE:
            return '⌫'''
        elif self == ButtonFunction.NOP:
            return '·'

    def act_on_letterer(self, letterer):
        if self == ButtonFunction.LEFT:
            letterer.advance_left()
        elif self == ButtonFunction.RIGHT:
            letterer.advance_right()
        elif self == ButtonFunction.GO:
            letterer.accumulate_letter()
        elif self == ButtonFunction.SPACE:
            letterer.accumulate_space()
        elif self == ButtonFunction.BACKSPACE:
            letterer.deaccumulate()
        elif self == ButtonFunction.NOP:
            pass

if __name__ == '__main__':
    dut = ButtonFunction(2)
