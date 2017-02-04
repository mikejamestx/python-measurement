from itertools import product as iproduct
from .base import MeasurementTestBase

from measurement.measures import Pressure


class PressureTest(MeasurementTestBase):
    def test_kpa_to_dbar(self):
        kpa = Pressure(kPa=100000)
        expected_dbar = 10000

        self.assertEqual(kpa.dbar, expected_dbar)

    def test_dbar_to_kpa(self):
        dbar = Pressure(dbar=10000)
        expected_kpa = 100000

        self.assertEqual(dbar.kPa, expected_kpa)

    def test_bar_to_pa(self):
        bar = Pressure(bar=1000)
        expected_pa = 100000000

        self.assertAlmostEqual(
            bar.Pa,
            expected_pa
        )

    def test_conversion_to_mbar(self):
        hpa = Pressure(hPa=1000.5)
        expected_mbar = 1000.5

        self.assertAlmostEqual(
            hpa.mbar, expected_mbar
        )

    def test_conversion_to_non_si(self):
        dbar = Pressure(dbar=10000)
        expected_psi = 14503.7737796859

        self.assertAlmostEqual(
            dbar.psi,
            expected_psi,
            3
        )

    def test_conversion_to_meters_of_seawater(self):
        dbars = [5e2, 1e3, 2e3, 3e3, 4e3, 5e3, 6e3, 7e3, 8e3, 9e3, 10e3]
        lats = [0, 30, 45, 60, 90]
        expected = [
            496.65, 496.00, 495.34, 494.69, 494.03,
            992.12, 990.81, 989.50, 988.19, 986.88,
            1979.55, 1976.94, 1974.33, 1971.72, 1969.11,
            2962.43, 2958.52, 2954.61, 2950.71, 2946.81,
            3940.88, 3935.68, 3930.49, 3925.30, 3920.10,
            4915.04, 4908.56, 4902.08, 4895.60, 4889.13,
            5885.03, 5877.27, 5869.51, 5861.76, 5854.01,
            6850.95, 6841.92, 6832.89, 6823.86, 6814.84,
            7812.93, 7802.63, 7792.33, 7782.04, 7771.76,
            8771.07, 8759.51, 8747.95, 8736.40, 8724.85,
            9725.47, 9712.65, 9699.84, 9687.03, 9674.23,
        ]
        for inputs, output in zip(iproduct(dbars, lats), expected):
            p = Pressure(dbar=inputs[0], latitude=inputs[1])
            self.assertAlmostEqual(
                p.to_meters_of_seawater(),
                output,
                2
            )

    def test_depth_conversion_no_latitude(self):
#         dbars = [5e2, 1e3, 2e3, 3e3, 4e3, 5e3, 6e3, 7e3, 8e3, 9e3, 10e3]
        dbars = range(0,10001,1)
        lats = [x*0.5 for x in range(0,181)]# [0, 30, 45, 60, 90]
        expected = [
            496.65, 496.00, 495.34, 494.69, 494.03,
            992.12, 990.81, 989.50, 988.19, 986.88,
            1979.55, 1976.94, 1974.33, 1971.72, 1969.11,
            2962.43, 2958.52, 2954.61, 2950.71, 2946.81,
            3940.88, 3935.68, 3930.49, 3925.30, 3920.10,
            4915.04, 4908.56, 4902.08, 4895.60, 4889.13,
            5885.03, 5877.27, 5869.51, 5861.76, 5854.01,
            6850.95, 6841.92, 6832.89, 6823.86, 6814.84,
            7812.93, 7802.63, 7792.33, 7782.04, 7771.76,
            8771.07, 8759.51, 8747.95, 8736.40, 8724.85,
            9725.47, 9712.65, 9699.84, 9687.03, 9674.23,
        ]
        for inputs in iproduct(dbars, lats):
            p = Pressure(dbar=inputs[0], latitude=inputs[1])
            val = p.to_meters_of_seawater()
            dif = val - inputs[0]
            print("{:5.1f}\t{:6.1f}\t{:8.2f}\t{:4.1f}".format(*inputs, val, dif))
#             self.assertAlmostEqual(
#                 p.to_meters_of_seawater(),
#                 output,
#                 2
#             )

