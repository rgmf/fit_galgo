from datetime import datetime

from pydantic import BaseModel, Field, validator

from fit_galgo.utils.date_utils import try_to_compute_local_datetime


class FileIdModel(BaseModel):
    file_type: str | int = Field(alias="type")
    serial_number: int | None = None
    time_created: datetime | None = None
    manufacturer: str | None = None
    product: int | None = None
    garmin_product: str | None = None


class SessionModel(BaseModel):
    message_index: int
    timestamp: datetime
    start_time: datetime
    total_elapsed_time: float
    total_timer_time: float
    sport: str
    sub_sport: str

    start_position_lat: int | None = None
    start_position_long: int | None = None
    end_position_lat: int | None = None
    end_position_long: int | None = None

    first_lap_index: int | None = None
    num_laps: int | None = None

    sport_profile_name: str | None = None
    sport_index: int | None = None

    total_distance: float | None = None
    total_cycles: int | None = None
    total_strides: int | None = None
    enhanced_avg_speed: float | None = None
    avg_speed: float | None = None
    enhanced_max_speed: float | None = None
    max_speed: float | None = None
    avg_heart_rate: float | None = None
    max_heart_rate: float | None = None
    avg_cadence: float | None = None
    avg_running_cadence: float | None = None
    max_cadence: float | None = None
    max_running_cadence: float | None = None
    total_calories: float | None = None
    total_ascent: float | None = None
    total_descent: float | None = None
    avg_temperature: float | None = None
    max_temperature: float | None = None
    min_temperature: float | None = None
    enhanced_avg_respiration_rate: float | None = None
    enhanced_max_respiration_rate: float | None = None
    enhanced_min_respiration_rate: float | None = None

    training_load_peak: float | None = None
    total_training_effect: float | None = None
    total_anaerobic_training_effect: float | None = None

    avg_fractional_cadence: float | None = None
    max_fractional_cadence: float | None = None
    total_fractional_ascent: float | None = None
    total_fractional_descent: float | None = None


class RecordModel(BaseModel):
    timestamp: datetime
    position_lat: int | None = None
    position_long: int | None = None
    altitude: float | None = None
    enhanced_altitude: float | None = None
    heart_rate: int | None = None
    cadence: int | None = None
    distance: float | None = None
    enhanced_distance: float | None = None
    speed: float | None = None
    enhanced_speed: float | None = None
    power: int | None = None
    grade: int | None = None
    resistance: int | None = None
    time_from_course: int | None = None
    cycle_length: int | None = None
    temperature: int | None = None
    cycles: int | None = None
    total_cycles: int | None = None
    gps_accuracy: int | None = None
    vertical_speed: int | None = None
    calories: int | None = None
    fractional_cadence: float | None = None
    step_length: int | None = None
    absolute_pressure: int | None = None
    respiration_rate: float | None = None
    enhanced_respiration_rate: float | None = None
    current_stress: int | None = None
    ascent_rate: int | None = None


class LapModel(BaseModel):
    message_index: int
    timestamp: datetime

    sport: str | None = None
    sub_sport: str | None = None

    start_position_lat: int | None = None
    start_position_long: int | None = None
    end_position_lat: int | None = None
    end_position_long: int | None = None

    total_elapsed_time: float | None = None
    total_timer_time: float | None = None
    total_moving_time: float | None = None

    total_distance: float | None = None

    start_time: datetime | None = None

    avg_speed: float | None = None
    enhanced_avg_speed: float | None = None
    max_speed: float | None = None
    enhanced_max_speed: float | None = None

    avg_heart_rate: int | None = None
    max_heart_rate: int | None = None
    min_heart_rate: int | None = None

    avg_cadence: int | None = None
    avg_running_cadence: int | None = None
    max_cadence: int | None = None
    max_running_cadence: int | None = None

    total_ascent: int | None = None
    total_descent: int | None = None
    avg_altitude: float | None = None
    enhanced_avg_altitude: float | None = None
    max_altitude: float | None = None
    enhanced_max_altitude: float | None = None
    min_altitude: float | None = None
    enhanced_min_altitude: float | None = None
    avg_grade: int | None = None
    avg_pos_grade: int | None = None
    avg_neg_grade: int | None = None
    max_pos_grade: int | None = None
    max_neg_grade: int | None = None

    wkt_step_index: int | None = None

    event: str | None = None
    event_type: str | None = None

    total_cycles: int | None = None
    total_strides: int | None = None
    total_strokes: int | None = None

    total_calories: int | None = None
    total_fat_calories: int | None = None

    intensity: int | None = None
    lap_trigger: int | str | None = None
    gps_accuracy: int | None = None

    avg_temperature: int | None = None
    max_temperature: int | None = None
    min_tempearture: int | None = None

    avg_respiration_rate: float | None = None
    enhanced_avg_respiration_rate: float | None = None
    max_respiration_rate: float | None = None
    enhanced_max_respiration_rate: float | None = None


