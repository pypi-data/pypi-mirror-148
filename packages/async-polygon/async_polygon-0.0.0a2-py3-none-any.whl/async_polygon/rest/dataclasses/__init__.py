from .templates import AggregateBars
from .templates import LastTrade
from .templates import LastTradeCryptoPair
from .templates import PreviousClose
from . import pretty_json

import typing

from .templates import Template


AnyDefinition = typing.TypeVar("AnyDefinition", bound=Template)


name_to_method: typing.Dict[str, typing.Callable[[], typing.Type[AnyDefinition]]] = {
    'LastTrade':LastTrade,
    'AggregateBars':AggregateBars,
    'PreviousClose':PreviousClose,
}