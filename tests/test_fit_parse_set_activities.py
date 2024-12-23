from datetime import datetime

from fit_galgo.galgo import FitGalgo
from fit_galgo.fit.definitions import (
    TRAINING_SPORT,
    STRENGTH_TRAINING_SUB_SPORT
)
from fit_galgo.fit.models import (
    FileId, Activity, SetActivity, Set, FitModel, FitError
)


def assert_parse_without_errors(path_file: str) -> SetActivity:
    galgo = FitGalgo(path_file)
    activity: SetActivity = galgo.parse()
    assert not isinstance(activity, FitError)
    assert isinstance(activity, FitModel)
    assert isinstance(activity, Activity)
    assert isinstance(activity, SetActivity)
    assert hasattr(activity, "file_id")
    assert isinstance(activity.file_id, FileId)
    return activity


def assert_sport(
        activity: SetActivity, expected_sport: str, expected_sub_sport: str
) -> None:
    assert activity.sport == expected_sport
    assert activity.sub_sport == expected_sub_sport


def assert_is_set_activity_with_minimal_required_stats(activity: Activity) -> None:
    """It asserts is a set activity and it has required stats.

    Required stats are:
    - name
    - sport
    - sub sport
    - time data
    """
    assert isinstance(activity, SetActivity)

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


def assert_required_set_data(s: Set) -> None:
    assert s.order is not None and isinstance(s.order, int)
    assert s.exercise is not None and isinstance(s.exercise, str)
    assert s.time is not None
    assert isinstance(s.time.timestamp, datetime)
    assert isinstance(s.time.start_time, datetime)
    assert isinstance(s.time.elapsed, float)
    assert isinstance(s.time.timer, float)
    assert isinstance(s.time.work, float)


def assert_sets_data(sets: list[Set]) -> None:
    assert sets is not None
    assert len(sets) > 0

    for set_ in sets:
        assert_required_set_data(set_)


def test_fit_parse_training():
    activity = assert_parse_without_errors("tests/files/training_strength.fit")
    assert_sport(activity, TRAINING_SPORT, STRENGTH_TRAINING_SUB_SPORT)
    assert_is_set_activity_with_minimal_required_stats(activity)
    assert_sets_data(activity.sets)


def test_fit_parse_training_with_20_sets():
    activity = assert_parse_without_errors(
        "tests/files/training_4pull_up_3push_up_3curl_3bench_press_1deadlift_1sit_up_5unknown.fit"
    )
    assert_sport(activity, TRAINING_SPORT, STRENGTH_TRAINING_SUB_SPORT)
    assert_is_set_activity_with_minimal_required_stats(activity)
    assert_sets_data(activity.sets)

    rest = 20
    work = 20
    assert len([c for c in activity.sets]) == rest + work
    assert len(
        [c for c in activity.sets if not c.is_active_set()]
    ) == 20
    assert len(
        [c for c in activity.sets if c.is_active_set()]
    ) == 20