class SetModel(BaseModel):
    timestamp: datetime
    set_type: str
    duration: float | None = None
    repetitions: int | None = None
    weight: float | None = None
    start_time: datetime | None = None
    category: list[str | int | None] | None = None
    category_subtype: list[str | int | None] | None = None
    weight_display_unit: str | None = None
    message_index: int | None = None
    wkt_step_index: int | None = None

    @validator("set_type", pre=True, always=True)
    @classmethod
    def convert_set_type(cls, value):
        return value if value is not None else "Unknown"


class SplitModel(BaseModel):
    split_type: str
    total_elapsed_time: float
    total_timer_time: float
    start_time: datetime

    # I figured out what this fields are in my activities recorded with a
    # Garmin Fenix 6s. For example: in split messages there's a key which value
    # is 15 with heart rate's average.
    avg_hr: int | None = Field(None, alias="15")
    max_hr: int | None = Field(None, alias="16")
    total_calories: int | None = Field(None, alias="28")
    difficulty: int | None = Field(None, alias="70")
    result: int | None = Field(None, alias="71")  # completed (3) or try (2)
    discarded: int | None = Field(None, alias="80")  # discarded (0)


class WorkoutModel(BaseModel):
    message_index: int | None = None
    sport: str | None = None
    sub_sport: str | None = None
    capabilities: int | None = None
    num_valid_steps: int | None = None
    wkt_name: str | None = None
    pool_length: int | None = None
    pool_length_unit: str | None = None

    @validator("wkt_name", pre=True, always=True)
    @classmethod
    def convert_wkt_name(cls, value):
        if value is not None and isinstance(value, list):
            return ", ".join(value)
        return value


class WorkoutStepModel(BaseModel):
    message_index: int

    wkt_step_name: str | None = None

    duration_type: str | None = None
    duration_value: int | None = None
    duration_time: float | None = None
    duration_distance: float | None = None
    duration_hr: int | None = None
    duration_calories: int | None = None
    duration_step: int | None = None
    duration_power: int | None = None
    duration_reps: int | None = None

    target_type: str | None = None
    target_value: int | None = None
    target_speed_zone: int | None = None
    target_hr_zone: int | None = None
    target_cadence_zone: int | None = None
    target_power_zone: int | None = None
    target_stroke_type: int | None = None

    repeat_steps: int | None = None
    repeat_time: float | None = None
    repeat_distance: float | None = None
    repeat_calories: int | None = None
    repeat_hr: int | None = None
    repeat_power: int | None = None

    custom_target_value_low: int | None = None
    custom_target_speed_low: float | None = None
    custom_target_heart_rate_low: int | None = None
    custom_target_cadence_low: int | None = None
    custom_target_power_low: int | None = None
    custom_target_value_high: int | None = None
    custom_target_speed_high: float | None = None
    custom_target_heart_rate_high: int | None = None
    custom_target_cadence_high: int | None = None
    custom_target_power_high: int | None = None

    intensity: str | None = None
    notes: str | None = None

    exercise_category: str | int | None = None
    exercise_name: str | int | None = None
    exercise_weight: float | None = None

    weight_display_unit: str | None = None

    secondary_target_type: str | None = None
    secondary_target_value: int | None = None
    secondary_target_speed_zone: int | None = None
    secondary_target_hr_zone: int | None = None
    secondary_target_cadence_zone: int | None = None
    secondary_target_power_zone: int | None = None
    secondary_target_stroke_type: int | None = None

    secondary_custom_target_value_low: int | None = None
    secondary_custom_target_speed_low: float | None = None
    secondary_custom_target_heart_rate_low: int | None = None
    secondary_custom_target_cadence_low: int | None = None
    secondary_custom_target_power_low: int | None = None
    secondary_custom_target_value_high: int | None = None
    secondary_custom_target_speed_high: float | None = None
    secondary_custom_target_heart_rate_high: int | None = None
    secondary_custom_target_cadence_high: int | None = None
    secondary_custom_target_power_high: int | None = None

    @validator("notes", pre=True, always=True)
    @classmethod
    def convert_notes(cls, value):
        if value is not None and isinstance(value, list):
            return ", ".join(value)
        return value


