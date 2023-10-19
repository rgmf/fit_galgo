from datetime import datetime

from fit_galgo.galgo import FitGalgo
from fit_galgo.fit.results import FitHrv


def assert_is_an_hrv(path_file: str) -> None:
    galgo = FitGalgo(path_file)
    hrv = galgo.parse()

    assert isinstance(hrv, FitHrv)
    assert isinstance(hrv.datetime_utc, datetime)
    assert isinstance(hrv.weekly_average, float)
    assert isinstance(hrv.last_night_average, float)
    assert isinstance(hrv.last_night_5_min_high, float)
    assert isinstance(hrv.baseline_low_upper, float)
    assert isinstance(hrv.baseline_balanced_lower, float)
    assert isinstance(hrv.baseline_balanced_upper, float)
    assert isinstance(hrv.status, str)
    assert len(hrv.values) > 0
    for v in hrv.values:
        assert isinstance(v.timestamp, datetime)
        assert v.value is None or isinstance(v.value, int)


def test_hrv():
    assert_is_an_hrv("tests/files/hrv1.fit")
    assert_is_an_hrv("tests/files/hrv2.fit")
