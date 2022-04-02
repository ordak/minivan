
import time

import brainflow
from brainflow.board_shim import BoardShim, BrainFlowInputParams
from brainflow.board_shim import BoardIds
from brainflow.data_filter import DataFilter, FilterTypes, AggOperations

def main():
    BoardShim.enable_dev_board_logger()
    print("Hello")
    params = BrainFlowInputParams()
    params.serial_port = '/dev/ttyACM0'

    board = BoardShim(BoardIds.GANGLION_BOARD, params)

    board.prepare_session()
    # board.start_stream () # use this for default options
    print(f'Board ID {board.get_board_id()}')
    print(f'Board Descr {board.get_board_descr(1)}')
    board.start_stream(45000)
    time.sleep(10)
    # data = board.get_current_board_data (256) # get latest 256 packages or less, doesnt remove them from internal buffer
    data = board.get_board_data()  # get all data and remove it from internal buffer
    print(len(data))
    board.stop_stream()
    board.release_session()

if __name__ == '__main__':
    main()
