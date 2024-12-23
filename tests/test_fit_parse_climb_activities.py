from datetime import datetime

from fit_galgo.galgo import FitGalgo
from fit_galgo.fit.definitions import (
    ROCK_CLIMBING_SPORT,
    BOULDERING_SUB_SPORT,
    ClimbResult
)
from fit_galgo.fit.models import (
    FitModel,
    FitError,
    FileId,
    Activity,
    ClimbActivity,
    Climb
)


def assert_parse_without_errors(path_file: str) -> ClimbActivity:
    galgo = FitGalgo(path_file)
    activity: ClimbActivity = galgo.parse()
    assert not isinstance(activity, FitError)
    assert isinstance(activity, FitModel)
    assert isinstance(activity, Activity)
    assert isinstance(activity, ClimbActivity)
    assert hasattr(activity, "file_id")
    assert isinstance(activity.file_id, FileId)
    return activity


def assert_sport(
        activity: ClimbActivity, expected_sport: str, expected_sub_sport: str
) -> None:
    assert activity.sport == expected_sport
    assert activity.sub_sport == expected_sub_sport


def assert_is_climb_activity_with_minimal_required_stats(
        activity: ClimbActivity
) -> None:
    """It asserts is a climb activity and it has required stats.

    Required stats are:
    - name
    - sport
    - sub sport
    - time data
    """
    assert isinstance(activity, ClimbActivity)

    assert activity.name is not None
    assert activity.sport is not None
    assert activity.sub_sport is not None

    assert activity.time is not None
    assert isinstance(activity.time.timestamp, datetime)
    assert isinstance(activity.time.start_time, datetime)
    assert isinstance(activity.time.elapsed, float)
    assert isinstance(activity.time.timer, float)
    assert isinstance(activity.time.work, float)
    assert activity.time.work < activity.time.elapsed


def assert_climbs_data(climbs: list[Climb]) -> None:
    assert climbs is not None
    assert len(climbs) > 0
    for climb in climbs:
        assert climb.time is not None
        assert isinstance(climb.time.timestamp, datetime)
        assert isinstance(climb.time.start_time, datetime)
        assert isinstance(climb.time.elapsed, float)
        assert isinstance(climb.time.timer, float)
        assert isinstance(climb.time.work, float)
        assert climb.split_type is not None


def test_fit_parse_bouldering():
    activity = assert_parse_without_errors("tests/files/bouldering.fit")
    assert_sport(activity, ROCK_CLIMBING_SPORT, BOULDERING_SUB_SPORT)
    assert_is_climb_activity_with_minimal_required_stats(activity)
    assert_climbs_data(activity.climbs)


def test_fit_parse_bouldering_with_18_climbs():
    activity = assert_parse_without_errors("tests/files/bouldering_18_climbs.fit")
    assert_sport(activity, ROCK_CLIMBING_SPORT, BOULDERING_SUB_SPORT)
    assert_is_climb_activity_with_minimal_required_stats(activity)
    assert_climbs_data(activity.climbs)

    assert len([
        c for c in activity.climbs if c.result in [ClimbResult.COMPLETED, ClimbResult.ATTEMPTED]
    ]) == 18