class MonitoringInfoModel(BaseModel):
    timestamp: datetime
    local_timestamp: int | None = None
    activity_type: list[str] | None = None
    cycles_to_distance: list[float] | None = None
    cycles_to_calories: list[float] | None = None
    resting_metabolic_rate: int | None = None


class MonitoringModel(BaseModel):
    timestamp: datetime | None = None
    # "device_index",
    calories: int | None = None
    distance: float | None = None
    cycles: float | None = None
    steps: int | None = None
    strokes: int | None = None
    active_time: float | None = None  # in seconds
    activity_type: str | int | None = None
    activity_subtype: str | int | None = None
    activity_level: str | None = None  # low, medium, high
    distance_16: int | None = None
    cycles_16: int | None = None
    active_time_16: int | None = None
    local_timestamp: int | None = None
    temperature: int | None = None
    temperature_min: int | None = None
    temperature_max: int | None = None
    activity_time: int | None = None
    active_calories: int | None = None
    current_activity_type_intensity: int | None = None
    timestamp_min_8: int | None = None
    timestamp_16: int | None = None
    heart_rate: int | None = None
    intensity: int | None = None
    duration_min: int | None = None  # in minutes
    duration: int | None = None  # in seconds
    ascent: float | None = None
    descent: float | None = None
    moderate_activity_minutes: int | None = None
    vigorous_activity_minutes: int | None = None

    def is_daily_log(self) -> bool:
        """Check if datetime is a daily log.

        In monitoring messages the timestamp must align to logging interval, for
        example, time must be 00:00:00 for daily log.

        It returns True if utc_dt has 00:00:00 time in the local datetime.
        """
        if not self.timestamp:
            return False
        local_dt: datetime = try_to_compute_local_datetime(self.timestamp)
        return local_dt.hour == 0 and local_dt.minute == 0 and local_dt.second == 0


class MonitoringHrDataModel(BaseModel):
    timestamp: datetime
    resting_heart_rate: int
    current_day_resting_heart_rate: int


class StressLevelModel(BaseModel):
    stress_level_value: int
    stress_level_time: datetime


class RespirationRateModel(BaseModel):
    timestamp: datetime
    respiration_rate: float  # breaths/min


class HrvStatusSummaryModel(BaseModel):
    timestamp: datetime | None = None
    weekly_average: float | None = None
    last_night_average: float | None = None
    last_night_5_min_high: float | None = None
    baseline_low_upper: float | None = None
    baseline_balanced_lower: float | None = None
    baseline_balanced_upper: float | None = None
    status: str | int | None  # see HRV_STATUS in definitions


class HrvValueModel(BaseModel):
    timestamp: datetime
    value: int | None = None  # in ms (5 minute RMSSD)


class SleepAssessmentModel(BaseModel):
    combined_awake_score: int | None = None
    awake_time_score: int | None = None
    awakenings_count_score: int | None = None
    deep_sleep_score: int | None = None
    sleep_duration_score: int | None = None
    light_sleep_score: int | None = None
    overall_sleep_score: int | None = None
    sleep_quality_score: int | None = None
    sleep_recovery_score: int | None = None
    rem_sleep_score: int | None = None
    sleep_restlessness_score: int | None = None
    awakenings_count: int | None = None
    interruptions_score: int | None = None
    average_stress_during_sleep: float | None = None


class SleepLevelModel(BaseModel):
    timestamp: datetime
    sleep_level: str | int | None = None  # see SLEEP_LEVEL in definitions


class ActivityModel(BaseModel):
    session: SessionModel
    workout: WorkoutModel | None = None,
    workout_steps: list[WorkoutStepModel] = []


class MultisportActivityModel(BaseModel):
    sessions: list[SessionModel]
    records: list[RecordModel]
    laps: list[LapModel]


class DistanceActivityModel(ActivityModel):
    records: list[RecordModel]
    laps: list[LapModel] = []


class ClimbActivityModel(ActivityModel):
    splits: list[SplitModel] = []


class SetActivityModel(ActivityModel):
    sets: list[SetModel] = []


class MonitorModel(BaseModel):
    monitoring_info: MonitoringInfoModel
    monitorings: list[MonitoringModel]
    hr_datas: list[MonitoringHrDataModel] = []
    stress_levels: list[StressLevelModel] = []
    respiration_rates: list[RespirationRateModel] = []


class HrvModel(BaseModel):
    summary: HrvStatusSummaryModel
    values: list[HrvValueModel] = []


class SleepModel(BaseModel):
    assessment: SleepAssessmentModel
    levels: list[SleepLevelModel] = []
