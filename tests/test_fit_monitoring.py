from datetime import datetime, timedelta, date

from fit_galgo.galgo import FitGalgo
from fit_galgo.fit.models import Monitor, FileId, MonitoringInfo


def assert_monitoring_info(mi: MonitoringInfo) -> None:
    assert mi.timestamp is not None
    assert isinstance(mi.timestamp, datetime)


def assert_monitoring_data(path_file: str) -> None:
    galgo = FitGalgo(path_file)
    monitor: Monitor = galgo.parse()

    # Models
    assert isinstance(monitor, Monitor)
    assert hasattr(monitor, "file_id")
    assert isinstance(monitor.file_id, FileId)

    # Dates and datetimes
    assert monitor.datetime_utc is not None
    assert monitor.datetime_local is not None

    local_datetime: datetime = monitor.datetime_utc + timedelta(seconds=7200)
    local_date: date = date(
        year=local_datetime.year,
        month=local_datetime.month,
        day=local_datetime.day
    )
    assert monitor.monitoring_date == local_date
    assert (
        monitor.datetime_local.year == local_date.year and
        monitor.datetime_local.month == local_date.month and
        monitor.datetime_local.day == local_date.day
    )

    # Monitoring info
    assert_monitoring_info(monitor.monitoring_info)

    # Activities and resting metabolic rate and calories
    assert "walking" in monitor.activities
    assert "running" in monitor.activities
    assert type(monitor.metabolic_calories) is int
    assert type(monitor.active_calories) is int
    assert type(monitor.total_calories) is int
    assert monitor.metabolic_calories is not None
    assert monitor.active_calories is not None
    assert monitor.total_calories is not None

    # All data: steps, heart rate, respiration rate and stress levels.
    assert monitor.total_steps is not None
    assert type(monitor.total_steps) is int

    assert monitor.heart_rates is not None
    assert len(monitor.heart_rates) > 0

    assert monitor.activity_intensities is not None
    assert isinstance(monitor.activity_intensities, list)

    assert monitor.respiration_rates is not None
    assert isinstance(monitor.respiration_rates, list)
    assert len(monitor.respiration_rates) > 0

    assert monitor.stress_levels is not None
    assert isinstance(monitor.stress_levels, list)
    assert len(monitor.stress_levels) > 0


def assert_monitoring_data_with_zone_info(path_file: str) -> None:
    galgo = FitGalgo(path_file, "Europe/Madrid")
    monitor: Monitor = galgo.parse()

    assert (
        monitor.datetime_utc.hour != monitor.datetime_local.hour or
        monitor.datetime_utc.minute != monitor.datetime_local.minute or
        monitor.datetime_utc.second != monitor.datetime_local.second
    )


def assert_activity_intensities(path_file: str, moderate_min: int, vigorous_min: int) -> None:
    galgo = FitGalgo(path_file)
    monitor: Monitor = galgo.parse()

    assert sum([ai.moderate_minutes for ai in monitor.activity_intensities]) == moderate_min
    assert sum([ai.vigorous_minutes for ai in monitor.activity_intensities]) == vigorous_min


def test_monitoring_with_all():
    assert_monitoring_data("tests/files/monitor1_with_all.fit")
    assert_monitoring_data("tests/files/monitor2_with_all.fit")

    assert_monitoring_data_with_zone_info("tests/files/monitor1_with_all.fit")


def test_activity_intensities():
    assert_activity_intensities(
        "tests/files/monitor1_with_all.fit",
        moderate_min=0,
        vigorous_min=0
    )
    assert_activity_intensities(
        "tests/files/monitor_with_intensities.fit",
        moderate_min=26,
        vigorous_min=2
    )
