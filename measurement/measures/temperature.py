#!/usr/bin/env python
# -*- coding: utf-8 -*-

from measurement.base import MeasureBase, SimpleTransform


__all__ = [
    'Temperature'
]


class Temperature(MeasureBase):
    STANDARD_UNIT = 'k'
    UNITS = {
        'c': SimpleTransform(
            to_fcn=lambda c: c + 273.15,
            from_fcn=lambda k: k - 273.15
        ),
        'f': SimpleTransform(
            to_fcn=lambda f: (f - 32) * 5.0 / 9 + 273.15,
            from_fcn=lambda k: (k - 273.15) * 9.0 / 5 + 32
        ),
        'k': 1.0,
    }
    ALIAS = {
        'celsius': 'c',
        'fahrenheit': 'f',
        'kelvin': 'k',
    }
    LABEL = {
        'c': u"°C",
        'f': u"°F",
        'k': u'K',
    }

    @staticmethod
    def average(items, default_unit='c'):
        """
        Since temperature unit scales other than Kelvin have arbitrary zero
        points, we must force the sum to be in Kelvin
        """
        avg = sum(items, Temperature(k=0)) / len(items)
        avg.unit = default_unit
        return avg
