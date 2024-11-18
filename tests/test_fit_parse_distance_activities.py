import pytest
from datetime import datetime

from fit_galgo.galgo import FitGalgo
from fit_galgo.fit.definitions import (
    RUNNING_SPORT,
    WALKING_SPORT,
    HIKING_SPORT,
    CYCLING_SPORT,
    GENERIC_SUB_SPORT,
    TRAIL_SUB_SPORT,
    ROAD_SUB_SPORT,
    MOUNTAIN_SUB_SPORT
)
from fit_galgo.fit.models import (
    FitModel,
    FitError,
    FileId,
    Activity,
    DistanceActivity
)


def assert_parse_without_errors(path_file: str) -> DistanceActivity:
    galgo = FitGalgo(path_file)
    activity: DistanceActivity = galgo.parse()
    assert not isinstance(activity, FitError)
    assert isinstance(activity, FitModel)
    assert isinstance(activity, Activity)
    assert isinstance(activity, DistanceActivity)
    assert hasattr(activity, "file_id")
    assert isinstance(activity.file_id, FileId)
    return activity


def assert_sport(
        activity: DistanceActivity, expected_sport: str, expected_sub_sport: str
) -> None:
    assert activity.sport == expected_sport
    assert activity.sub_sport == expected_sub_sport


def assert_is_distance_activity_with_required_stats(activity: Activity) -> None:
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


def assert_there_are_laps_in_activity(activity: DistanceActivity, num_of_laps: int) -> None:
    assert activity.laps is not None
    assert len(activity.laps) == num_of_laps


def test_fit_parse_walking():
    activity = assert_parse_without_errors("tests/files/walking.fit")
    assert_sport(activity, WALKING_SPORT, GENERIC_SUB_SPORT)
    assert_is_distance_activity_with_required_stats(activity)


def test_fit_parse_hiking():
    activity = assert_parse_without_errors("tests/files/hiking.fit")
    assert_sport(activity, HIKING_SPORT, GENERIC_SUB_SPORT)
    assert_is_distance_activity_with_required_stats(activity)


def test_fit_parse_running():
    activity = assert_parse_without_errors("tests/files/running.fit")
    assert_sport(activity, RUNNING_SPORT, GENERIC_SUB_SPORT)
    assert_is_distance_activity_with_required_stats(activity)


def test_fit_parse_trail_running():
    activity = assert_parse_without_errors("tests/files/trail_running.fit")
    assert_sport(activity, RUNNING_SPORT, TRAIL_SUB_SPORT)
    assert_is_distance_activity_with_required_stats(activity)


def test_fit_parse_road_cycling():
    activity = assert_parse_without_errors("tests/files/road_cycling.fit")
    assert_sport(activity, CYCLING_SPORT, ROAD_SUB_SPORT)
    assert_is_distance_activity_with_required_stats(activity)


@pytest.mark.skip(reason="The activity is not a mountain biking one")
def test_fit_parse_mountain_cycling():
    activity = assert_parse_without_errors("tests/files/mountain_biking.fit")
    assert_sport(activity, CYCLING_SPORT, MOUNTAIN_SUB_SPORT)
    assert_is_distance_activity_with_required_stats(activity)
