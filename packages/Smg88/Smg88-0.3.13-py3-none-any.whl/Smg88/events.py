import functools
import json
from json import JSONDecodeError
from types import EllipsisType
from typing import Callable, Dict, List
from . import loghelp
from .loghelp import o_str, o_Callable, s_sable, sT_sable, s_str
from . import errors
from . errors import ProgrammerError, ProgrammerErrorHandle, SafeCatchAll


class EventError(errors.Error):
    """The base class for all errors in this module
    """
    ...


class EventSubscriberCallbackError:
    """Class of error parenting all errors related to subscriber callbacks
    """
    ...


class EventSubscriberCallbackErrorNotCallable(EventSubscriberCallbackError):
    """Error raised when a subscriber callback is not callable
    """
    ...


class Event():
    """Event class represents an event that can be posted and subscribed to

    Attributes:
      channel: str
        The channel to which the event is said to be existing in
      name: str
        The name of the event, used for easy identification
      payload: str
        The payload of the event, used to convey the information of the event, usually in JSON format
    """
    channel: o_str = ...
    name: o_str = ...

    payload: o_str = ...

    def __init__(self, *,
                 channel: o_str = ...,
                 name: o_str = ...,
                 payload: o_str = ...,
                 **kwargs) -> None:
        if channel is ...:
            # TODO add warning for instinating event without channel handle
            ...
        self.channel = s_str(channel)
        if s_sable(self.channel) is False:
            # TODO add warning for instinating event with non-serializable (not str) channel handle
            ...
        if name is ...:
            # TODO add warning for instinating event without name handle
            ...
        self.name = name
        if type(self.name) is not str:
            # TODO add warning for instinating event with non-serializable (not str) name handle
            ...
        if payload is ...:
            # TODO add warning for instinating event without payload
            ...
        self.payload = payload
        if s_sable(self.payload) is False:
            # TODO add warning for instinating event with non-serializable (not str) payload
            ...

    def send(self, /, stage=..., **kwargs) -> None:
        """Posts the event to the given EventStage as if EventStage.post(event=self) was called (hint it is : )

          Args:       
            stage: EventStage
              The stage to which the event is sent too
              Note: Annotation for stage is not possible as this is a convenience method
        """
        try:
            stage.post(event=self)
        except SafeCatchAll as err:
            # TODO add warning for eventstage post failure
            raise err


class HeartBeatEvent(Event):
    """Event class representing a heartbeat event

    For __docs__ on Event, see Event.__doc__ NOT here!
    Attributes:
      channel: str = "Smg88::HeartBeat"
        The channel to which the event is said to be existing in
      name: str = f"Smg88 HeartBeat ({self.count}) at about {loghelp.now()}"
      payload: str = JSON Format below:
        {
          "count": int,
          "approxtime": str,
        }
    """
    count: int

    def __init__(self, /,
                 count: int = -1,
                 *,
                 channel: o_str = ...,
                 name: o_str = ...,
                 timestr: o_str = ...,
                 payload: o_str = ...,
                 **kwargs
                 ) -> None:
        self.count = count
        if type(self.count) is not int:
            # TODO add warning for non-serializable (not int) count
            ...
        self.timestr = timestr
        if self.timestr is ...:
            self.timestr = loghelp.now()
        if type(self.timestr) is not str:
            # TODO add warning for non-serializable (not str) timestr
            ...
        _payload: Dict[str, sT_sable] = payload
        if _payload is ...:
            _payload = {
                "count": self.count,
                "approxtime": self.timestr,
            }
        if type(_payload) is Dict:
            _payload = s_jsonify(_payload)
        self.payload = _payload
        self.name = name
        if self.name is ...:
            self.name = f"Smg88 HeartBeat ({self.count}) at about {self.timestr}"
        if type(self.name) is not str:
            # TODO add warning for non-serializable (not str) name
            ...
        try:
            self._package = json.dumps(self.payload)
        except SafeCatchAll as err:
            # TODO properly handle this error :)
            ...
        super().__init__(channel=channel, name=name, payload=payload, **kwargs)


