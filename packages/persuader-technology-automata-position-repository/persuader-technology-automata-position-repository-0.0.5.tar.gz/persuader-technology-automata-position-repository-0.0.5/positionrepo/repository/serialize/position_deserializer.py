from core.number.BigFloat import BigFloat
from core.position.Position import Position
from utility.json_utility import as_data


def deserialize(position) -> Position:
    instrument = as_data(position, 'instrument')
    quantity = BigFloat(as_data(position, 'quantity'))
    instant = as_data(position, 'instant')
    deserialized_position = Position(instrument, quantity, instant)
    return deserialized_position
