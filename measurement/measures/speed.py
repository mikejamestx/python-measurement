from measurement.base import BidimensionalMeasure


from measurement.measures.distance import Distance
from measurement.measures.time import Time


__all__ = [
    'Speed'
]


class Speed(BidimensionalMeasure):
    PRIMARY_DIMENSION = Distance
    REFERENCE_DIMENSION = Time

    ALIAS = {
        'mph': 'mi__hr',
        'kph': 'km__hr',
        'm/s': 'm__s',
        'kt': 'nmi__hr',
        'kts': 'nmi__hr',
        'Knots': 'nmi__hr',
        'mm/s': 'mm__s',
        'cm/s': 'cm__s',
        'ft/s': 'ft__s',

    }
    LABEL = {
        'nmi__hr': 'kt'
    }
