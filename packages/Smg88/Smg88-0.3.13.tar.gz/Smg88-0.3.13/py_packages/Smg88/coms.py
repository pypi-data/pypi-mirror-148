from enum import auto
from typing import List, overload
from Smg88.errors import ProgrammerErrorHandle
from loghelp import EnumParent
import errors
from errors import Error


class PointRole(EnumParent):
    Server = auto()
    Node = auto()


class PointType(EnumParent):
    LocalToLocal = auto()
    LocalToRemote = auto()
    RemoteToLocal = auto()
    RemoteToRemote = auto()


class PacketItem():
    _content: List[str]

    def __init__(self, *strings):
        self._content = strings

    @property
    def content(self):
        return self._content

    @property
    def msg(self):
        return self._content[0]

    def __str__(self) -> str:
        return self.msg


class Communicator():
    """Represents a communication 'stream' or option for communicating with something, usually a Point

    isasync: bool = True
    requestRole(): PointRole
    requestType(): PointType
    buffer: List[Item] property get
    bufferSend: List[Item] property get

    get(num: int): Item
        Takes (num number of) items off the _buffer and gives it to the caller
    send(*items: Item): Item
        Takes items and puts it on the _bufferSend

    _buffer: List[Item]
        An array that represents the data received  
    _bufferSend: List[Item]
        An array that represents data yet to be sent (on next eventloop perhaps?)

    _send(num: int): Item
        Asynchronously sends (num number of) items from the _bufferSend start
    _receive(*packets): Item
        Is called to receive packet/s, appends then to _buffer end

    """
    isasync: bool

    _buffer: List[str]
    _bufferSend: List[PacketItem]

    def __init__(self, isasync: bool = True):
        self.isasync = isasync
        self._buffer = []
        self._bufferSend = []

    @property
    def buffer(self):
        return self._buffer

    @property
    def bufferSend(self):
        return self._bufferSend

    def get(self, num: int):
        raise NotImplementedError

    def send(self, *packets: PacketItem):
        raise NotImplementedError

    def _receive(self, *packets: PacketItem):
        raise NotImplementedError

    def _send(self, *packets: PacketItem):
        raise NotImplementedError


class CommunicatorErrors(errors.Errors):
    """Errors for the Communicator class"""
    ...


class CommunicatorBufferError(CommunicatorErrors):
    """Errors for the Communicator class related to buffers"""
    ...


class CommunicatorEmptyBuffer(CommunicatorBufferError):
    """Raised when strict and the buffer is empty"""
    ...


class CommunicatorPurgeBuffer(CommunicatorBufferError):
    """Raised when strict and the buffer is purged"""
    ...


class CLICommunicator(Communicator):
    def send(self, *packets: PacketItem) -> None:
        (self._bufferSend.append(packet) for packet in packets)

    @overload
    def get(self, num: int = 1) -> List[PacketItem]:
        ...

    @overload
    def get(self, all: bool = True) -> List[PacketItem]:
        ...

    def get(self, /, num: int = 1, *, all: bool = False, retain: bool = ..., strict: bool = True) -> List[PacketItem]:
        """Gets (num number of) items from the buffer

        Args:
            num (int, optional): how many items to take from the buffer. Defaults to 1.
            all (bool, optional *overrides num*): whether to take all items from the buffer. Defaults to False.
            retain (bool, optional): whether to retain taken items or to pop them. Defaults to False, unless all then *defaults* to True
            strict (bool, optional): whether to raise errors on bad practices. Defaults to True.

        Raises:
            CommunicatorPurgeBuffer: Raises when strict and the buffer is purged, as in all=True and retain=False (note: retain defaults to True when all=True to avoid this)
            CommunicatorEmptyBuffer: Raises when the items requested (through setting num) are not in the buffer

        Returns:
            List[PacketItem]: A list of PacketItems taken from the buffer
        """
        if all:
            num = len(self._buffer)
            if not retain:
                # TODO Add warning for purging self._buffer when !strict
                if strict:
                    raise CommunicatorPurgeBuffer(errorHandle=ProgrammerErrorHandle(
                        "Try not to set all=True and retain=False else you will purge (delete the whole of) the self._buffer!"))
        elif retain is ...:
            retain = False
        if type(num) is not int:
            raise errors.InappropriateRequest("num must be an int if provided and all=False", errorHandle=ProgrammerErrorHandle(
                "Either set all=True or provide an int for the num parameter when using get()"))
        if num > len(self._buffer):
            raise CommunicatorEmptyBuffer(errorHandle=ProgrammerErrorHandle(
                "Do not request more items than are in the buffer, use all=True and/or retain=True"))
        if retain:
            return [self._buffer[i] for i in range(num)]
        return [self._buffer.pop(0) for i in range(num)]

    def _receive(self, *packets: PacketItem) -> None:
        self._bufffer.append(packets)

    def _send(self, num: int = 1) -> None:
        print(f"P{i}: {self._buffer.pop(0)}\n" for i in range(num))


class Communication():
    """Represents a possible communication 'target' and provides an array of Communicator objects to use to communicate with is

    communicators: List[Communicator]
    requestRole(): PointRole
    requestType(): PointType
    """

    def __init__(self) -> None:
        ...


class Point():
    """Class that represents a single point (to current python interpreter) in the IOT

    role: PointRole
    type: PointType

    requestPoints(): Dict
        Returns a dictionary of Communication objects for each point found that responded in my IOT
    requestServers(): Dict
        Returns a dictionary of Communication objects for each server found that responded in my IOT
    requestNodes(): Dict
        Returns a dictionary of Communication objects for each node found that responded in my IOT

    """

    def __init__(self):
        ...


def tests():
    """Tests for the coms.py module"""
    p = Point()
    test = CLICommunicator()
    test.send(PacketItem("Hello world!"))
    test.send(test.get())
    ...


if __name__ == "__main__":
    tests()
