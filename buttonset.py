from buttonfunction import ButtonFunction

class ButtonSet:

    def __init__(self, num_buttons=4):
        self._functions = dict()
        self._num_buttons = num_buttons
        self._load_default_functions()

    def get_changed(self):
        return self._changed

    def ack_changes(self):
        self._changed = False

    def cycle_button_function(self, button_index):
        print('CBF')
        self._functions[button_index] = self._functions[button_index].get_next()
        self._changed = True

    def act_on_letterer(self, button_index, letterer):
        self._functions[button_index].act_on_letterer(letterer)

    def get_labelchar(self, button_index):
        return self._functions[button_index].to_labelchar()

    def get_labelchars__index(self):
        return {
            index : self.get_labelchar(index) \
                for index in range(1, 1 + self._num_buttons)}



    def _load_default_functions(self):
        for load_index in range(1, 1 + self._num_buttons):
            if load_index == 1:
                self._functions[load_index] = ButtonFunction.RIGHT
            elif load_index == 2:
                self._functions[load_index] = ButtonFunction.LEFT
            elif load_index == 3:
                self._functions[load_index] = ButtonFunction.GO
            elif load_index == 4:
                self._functions[load_index] = ButtonFunction.SPACE
            elif load_index == 5:
                self._functions[load_index] = ButtonFunction.BACKSPACE
            else:
                self._functions[load_index] = ButtonFunction.NOP
        self._changed = True

if __name__ == '__main__':
    dut = ButtonSet(1)
    dut = ButtonSet(2)
    dut = ButtonSet(3)
    dut = ButtonSet(4)
    dut = ButtonSet(11)
