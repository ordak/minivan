import time

import brainflow
from brainflow.board_shim import BoardShim, BrainFlowInputParams
from brainflow.board_shim import BoardIds
from brainflow.data_filter import DataFilter, FilterTypes, AggOperations

class GanglionHID:
    def __init__(self, serial_port='/dev/ttyACM0'):
        self._serial_port = serial_port
        self._board = None
        self._board_id = None
        self._board_version = None
        self._board_name = None
        self._emg_channel_inds = None
        self._accel_channel_inds = None
        self._timestamp_channel_ind = None
        BoardShim.enable_dev_board_logger()

    def __del__(self):
        time.sleep(1)  # to let library recover from
                       #   any immediately preceding
                       #   under-the-hood operations
                       # (this helps things work the
                       #   *next* run)
        self._end_session()

    def connect_to_board(self):
        params = BrainFlowInputParams()
        params.serial_port = self._serial_port
        self._board = BoardShim(BoardIds.GANGLION_BOARD, params)
        self._start_session()
        while not self._board.is_prepared():
            time.sleep(0.1)
        self._query_board_info()

    def _query_board_info(self):
        b = self._board 
        bid = self._board_id = self._board.get_board_id()

        self._board_version = b.get_version()
        self._board_id = self._board.get_board_id()
        self._board_name = b.get_device_name(bid)
        self._emg_channel_inds = b.get_emg_channels(bid)
        self._accel_channel_inds = b.get_accel_channels(bid)
        self._timestamp_channel_ind = b.get_timestamp_channel(bid)

    def print_board_info(self):
        print(f'OK.  {self._board_name} board, version {self._board_version}, ID {self._board_id}:')
        print(f'    timestamp on channel {self._timestamp_channel_ind}')
        print(f'    EMG on channels {self._emg_channel_inds}')
        print(f'    accel on channels {self._accel_channel_inds}')

    def _start_session(self):
        self._board.prepare_session()
        print(f'Board Descr {self._board.get_board_descr(1)}')
        self._board.start_stream(45000)

    def _end_session(self):
        if self._board is not None:
            self._board.stop_stream()
            self._board.release_session()

    def get_raw_data(self):
        return self._board.get_board_data() 


def main():
    dut = GanglionHID()
    dut.connect_to_board()
    dut.print_board_info()
    for _ in range(6):
        time.sleep(0.2)
        data = dut.get_raw_data()
        print(data.size, data.shape)

if __name__ == '__main__':
    main()
