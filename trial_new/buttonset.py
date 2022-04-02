from buttonfunction import ButtonFunction

class ButtonSet:

    def __init__(self, num_buttons=4):
        self._functions = dict()
        self._num_buttons = num_buttons
        self._changed = True

    def get_changed(self):
        return self._changed

    def ack_changes(self):
        self._changed = False

    def cycle_button_function(self, button_index):
        self._functions[button_index] = self._functions[button_index].get_next()
        self._changed = True

    def act_on_letterer(self, button_index, letterer):
        self._functions[button_index].act_on_letterer(letterer)

    def _load_default_functions(self):
        for load_index in range(1, self._num_buttons):
            if load_index == 1:
                self._functions[load_index] = ButtonFunction.LEFT
            elif load_index == 2:
                self._functions[load_index] = ButtonFunction.RIGHT
            elif load_index == 3:
                self._functions[load_index] = ButtonFunction.GO
            elif load_index == 4:
                self._functions[load_index] = ButtonFunction.SPACE
            else:
                self._functions[load_index] = ButtonFunction.NOP

if __name__ == '__main__':
    dut = ButtonSet(1)
    dut = ButtonSet(2)
    dut = ButtonSet(3)
    dut = ButtonSet(4)
    dut = ButtonSet(11)
