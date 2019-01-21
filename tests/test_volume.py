from .base import MeasurementTestBase


from measurement.measures import Volume


class VolumeTest(MeasurementTestBase):
    def test_sub_one_base_si_measure(self):
        milliliters = Volume(ml=200)
        fl_oz = Volume(us_oz=6.76280454)

        self.assertAlmostEqual(
            milliliters.standard,
            fl_oz.standard
        )

    def test_multiply_divide(self):
        vol = Volume(ML=100)
        result = vol * 2
        self.assertEqual(result.ml, 200)
        result *= 2
        self.assertEqual(result.ml, 400)
        with self.assertRaises(TypeError):
            vol * vol
        with self.assertRaises(TypeError):
            vol *= vol
        with self.assertRaises(TypeError):
            vol /= vol

        result /= 4
        self.assertEqual(result.ml, 100)
        result = result / 2
        self.assertEqual(result.ml, 50)
        result = vol / vol
        self.assertEqual(result, 1)


