from datetime import datetime

from fit_galgo.galgo import FitGalgo
from fit_galgo.fit.models import (
    FileId,
    MultisportActivity,
    DistanceActivity,
    TransitionActivity,
    FitModel,
    FitError
)
from fit_galgo.fit.definitions import (
    RUNNING_SPORT,
    CYCLING_SPORT,
    TRANSITION_SPORT,
    GENERIC_SUB_SPORT,
    ROAD_SUB_SPORT
)
from .test_fit_parse_distance_activities import (
    assert_is_distance_activity_with_required_stats
)


def assert_parse_without_errors(path_file: str) -> MultisportActivity:
    galgo = FitGalgo(path_file)
    activity: MultisportActivity = galgo.parse()
    assert not isinstance(activity, FitError)
    assert isinstance(activity, FitModel)
    assert isinstance(activity, MultisportActivity)
    assert hasattr(activity, "file_id")
    assert isinstance(activity.file_id, FileId)
    return activity


def assert_is_transition_activity_with_required_stats(
        activity: TransitionActivity
) -> None:
    """It asserts is a transition activity and it has required stats.

    Required stats are:
    - name
    - sport
    - sub sport
    - time data
    """
    assert isinstance(activity, TransitionActivity)

    assert activity.name is not None
    assert activity.sport is not None
    assert activity.sub_sport is not None

    assert activity.time is not None
    assert isinstance(activity.time.timestamp, datetime)
    assert isinstance(activity.time.start_time, datetime)
    assert isinstance(activity.time.elapsed, float)
    assert isinstance(activity.time.timer, float)
    assert isinstance(activity.time.work, float)


def assert_duathlon(activity: MultisportActivity, sports: list[tuple]) -> None:
    assert isinstance(activity, MultisportActivity)
    assert len(activity.activities) == 5
    assert isinstance(activity.activities[0], DistanceActivity)
    assert isinstance(activity.activities[1], TransitionActivity)
    assert isinstance(activity.activities[2], DistanceActivity)
    assert isinstance(activity.activities[3], TransitionActivity)
    assert isinstance(activity.activities[4], DistanceActivity)

    for a, st in zip(activity.activities, sports):
        assert a.sport == st[0]
        assert a.sub_sport == st[1]
        if isinstance(a, TransitionActivity):
            assert_is_transition_activity_with_required_stats(a)
        else:
            assert_is_distance_activity_with_required_stats(a)


def test_fit_parse_multisport_duathlon():
    activity = assert_parse_without_errors("tests/files/duathlon.fit")
    assert_duathlon(
        activity,
        [
            (RUNNING_SPORT, GENERIC_SUB_SPORT),
            (TRANSITION_SPORT, GENERIC_SUB_SPORT),
            (CYCLING_SPORT, ROAD_SUB_SPORT),
            (TRANSITION_SPORT, GENERIC_SUB_SPORT),
            (RUNNING_SPORT, GENERIC_SUB_SPORT)
        ]
    )
