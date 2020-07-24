import time

import serial


class SerialConnection:
    def __init__(self, device, baudrate=115200):
        self.device = device
        self.baudrate = baudrate
        self.connection = serial.Serial()

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def open(self):
        self.connection = serial.Serial(self.device, self.baudrate)
        self.connection.flushInput()

    def close(self):
        if self.is_open():
            self.connection.close()

    def send_at(self, command, expected_response, timeout):
        rec_buff = b''
        self.connection.write(f'{command}\r\n'.encode())
        time.sleep(timeout)

        if self.connection.in_waiting:
            time.sleep(0.01)
            rec_buff = self.connection.read(self.connection.in_waiting)

        if rec_buff != b'':
            decoded_response = rec_buff.decode()
            if expected_response not in decoded_response:
                error_msg = f"{command} ERROR, expected: '{expected_response}' but got: '{decoded_response}'"
                return False, error_msg
            else:
                return True, decoded_response

        error_msg = 'Device is not ready'
        return False, error_msg

    def is_open(self):
        return self.connection is not None and self.connection.is_open

    def flush_input(self):
        self.connection.flushInput()
