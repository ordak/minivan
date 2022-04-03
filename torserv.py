# TOODO
#  -> add "changed" flags for all UI fields, esp. accumulated
#       [DONE] model in DSs
#       pass in handlers
#       utilize in JS
#  -> make frontend pass button indices not IDs
#  -> make events nonconsumable

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

import buttonset
import letterer

the_button_set = buttonset.ButtonSet()
the_letterer = letterer.Letterer()
the_button_push_queue = queue.Queue()


_DUMB_TEST = False
_SEQUENTIAL_TEST = False
_PREQUEUE_TEST = False


class MainViewHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("main.html")

class SensorsViewHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("sensors.html")

class InputOnlyViewHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("input_only.html")

class GetButtonFunctionsHandler(tornado.web.RequestHandler):
    def get(self):
        button_chars_map = the_button_set.get_labelchars__index()
        print(f'Here is map {button_chars_map}')
        self.write(json.dumps(button_chars_map))

class CycleButtonFunctionHandler(tornado.web.RequestHandler):
    def post(self):
        print('buttoncycle')
        button_index = int(self.request.body[-1:])
        print('button cycle {self.request.body}, {button_index}')
        the_button_set.cycle_button_function(button_index)
        self.write(the_button_set.get_labelchar(button_index))

class ForceButtonActionHandler(tornado.web.RequestHandler):
    def post(self):
        #print(json.loads(self.request.body))
        button_index = int(self.request.body[-1:])
        print(self.request.body, button_index)
        the_button_push_queue.put(button_index)

  # def EventsGenerator():
  #     global the_button_set
  #     global the_letterer
  #     while True:
  #         for eventInd in range(1, 5):
  #             yield from [{
  #                 "events" : [],
  #                 "left_letters" : alphaSet[:2],
  #                 "center_letter" : alphaSet[2],
  #                 "right_letters" : alphaSet[3:],
  #                 "accumulated" : accumulated,
  #                 }] * 7
  #             if random.random() > 0.8:
  #                 accumulated += alphaSet[2];
  #                 if random.random() > 0.8:
  #                     accumulated += ' ';
  #             alphaSet = next(alphaIter)
  #             yield {
  #                     "events" : [eventind],
  #                     "left_letters" : alphaSet[:2],
  #                     "center_letter" : alphaSet[2],
  #                     "right_letters" : alphaSet[3:],
  #                     "accumulated" : accumulated,
  #                     }
  # 
  # eventGenerator = EventsGenerator()

if _PREQUEUE_TEST:
    def addPreQueue():
        button_index = random.randint(1, 4)
        print(f'putting {button_index}')
        the_button_push_queue.put(button_index)

    prequeueTestTimer = tornado.ioloop.PeriodicCallback(addPreQueue,  1000)
    prequeueTestTimer.start()

class GetStateHandler(tornado.web.RequestHandler):
    def get(self):
        if _SEQUENTIAL_TEST:
            self.write(json.dumps(next(eventGenerator)))
        elif _DUMB_TEST:
            self.write(json.dumps({"fat": "yes"}))
        else:
            pushed_button_indexes = list()
            while not the_button_push_queue.empty():
                pushed_button_index = the_button_push_queue.get(block=False)
                pushed_button_indexes.append(pushed_button_index)
                print(f'button {pushed_button_index} pushed')
                the_button_set.act_on_letterer(pushed_button_index, the_letterer)
            self.write(json.dumps({
                "events" : pushed_button_indexes,
                "left_letters" : the_letterer.alphaset.get_left_letters(),
                "center_letter" : the_letterer.alphaset.get_center_letter(),
                "right_letters" : the_letterer.alphaset.get_right_letters(),
                "accumulated" : the_letterer.get_accumulator(),
            }))

class GetSensorsStateHandler(tornado.web.RequestHandler):
    def get(self):
        rd = dict()
        rd['test'] = [0, 1, 0, 1, 0]
        self.write(json.dumps(rd))

def make_app():

    return tornado.web.Application([

        # main app pages (views)
        (r"/", MainViewHandler),
        (r"/inputOnly", InputOnlyViewHandler),
        (r"/sensors", SensorsViewHandler),

        # dynamic operation endpoints
        (r"/getState", GetStateHandler),
        (r"/cycleButtonFunction", CycleButtonFunctionHandler),
        (r"/forceButtonAction", ForceButtonActionHandler),
        (r"/getButtonFunctions", GetButtonFunctionsHandler),
        (r"/getSensorsState", GetSensorsStateHandler),

        # misc endpoints
        (r"/(favicon.ico)", 
                tornado.web.StaticFileHandler, {"path": "static"}),
        (r"/static/(.*)",
                tornado.web.StaticFileHandler, {"path": "static"}),

    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
