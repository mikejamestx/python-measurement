import math
from measurement.base import MeasureBase
import warnings

__all__ = [
    'Pressure',
]

def dbar_to_meters_of_seawater(p, latitude):
    x = math.sin(latitude / 57.29578)**2
    g = 9.780318 * ( 1.0 + ( 5.2788e-3  + 2.36e-5  * x) * x) + 1.092e-6  * p
    d = ((((-1.82e-15  * p + 2.279e-10 ) * p - 2.2512e-5 ) * p + 9.72659) * p) / g
    return d

def meters_of_seawater_to_dbar(d, latitude):
    raise NotImplementedError()

class ApproximatedDepthError(Exception):
    """
    Exception that is raised when converting pressure to meters of seawater
    without providing a latitude.
    """

class Pressure(MeasureBase):
    """
    Pressure with optional latitude and conversion to meters of seawater
    based on Unesco Technical Papers in Marine Science #44 (pg 25-28)
    """
    STANDARD_UNIT = "Pa"
    UNITS = {
        'Pa': 1.0,
        'bar': 1e5,
        'mbar': 1e2,
        'dbar': 1e4,
        'at': 98066.5,
        'atm': 101325,
        'torr': 133.322,
        'psi': 6894.757293168,
        'inhg': 2.95299830714e4,
        'm_seawater': None,
    }

    ALIAS = {
        'pascal': 'Pa',
        'bar': 'bar',
        'technical atmosphere': 'at',
        'atmosphere': 'atm',
        'torr': 'torr',
        'pounds per square inch': 'psi' ,
        'inches of Mercury': 'inhg',
        'm': 'dbar',
        'Decibar': 'dbar',
        'Decibars': 'dbar',
        'Millibar': 'mbar',
        'Millibars': 'mbar',
        'Meters of Seawater': 'dbar',
    }
    LABEL = {
        'm_seawater': 'm',
    }
    SI_UNITS = ['Pa']

    def __init__(self, *args, **kwargs):
        self.latitude = kwargs.pop('latitude', None)
        super(Pressure, self).__init__(*args, **kwargs)

    def default_units(self, kwargs):
        """
        Do not accept m_seawater as an input unit.
        """
        if 'm_seawater' in kwargs:
            raise AttributeError('Cannot accept m_seawater as input unit')
        return super(Pressure, self).default_units(kwargs)

    def __getattr__(self, name):
        if name == "m_seawater":
            return self.to_meters_of_seawater()
        return super(Pressure, self).__getattr__(name)

    def __format__(self, fmt):
        try:
            val = super(Pressure, self).__format__(fmt)
        except ApproximatedDepthError as e:
            if self.dbar > 5:
                raise
            try:
                prec = int("".join(x for x in fmt.split(".")[1] if x.isdigit()))
                if prec > 2:
                    raise
            except IndexError:
                pass
            _unit = self.unit
            self.unit = 'dbar'
            if len(fmt) != 0:
                val = super(Pressure, self).__format__(fmt)
            else:
                val = str(self)
            self.unit = _unit
            val = val.replace('dbar', self.unit_label)
        return val

    def to_meters_of_seawater(self):
        """
        Convert pressure to seawater depth in meters.
        Raise ApproximatedDepthError if latitude isn't known.
        """
        try:
            if self.latitude is None:
                raise ValueError
            p = self.dbar
            return dbar_to_meters_of_seawater(p, self.latitude)
        except (AttributeError, ValueError) as e:
            msg = "Pressure converted to meters of seawater without latitude."
            raise ApproximatedDepthError(msg)



