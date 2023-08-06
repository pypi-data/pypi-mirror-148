""" module:: lin.common
    :synopsis: common parts of lin package
    moduleauthor:: Patrick Menschel (menschel.p@posteo.de)
    license:: CC-BY-NC
"""
from enum import IntFlag

LINE_END = b"\r"


class LinFlag(IntFlag):
    RTR = 1


class LinFrame:

    def __init__(self,
                 lin_id: int,
                 lin_data: bytes,
                 lin_flags: LinFlag = LinFlag(0)):
        """
        Constructor
        :param lin_id: LIN ID
        :param lin_data: Data bytes.
        :param lin_flags: The flags.
        """
        self.id = lin_id
        self.data = lin_data
        self.flags = lin_flags

    @classmethod
    def from_bytes(cls, byte_repr: bytes):
        """
        Constructor from byte representation
        :param byte_repr: The bytes representation.
        :return: The LinFrame instance.
        """
        lin_flags = LinFlag(0)
        lin_data = bytes(0)
        if byte_repr[0] == b"t"[0]:
            # sff
            lin_id = byte_repr[1:4]  # 3 bytes
            lin_dlc = int(byte_repr[4:5], 16)  # 1 byte
            lin_data = byte_repr[5:5 + lin_dlc]
        elif byte_repr[0] == b"T"[0]:
            # eff
            lin_id = byte_repr[1:9]  # 8 bytes
            lin_dlc = int(byte_repr[9:10], 16)  # 1 byte
            lin_data = byte_repr[10:10 + lin_dlc]
        elif byte_repr[0] == b"r"[0]:
            # sff rtr
            lin_id = byte_repr[1:4]  # 3 bytes
            lin_dlc = int(byte_repr[4:5], 16)  # 1 byte
            lin_flags = LinFlag.RTR
        elif byte_repr[0] == b"R"[0]:
            # eff rtr
            lin_id = byte_repr[1:9]  # 8 bytes
            lin_dlc = int(byte_repr[9:10], 16)  # 1 byte
            lin_flags = LinFlag.RTR
        else:
            raise ValueError("Not a valid byte_repr {0}".format(byte_repr.hex()))
        return LinFrame(lin_id=int(lin_id, 16),
                        lin_flags=lin_flags,
                        lin_data=lin_data)

    def to_bytes(self) -> bytes:
        """
        Format frame to byte representation.
        :return: The byte representation.
        """
        byte_repr = bytearray()
        cmd_char = "t"
        if self.flags == LinFlag.RTR:
            cmd_char = "r"
        if self.id > 0x7FF:
            byte_repr.extend("{0}{1:08X}{2:X}".format(cmd_char.upper(), self.id, len(self.data)).encode())
        else:
            byte_repr.extend("{0}{1:03X}{2:X}".format(cmd_char, self.id, len(self.data)).encode())

        byte_repr.extend(self.data)
        return bytes(byte_repr)
