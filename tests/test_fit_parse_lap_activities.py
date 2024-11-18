import pytest
from datetime import datetime

from fit_galgo.galgo import FitGalgo
from fit_galgo.fit.definitions import (
    SWIMMING_SPORT,
    LAP_SWIMMING_SUB_SPORT
)
from fit_galgo.fit.models import (
    FitModel,
    FitError,
    FileId,
    Activity,
    DistanceActivity,
    LapActivity
)


def assert_parse_without_errors(path_file: str) -> LapActivity:
    galgo = FitGalgo(path_file)
    activity: DistanceActivity = galgo.parse()
    assert not isinstance(activity, FitError)
    assert isinstance(activity, FitModel)
    assert isinstance(activity, Activity)
    assert isinstance(activity, DistanceActivity)
    assert isinstance(activity, LapActivity)
    assert hasattr(activity, "file_id")
    assert isinstance(activity.file_id, FileId)
    return activity


def assert_sport(
        activity: LapActivity, expected_sport: str, expected_sub_sport: str
) -> None:
    assert activity.sport == expected_sport
    assert activity.sub_sport == expected_sub_sport


def assert_is_lap_activity_with_required_stats(activity: Activity) -> None:
    """It asserts is a distance activity and it has required stats.

    Required stats are:
    - name
    - sport
    - sub sport
    - time data
    - total distance
    - speed
    """
    assert isinstance(activity, DistanceActivity)
    assert isinstance(activity, LapActivity)

    assert activity.name is not None
    assert activity.sport is not None
    assert activity.sub_sport is not None

    assert activity.time is not None
    assert isinstance(activity.time.timestamp, datetime)
    assert isinstance(activity.time.start_time, datetime)
    assert isinstance(activity.time.elapsed, float)
    assert isinstance(activity.time.timer, float)

    assert activity.total_distance is not None
    assert activity.speed is not None
    assert isinstance(activity.speed.max, float)
    assert isinstance(activity.speed.avg, float)


def assert_there_are_laps_in_activity(activity: LapActivity, num_of_laps: int) -> None:
    assert activity.laps is not None
    assert len(activity.laps) == num_of_laps


def test_fit_parse_swimming_lap():
    activity = assert_parse_without_errors("tests/files/swimming_18_laps.fit")
    assert_sport(activity, SWIMMING_SPORT, LAP_SWIMMING_SUB_SPORT)
    assert_is_lap_activity_with_required_stats(activity)
    assert_there_are_laps_in_activity(activity, 18)
