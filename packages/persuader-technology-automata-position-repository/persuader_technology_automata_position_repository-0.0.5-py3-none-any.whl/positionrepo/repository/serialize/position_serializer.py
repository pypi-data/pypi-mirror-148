from core.position.Position import Position


def serialize(position: Position) -> dict:
    serialized = {
        'instrument': position.instrument,
        'quantity': str(position.quantity),
        'instant': position.instant
    }
    return serialized
