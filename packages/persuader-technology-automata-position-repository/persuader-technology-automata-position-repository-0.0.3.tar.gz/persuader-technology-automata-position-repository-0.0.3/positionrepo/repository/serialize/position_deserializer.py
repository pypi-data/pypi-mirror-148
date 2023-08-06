from core.number.BigFloat import BigFloat
from utility.json_utility import as_data

from positionrepo.Position import Position


def deserialize(position) -> Position:
    instrument = as_data(position, 'instrument')
    quantity = BigFloat(as_data(position, 'quantity'))
    deserialized_position = Position(instrument, quantity)
    return deserialized_position
