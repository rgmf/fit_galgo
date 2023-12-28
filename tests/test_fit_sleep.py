from datetime import datetime, timedelta

from fit_galgo.galgo import FitGalgo
from fit_galgo.fit.models import Sleep, SleepLevel


def sleep(path_file: str) -> None:
    galgo = FitGalgo(path_file)
    sleep: Sleep = galgo.parse()

    assert isinstance(sleep, Sleep)
    assert len(sleep.dates) == 2
    dt1: datetime = datetime.fromisoformat(sleep.dates[0])
    dt2: datetime = datetime.fromisoformat(sleep.dates[1])
    assert isinstance(dt2, datetime)
    assert isinstance(dt1, datetime)
    assert timedelta(days=0) <= (dt2 - dt1) <= timedelta(days=1)
    assert isinstance(sleep.combined_awake_score, int)
    assert isinstance(sleep.awake_time_score, int)
    assert isinstance(sleep.awakenings_count_score, int)
    assert isinstance(sleep.deep_sleep_score, int)
    assert isinstance(sleep.sleep_duration_score, int)
    assert isinstance(sleep.light_sleep_score, int)
    assert isinstance(sleep.overall_sleep_score, int)
    assert isinstance(sleep.sleep_quality_score, int)
    assert isinstance(sleep.sleep_recovery_score, int)
    assert isinstance(sleep.rem_sleep_score, int)
    assert isinstance(sleep.sleep_restlessness_score, int)
    assert isinstance(sleep.awakenings_count, int)
    assert isinstance(sleep.interruptions_score, int)
    assert isinstance(sleep.average_stress_during_sleep, float)
    assert len(sleep.levels) > 0
    for level in sleep.levels:
        assert isinstance(level, SleepLevel)
        assert isinstance(level.datetime_utc, datetime)
        assert isinstance(level.level, str)


def test_sleep():
    sleep("tests/files/sleep1.fit")
    sleep("tests/files/sleep2.fit")
