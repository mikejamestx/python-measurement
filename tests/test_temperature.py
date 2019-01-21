from .base import MeasurementTestBase
from measurement.base import pretty_name

try:
    import numpy as np
except:
    np = None

from measurement.measures import Temperature


class TemperatureTest(MeasurementTestBase):
    def setUp(self):
        if np:
            self.c_array = np.array([0, 100])
            self.f_array = np.array([32, 212])
            self.c_marray = np.ma.array(self.c_array)
            self.c_marray[self.c_marray==100] = np.ma.masked
            self.f_marray = np.ma.array(self.f_array)
            self.f_marray[self.f_marray==212] = np.ma.masked

    def test_sanity(self):
        fahrenheit = Temperature(fahrenheit=70)
        celsius = Temperature(celsius=21.1111111)

        self.assertAlmostEqual(
            fahrenheit.k,
            celsius.k
        )

    def test_conversion_to_non_si(self):
        celsius = Temperature(celsius=21.1111111)
        expected_farenheit = 70

        self.assertAlmostEqual(
            celsius.f,
            expected_farenheit
        )

    def test_average(self):
        t1 = Temperature(c=100)
        t2 = Temperature(c=300)
        expected_average = (t1.c + t2.c) / 2
        t_avg = Temperature.average([t1, t2])
        self.assertAlmostEqual(t_avg.c, expected_average)

    def test_addition_typeerrors(self):
        t1 = Temperature(c=100)
        values = [1, 1.5, 0, -1]
        for value in values:
            with self.subTest(value=value, value_type=pretty_name(value)):
                self.assertRaises(TypeError, sum, t1, value)

    def test_ensure_that_we_always_output_float(self):
        kelvin = Temperature(kelvin=10)

        celsius = kelvin.c

        self.assertTrue(
            isinstance(celsius, float)
        )

    def test_attributes(self):
        t = Temperature(c=100)
        expected_c = 100
        expected_f = 212
        expected_k = 373.15
        units = ['celsius', 'f', 'k']
        expected_values = [100, 212, 373.15]
        for u, expected_value in zip(units, expected_values):
            with self.subTest(output_unit=u, expected_value=expected_value):
                t.unit = u
                self.assertEqual(t.value, expected_value)
        u_out = 'c'
        u_in = 'f'
        v_in = 32
        v_out = 0
        kw = dict(unit_in='f', unit_out='c', value_in=32, expected_output=0)
        with self.subTest("value setter", **kw):
            t.unit = kw['unit_in']
            t.value = kw['value_in']
            t.unit = kw['unit_out']
            self.assertEqual(t.value, kw['expected_output'])

    def test_comparison(self):
        c0 = Temperature(c=0)
        c100 = Temperature(c=100)
        f0 = Temperature(f=32)
        f100 = Temperature(f=212)

        self.assertEqual(c0, f0)
        self.assertEqual(c100, f100)
        self.assertTrue(c0 < c100)
        self.assertFalse(c0 > c100)
        self.assertTrue(c0 < f100)
        self.assertFalse(c0 > f100)

    if np:
        def test_arrays(self):
            tc_array = Temperature(celsius=self.c_array)
            tc_marray = Temperature(celsius=self.c_marray)
            tf_array = Temperature(f=self.f_array)
            tf_marray = Temperature(f=self.f_marray)
            with self.subTest('array as C'):
                for c_as_c, f_as_c in zip(tc_array.c, tf_array.c):
                    self.assertAlmostEqual(c_as_c, f_as_c, 6)

            with self.subTest('array as F'):
                for c_as_f, f_as_f in zip(tc_array.f, tf_array.f):
                    self.assertAlmostEqual(c_as_f, f_as_f, 6)
