# -*- coding: utf-8 -*-
from .base import MeasurementTestBase

from measurement.base import pretty_name
from measurement.measures import Distance, Area


class DistanceTest(MeasurementTestBase):
    def test_conversion_equivalence(self):
        miles = Distance(mi=1)
        kilometers = Distance(km=1.609344)

        self.assertAlmostEqual(
            miles.km,
            kilometers.km
        )

    def test_attrib_conversion(self):
        kilometers = Distance(km=1)
        expected_meters = 1000

        self.assertAlmostEqual(
            kilometers.m,
            expected_meters
        )

        with self.assertRaises(AttributeError):
            val = kilometers.invalid_unit

    def test_identity_conversion(self):
        expected_miles = 10
        miles = Distance(mi=expected_miles)

        self.assertAlmostEqual(
            miles.mi,
            expected_miles
        )

    def test_auto_si_kwargs(self):
        meters = Distance(meter=1e6)
        megameters = Distance(megameter=1)

        self.assertEqual(
            meters,
            megameters,
        )

    def test_auto_si_attrs(self):
        one_meter = Distance(m=1)

        micrometers = one_meter.um

        self.assertEqual(
            one_meter.value * 10**6,
            micrometers
        )

    def test_area_sq_km(self):
        one_sq_km = Area(sq_km=10)
        miles_sqd = Area(sq_mi=3.8610216)

        self.assertAlmostEqual(
            one_sq_km.standard,
            miles_sqd.standard,
            places=1
        )

    def test_set_value(self):
        distance = Distance(mi=10)

        expected_standard = 16093.44
        self.assertEqual(
            distance.standard,
            expected_standard,
        )

        distance.value = 11

        expected_standard = 17702.784
        self.assertEqual(
            distance.standard,
            expected_standard
        )

    def test_multiply(self):
        m1 = 100
        m2 = 200
        d1 = Distance(m=m1)
        values = [150.5, Distance(m=m2)]
        expected_results = [150.5 * m1, m1 * m2]
        for value, expected_result in zip(values, expected_results):
            with self.subTest(value=value, type=pretty_name(value)):
                result = d1 * value
                if isinstance(value, Distance):
                    self.assertIsInstance(result, Area)
                    result = result.sq_m
                else:
                    result = result.m
                self.assertAlmostEqual(result, expected_result, 6)

        with self.subTest(value=value, type=pretty_name(value)):
            mult = lambda x: x[0] * x[1]
            self.assertRaises(TypeError, mult, (d1, "can't multiply"))


    def test_area_divide(self):
        area = Area(sq_m=300)
        value = 2
        expected_result = 150
        with self.subTest(value=value, type=pretty_name(value)):
            result = area / value
            self.assertIsInstance(result, Area)
            self.assertEqual(result.sq_m, expected_result)

        value = Area(sq_m=2)
        with self.subTest(value=value, type=pretty_name(value)):
            self.assertRaises(TypeError, area.__div__, value)

    def test_lowercase_alias(self):
        d = Distance(**{'nautical mile': 1})
        self.assertEqual(d.unit, 'nmi')
        self.assertEqual(d.m, 1852)

    def test_units_assignment(self):
        meters = 100
        d = Distance(m=meters)
        u_in = ['mm', 'nautical mile']
        u_out = ['mm', 'nmi']
        invalid_unit = 'invalid unit'
        values = [meters * 1000, meters / 1852]
        for unit, expected_unit, expected_value in zip(u_in, u_out, values):
            with self.subTest(unit=unit):
                d.unit = unit
                self.assertEqual(d.unit, expected_unit)
                self.assertEqual(d.value, expected_value)
                self.assertEqual(d.unit_attname(unit), expected_unit)


        with self.subTest(unit=invalid_unit):
            with self.assertRaises(ValueError):
                d.unit = invalid_unit
            self.assertRaises(Exception, d.unit_attname, invalid_unit)


    def test_string_formatting(self):
        d = Distance(m=100)
        self.assertEqual("100.00 m", "{:.2f %u}".format(d))
        self.assertEqual("100.0 m", "{}".format(d))
        self.assertEqual("Distance(m=100.0)", repr(d))

    def test_addition_subtraction(self):
        d = Distance(m=100) + Distance(m=200)
        self.assertEqual(d.m, 300)
        d += Distance(m=300)
        self.assertEqual(d.m, 600)
        with self.assertRaises(TypeError):
            d + 10
        d -= Distance(m=150)
        self.assertEqual(d.m, 450)
        d = d - Distance(m=50)
        self.assertEqual(d.m, 400)
        with self.assertRaises(TypeError):
            d - 10