class EventStage():
    """Represents a place for events to occur
    Events are objects that have a channel and a name, all events are passed to all subscribers of that event's channel

    Events can be posted to this stage by instancing the 'Event' object and calling EventStageInstance.post(EventInstance)
    Or, shorthand, call 'send' on an Event instance with the EventStage instance

    Methods:
      subscribe(callback)
        Subscribes the function to be called with all Event objects posted to this stage under the channel (default __name__ of function)

    Attributes:
      nameHandle: str (constructable)
        A common name for the EventStage, needed to connect to the EventStage
      subscriptions: Dict[str, Callable.__name__]
        Is a property exposing the subscriptions of the stage, the key is the channel and the value is the name of the subscriber's function

      _subscriptions: Dict[str, Callable]
        A dictionary of channel names to functions that are subscribed to that channel name
      _eventBuffer: List[Event]
        A buffer of events to post to the stage
    """
    _subscriptions: Dict[str, List[Callable]]
    nameHandle: str

    _eventBuffer: List[Event]

    @property
    def eventBuffer(self) -> List[Event]:
        return self._eventBuffer

    @property
    def channels(self) -> List[str]:
        return list(self._subscriptions.keys())

    def __init__(self, /,
                 nameHandle: o_str = ...
                 ) -> None:
        self.nameHandle = nameHandle
        if self.nameHandle is ...:
            # TODO add warning for instinating an EventStage without a nameHandle
            ...
        if type(self.nameHandle) is not str:
            # TODO add warning for instinating an EventStage without a serializable (str) nameHandle
            ...
        self._subscriptions = {}
        self._eventBuffer = []

    def post(self, /, event: Event | ... = ...,) -> None:
        if event is ...:
            # TODO add warning for not passing an event
            raise errors.InappropriateRequest(f"No event was passed to the post method {event}",
                                              errorHandle=errors.ProgrammerErrorHandle("Must pass an event to the post method (of an EventStage instance or child of such)"))
        self._eventBuffer.append(event)

    def release(self, /,
                channel: o_str = ...,
                ) -> None:
        """_posts all events in the buffer that are in the given channel

        Overloads:
          release()
            Release the latest event in the buffer: _post(1, all=False, retain=False)
          release("channel")
            Release all of the events conforming to that channel: _release(channel="channel")

        Args:
            channel (str, optional): Channel to post all buffered events that are in.
        """
        if channel is ...:
            self._post(num=1, all=False, retain=False)
        else:
            self._release(channel=channel)

    def _release(self, /,
                 channel: str | EllipsisType = ...,
                 ) -> None:
        if channel is ...:
            raise errors.InappropriateRequest("No channel was passed to the _release method", errorHandle=errors.ProgrammerErrorHandle(
                "Must pass a channel to the _release method (of an EventStage instance or child of such)"))
        for event in self._eventBuffer:
            if event.channel == channel:
                self._handle(event, remove=True)

    def subscribe(self, /,
                  callback: o_Callable = ...,
                  *,
                  channel: o_str = ...,
                  ) -> None:
        """Subscribes a callback to the given channel (defaults to callback.__name__)

        Args:
            callback (Callable): Callable to call with event=event when event is posted on that channel. Defaults to ....
            channel (str, optional): The exact channel to subscribe the callback to. Defaults to callback.__name__
        """
        # TODO add some info for this function as it is very useful
        if channel is ...:
            channel = callback.__name__
        print(f"Subscribing to EventStage {callback=} under {channel=}")
        if channel not in self.channels:
            self._subscriptions[channel] = []
        self._subscriptions[channel].append(callback)

    def _post(self, /, num: int = 1, *, all: bool = False, retain: bool | EllipsisType = ..., **kwargs) -> None:
        if all:
            if retain is ...:
                retain = True
            if not retain:
                # TODO Warn for purging buffer
                ...
            self._postn(num=len(self._eventBuffer),
                        retain=bool(retain), **kwargs)
        else:
            self._postn(num=num, retain=retain, **kwargs)

    def _postn(self, /, num: int = 1, *, retain: bool = False, **kwargs) -> None:
        for _ in range(num):
            self._handle(self._eventBuffer.pop(0))

    def _handle(self, /, event: Event, *, remove: bool = ...) -> None:
        if remove is ...:
            remove = False
        if event.channel in self.channels:
            subscribers = self._subscriptions[event.channel]
            for subscriber in subscribers:
                # TODO add warning for subscriber callback error
                subscriber(event=event)
        else:
            # TODO add warning for no subscribers to given event channel
            ...
        if remove:
            self._eventBuffer.remove(event)


