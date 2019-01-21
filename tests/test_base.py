from .base import MeasurementTestBase
from measurement.utils import guess


class BaseMeasurementTest(MeasurementTestBase):
    def test_invalid_guess(self):
        self.assertRaises(ValueError, guess, 100, 'not a unit')
