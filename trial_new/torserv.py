# TOODO
#  -> add "changed" flags for all UI fields, esp. accumulated
#  -> API:
#        entry pages
#          input-only window + full window
#          sensor-level window
#          input-only window (with input-output window open elsewhere)
#        buttons
#          cycleButtonFunction
#          forceButtonAction
#          getState
#          static serving (jquery.js)

import enum
import queue
import time
import random
import toolz.itertoolz as itz
import itertools
import json

import brainflow
from brainflow.board_shim import BoardShim, BrainFlowInputParams
from brainflow.board_shim import BoardIds
from brainflow.data_filter import DataFilter, FilterTypes, AggOperations
import asyncio
import tornado.ioloop
import tornado.web

_DUMB_TEST = False
_SEQUENTIAL_TEST = False
_PREQUEUE_TEST = True

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

    def to_char(self):
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

button_functions = {
        1 : ButtonFunction.LEFT,
        2 : ButtonFunction.RIGHT,
        3 : ButtonFunction.GO,
        4 : ButtonFunction.SPACE,
        }

class MainViewHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("template_spa.html")

class SensorsViewHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("template_spa.html")

class InputOnlyViewHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("template_spa.html")

class GetButtonFunctionsHandler(tornado.web.RequestHandler):
    def get(self):
        self.write(json.dumps({
            ei : button_functions[ei].to_char() for ei in button_functions
            }))

class CycleButtonFunctionHandler(tornado.web.RequestHandler):
    def post(self):
        #print(json.loads(self.request.body))
        event_index = int(self.request.body[-1:])
        print(self.request.body, event_index)
        button_functions[event_index] = button_functions[event_index].get_next()
        self.write(button_functions[event_index].to_char())

class ForceButtonActionHandler(tornado.web.RequestHandler):
    def post(self):
        #print(json.loads(self.request.body))
        event_index = int(self.request.body[-1:])
        print(self.request.body, event_index)
        eventQueue.put(event_index)

alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ 01234567890'
alphaIter = itz.sliding_window(5,
    itertools.cycle(list(alphabet)))
alphaSet = next(alphaIter)
accumulated = "Wiggle"

def EventsGenerator():
    global accumulated
    global alphaSet
    while True:
        for eventInd in range(1, 5):
            yield from [{
                "events" : [],
                "left_letters" : alphaSet[:2],
                "center_letter" : alphaSet[2],
                "right_letters" : alphaSet[3:],
                "accumulated" : accumulated,
                }] * 7
            if random.random() > 0.8:
                accumulated += alphaSet[2];
                if random.random() > 0.8:
                    accumulated += ' ';
            alphaSet = next(alphaIter)
            yield {
                    "events" : [eventind],
                    "left_letters" : alphaSet[:2],
                    "center_letter" : alphaSet[2],
                    "right_letters" : alphaSet[3:],
                    "accumulated" : accumulated,
                    }

eventGenerator = EventsGenerator()

eventQueue = queue.Queue()
if _PREQUEUE_TEST:
    def addPreQueue():
        event_index = random.randint(1, 4)
        print(f'putting {event_index}')
        eventQueue.put(event_index)

    prequeueTestTimer = tornado.ioloop.PeriodicCallback(addPreQueue,  1000)
    prequeueTestTimer.start()

def processEvent(event : ButtonFunction):
    global accumulated
    global alphaSet
    if event == ButtonFunction.LEFT:
        for _ in range(len(alphabet) - 1):
            alphaSet = next(alphaIter)
    elif event == ButtonFunction.RIGHT:
        alphaSet = next(alphaIter)
    elif event == ButtonFunction.GO:
        accumulated += alphaSet[2]
    elif event == ButtonFunction.SPACE:
        accumulated += ' '
    elif event == ButtonFunction.BACKSPACE:
        if len(accumulated):
            accumulated = accumulated[:-1]
    elif event == ButtonFunction.NOP:
        pass

class GetStateHandler(tornado.web.RequestHandler):
    def get(self):
        if _SEQUENTIAL_TEST:
            self.write(json.dumps(next(eventGenerator)))
        elif _DUMB_TEST:
            self.write(json.dumps({"fat": "yes"}))
        else:
            events = list()
            while not eventQueue.empty():
                newEventIndex = eventQueue.get(block=False)
                events.append(newEventIndex)
                processEvent(ButtonFunction(button_functions[newEventIndex]))
            self.write(json.dumps({
                "events" : events,
                "left_letters" : alphaSet[:2],
                "center_letter" : alphaSet[2],
                "right_letters" : alphaSet[3:],
                "accumulated" : accumulated,
            }))


def make_app():

    return tornado.web.Application([

        # main app pages (views)
        (r"/", MainViewHandler),
        (r"/inputOnly", InputViewHandler),
        (r"/sensors", SensorsViewHandler),

        # dynamic operation endpoints
        (r"/getState", GetStateHandler),
        (r"/cycleButtonFunction", CycleButtonFunctionHandler),
        (r"/forceButtonAction", ForceButtonActionHandler),
        (r"/getButtonFunctions", GetButtonFunctionsHandler),

        # misc endpoints
        (r"/static/(.*)",
                tornado.web.StaticFileHandler, {"path": "static"}),

    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