class EventStageHeartbeat():
    """Represents a heartbeat for an AutoEventStage, subscribes to its own channel and reposts it with count++

    Attributes:
      SubscribeHandle: Callable
        Represents the handle 

    Methods:
      pump(): Pump this heartbeat once more!
      subscribe
    """

    counter: int = ...
    approxlastpump: str = ...

    stages: List[EventStage] = ...
    defaultChannel: str = "Smg88::heartbeat::pulse"

    @staticmethod
    def __subscribeHandle(event: Event = ...) -> None:
        """Internal function to be called on a heartbeat

        Args:
            event (Event): Event to be analysed
        """
        print("Cool event handle called!")
        print(f"{event=}")

    def __init__(self, *, stage: EventStage = ..., stages: List[EventStage] = ..., countstart: int = -1) -> None:
        self.counter = countstart
        if type(self.counter) is not int:
            # TODO add warning for non-int counter
            raise errors.InappropriateRequest("counterstart must be an int", errorHandle=ProgrammerErrorHandle(
                "counterstart must be an int when instinating an EventStageHeartbeat object (or children of such)"))
        self.stages = []
        if stage is ... and stages is ...:
            # TODO add info for not passing a stage or stages
            ...
        if stage is not ... and stages is not ...:
            raise errors.InappropriateRequest("Cannot pass both a stage and stages", errorHandle=ProgrammerErrorHandle(
                "Please pass only a stages or a list of stages to an EventStageHeartbeat object constructor (or children thereof)"))
        if stage is ...:
            # TODO add info for not passing a stage
            ...
        else:
            self.stages.append(stage)
        if stages is ...:
            # TODO add info for not passing stages
            ...
        else:
            for stage in stages:
                self.stages.append(stage)

    def pump(self) -> None:
        self._step()

    def _step(self) -> None:
        self.counter += 1
        self.postdefault()
        [stage.release(channel=self.defaultChannels) for stage in self.stages]

    def _defaultEventConstructor(self):
        return HeartBeatEvent(count=self.counter,)

    def postdefault(self) -> None:
        [stage.post(event=self._defaultEventConstructor())
         for stage in self.stages]

    def _subscribeTo(self, *, stage: EventStage = ..., channel: str = ...) -> None:
        """Internal function to subscribe this heartbeat to an EventStage

        Args:
            stage (EventStage): Stage to subscribe to
        """
        if channel is ...:
            # TODO add info for calling _subscribeTo with no given channel
            channel = self.defaultChannel
        if stage is ...:
            # TODO add error for calling _subscribeTo without a given stage
            raise errors.InappropriateRequest(
                "stage not given to _subscribeTo")

        @stage.subscribe
        @loghelp.callbacknamed(channel)
        def _(event: Event = ...):
            self.__subscribeHandle(event)

    def setupStage(self, /, stage: EventStage = ...) -> None:
        """Setups up a stage to receive heartbeats from this object

        Args:
            stage (EventStage): Stage to setup (NOT a list of stages)
        """
        if stage is ...:
            # TODO add warning for calling setup without a stage
            raise errors.InappropriateRequest("stage not given to setupStage")
        self._subscribeTo(stage=stage, channel=self.defaultChannel)


class AutoEventStage(EventStage):
    """An EventStage that automatically posts its events (no manual post required)

    Args:
        nameHandle: str
        autosetup: bool
        heartbeat: EventStageHeartbeat
          Dependency injection only
    """
    heartbeat: EventStageHeartbeat = ...

    def setup(self, *, heartbeat: EventStageHeartbeat = ...) -> None:
        if heartbeat is ...:
            self.heartbeat = EventStageHeartbeat()
        if type(self.heartbeat) is not EventStageHeartbeat:
            # TODO add warning for non-EventStageHeartbeat heartbeat
            ...
        self.heartbeat.setupStage(stage=self)

        self.heartbeat.pump()

    def __init__(self, *, nameHandle: str = ..., autosetup: bool = ..., heartbeat: EventStageHeartbeat = ...) -> None:
        super().__init__(nameHandle=nameHandle)
        self.heartbeat = heartbeat
        if self.heartbeat is ...:
            self.heartbeat = EventStageHeartbeat(stage=self, countstart=0)
        if autosetup:
            self.setup(heartbeat=self.heartbeat)


def main():
    stage = AutoEventStage()

    @stage.subscribe
    @loghelp.callbacknamed("Smg88")
    def _(event: Event):
        print(
            f"EVENT {event=}, {event.channel=}, {event.name=}, {event.payload=}")
    stage.post(Event(channel="Smg", name="help!", payload="TESTING!"))
    stage.post(Event(channel="Smg88", name="LETS F**KING GO!", payload="gout!"))
    stage._post(all=True)


if __name__ == "__main__":
    main()
