""" module:: lin.adapter
    :synopsis: serial line LIN adapter
    moduleauthor:: Patrick Menschel (menschel.p@posteo.de)
    license:: CC-BY-NC
"""
from threading import Thread
from typing import Callable

from serial import Serial

from lin.common import LinFrame, LINE_END

from enum import IntEnum, auto


class OpMode(IntEnum):
    LinMaster = auto()
    Monitor = auto()
    LinSlave = auto()


class SLLinAdapter:

    def __init__(self, ser: Serial,
                 mode: OpMode = OpMode.LinMaster,
                 lin_baudrate: int = 19200):
        """
        Constructor
        :param ser: The serial device, typical ser = serial.Serial(port=<port>)
        """
        self.ser = ser
        self.rx_handler = Thread(target=self.handle_rx)
        self.listeners = []
        self.rx_handler.daemon = True
        self.rx_handler.start()
        self.set_lin_baudrate(baudrate=lin_baudrate)
        self.open(mode=mode)

    def __del__(self) -> None:
        """
        Destructor

        Sends close command to device for cleanup.
        :return: Nothing.
        """
        self.close()

    def __enter__(self):
        """
        With statement entry.
        :return: Self.
        """
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        With statement cleanup.
        :param exc_type: Unused, see python docs.
        :param exc_val: Unused, see python docs.
        :param exc_tb: Unused, see python docs.
        :return: Nothing.
        """
        self.close()

    def send(self, data: bytes):
        """
        Send data to adapter. LINE_END is attached automatically.
        :param data: The data.
        :return: The bytes written.
        """
        line = bytearray()
        line.extend(data)
        line.extend(LINE_END)
        return self.ser.write(data=line)

    def set_lin_baudrate(self, baudrate: int):
        cmd_mapping = {19200: b"S2",
                       9600: b"S1",
                       }
        cmd = cmd_mapping.get(baudrate)
        if cmd is None:
            raise ValueError("Not a valid baudrate {0}".format(baudrate))
        self.send(data=cmd)

    def open(self, mode: OpMode):
        """
        Send Open Command to Adapter.
        :return: The bytes written.
        """
        cmd_mapping = {OpMode.LinMaster: b"O",
                       OpMode.Monitor: b"l",  # a lowercase "L"
                       OpMode.LinSlave: b"L",
                       }

        return self.send(data=cmd_mapping.get(mode))

    def close(self):
        """
        Send Close Command to Adapter.
        :return: The bytes written.
        """
        return self.send(data=b"C")

    def handle_rx(self):
        """
        RX Thread.
        :return: Nothing.
        """
        buffer = bytearray()
        while True:
            data = self.ser.read(1)
            if data:
                buffer.extend(data)
                buffer.extend(self.ser.read(self.ser.inWaiting()))
                if LINE_END in buffer:
                    lines = buffer.split(LINE_END)
                    for line in lines:
                        self.handle_rx_line(line)
                    buffer.clear()
                    buffer.extend(lines[-1])

    def handle_rx_line(self, line) -> None:
        """
        RX line handling. branch by line/frame type.
        :param line: The line received.
        :return: Nothing.
        """
        line_lower = line.lower()
        if line_lower.startswith(b"t") \
                or line_lower.startswith(b"r"):
            self.handle_rx_lin_frames(LinFrame.from_bytes(line))

    def handle_rx_lin_frames(self, frame) -> None:
        """
        Handle received LIN frames. Call listeners.
        :param frame: The Lin Frame.
        :return: Nothing.
        """
        for listener in self.listeners:
            listener(frame)

    def add_listener(self, callback: Callable):
        """
        Add a listener callback for received LIN frames.
        :param callback: The callback function.
        :return: Nothing.
        """
        if callback not in self.listeners and callable(callback):
            self.listeners.append(callback)

    def send_lin_frame(self, frame: LinFrame):
        """
        Send a new lin frame to device.
        Apparently the device has internal list of RX Filters and TX Messages.
        Depending on OpMode, sending RTR frames and NON-RTR frames are handled differently.
        :param frame: The LinFrame.
        :return: The bytes written.
        """
        return self.send(data=frame.to_bytes())
