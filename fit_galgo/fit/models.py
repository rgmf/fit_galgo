from datetime import date, datetime, timedelta
from collections import namedtuple
from zoneinfo import ZoneInfo

from pydantic import (
    BaseModel,
    field_validator,
    Field,
    ConfigDict,
    AliasChoices,
    computed_field
)

from fit_galgo.fit.definitions import (
    HRV_STATUS,
    ACTIVITY_TYPES,
    ACTIVITY_TYPE_UNKNOWN,
    SplitType,
    ClimbResult,
    TRANSITION_SPORT,
    is_distance_sport,
    SLEEP_LEVEL,
    UNKNOWN,
    EXERCISE_CATEGORIES,
    SetType
)
from fit_galgo.utils.date_utils import combine_date_and_seconds

DoubleStat = namedtuple("DoubleStat", ["max", "avg"])
TripleStat = namedtuple("TripleStat", ["max", "min", "avg"])
AltitudeStat = namedtuple("AltitudeStat", ["max", "min", "gain", "loss"])
LocationStat = namedtuple("LocationStat", ["lat", "lon"])
LocationRecordStat = namedtuple(
    "LocationRecordStat", ["lat", "lon", "altitude", "gps_accuracy"]
)
WorkoutDuration = namedtuple(
    "WorkoutDuration",
    [
        "type", "value", "time", "distance", "hr", "calories", "step", "power", "reps"
    ]
)
WorkoutRepeat = namedtuple(
    "WorkoutRepeat", ["steps", "time", "distance", "calories", "hr", "power",]
)
WorkoutTarget = namedtuple(
    "WorkoutTarget",
    [
        "type", "value", "speed_zone", "hr_zone", "cadence_zone",
        "power_zone", "stroke_type"
    ]
)
WorkoutCustomTarget = namedtuple(
    "WorkoutCustomTarget",
    [
        "value_low", "speed_low", "heart_rate_low", "cadence_low", "power_low",
        "value_high", "speed_high", "heart_rate_high", "cadence_high", "power_high"
    ]
)
RecordsAndLaps = namedtuple("RecordsAndLaps", ["records", "laps"])


class FileId(BaseModel):
    file_type: str | int = Field(validation_alias=AliasChoices("type", "file_type"))
    serial_number: int | None = None
    time_created: datetime | None = None
    manufacturer: str | None = None
    product: int | None = None
    garmin_product: str | None = None


class FitModel(BaseModel):
    fit_file_path: str
    file_id: FileId
    zone_info: str | None = None


class FitError(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    fit_file_path: str
    errors: list[Exception]


class WorkoutExercise(BaseModel):
    category: str
    name: str = UNKNOWN
    weight: float = 0.0

    @field_validator("category", mode="before")
    @classmethod
    def convert_category(cls, value):
        if value is None:
            return UNKNOWN
        if isinstance(value, str) and value in EXERCISE_CATEGORIES:
            return EXERCISE_CATEGORIES[value]
        return str(value)


class WorkoutStep(BaseModel):
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

    @field_validator("notes", mode="before")
    @classmethod
    def convert_notes(cls, value):
        if value is not None and isinstance(value, list):
            return ", ".join(value)
        return value

    def duration(self) -> WorkoutDuration:
        return WorkoutDuration(
            self.duration_type,
            self.duration_value,
            self.duration_time,
            self.duration_distance,
            self.duration_hr,
            self.duration_calories,
            self.duration_step,
            self.duration_power,
            self.duration_reps
        )

    def repeat(self) -> WorkoutRepeat:
        return WorkoutRepeat(
            self.repeat_steps,
            self.repeat_time,
            self.repeat_distance,
            self.repeat_calories,
            self.repeat_hr,
            self.repeat_power
        )

    def target(self) -> WorkoutTarget:
        return WorkoutTarget(
            self.target_type,
            self.target_value,
            self.target_speed_zone,
            self.target_hr_zone,
            self.target_cadence_zone,
            self.target_power_zone,
            self.target_stroke_type
        )

    def secondary_target(self) -> WorkoutTarget:
        return WorkoutTarget(
            self.secondary_target_type,
            self.secondary_target_value,
            self.secondary_target_speed_zone,
            self.secondary_target_hr_zone,
            self.secondary_target_cadence_zone,
            self.secondary_target_power_zone,
            self.secondary_target_stroke_type
        )

    def custom_target(self) -> WorkoutCustomTarget:
        return WorkoutCustomTarget(
            self.custom_target_value_low,
            self.custom_target_speed_low,
            self.custom_target_heart_rate_low,
            self.custom_target_cadence_low,
            self.custom_target_power_low,
            self.custom_target_value_high,
            self.custom_target_speed_high,
            self.custom_target_heart_rate_high,
            self.custom_target_cadence_high,
            self.custom_target_power_high
        )

    def secondary_custom_target(self) -> WorkoutCustomTarget:
        return WorkoutCustomTarget(
            self.secondary_custom_target_value_low,
            self.secondary_custom_target_speed_low,
            self.secondary_custom_target_heart_rate_low,
            self.secondary_custom_target_cadence_low,
            self.secondary_custom_target_power_low,
            self.secondary_custom_target_value_high,
            self.secondary_custom_target_speed_high,
            self.secondary_custom_target_heart_rate_high,
            self.secondary_custom_target_cadence_high,
            self.secondary_custom_target_power_high
        )

    def exercise(self) -> WorkoutExercise:
        return WorkoutExercise(
            self.exercise_category, self.exercise_name, self.exercise_weight
        )


class Workout(BaseModel):
    steps: list[WorkoutStep] = []
    wkt_name: str = UNKNOWN
    sport: str = UNKNOWN
    sub_sport: str = UNKNOWN
    message_index: int | None = None
    capabilities: int | None = None
    num_valid_steps: int | None = None
    pool_length: int | None = None
    pool_length_unit: str | None = None

    @field_validator("wkt_name", mode="before")
    @classmethod
    def convert_wkt_name(cls, value):
        if isinstance(value, list):
            value = ", ".join(filter(None, (v.strip() for v in value)))
        return value if value else UNKNOWN


class Session(BaseModel):
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


class TimeStat(BaseModel):
    timestamp: datetime
    start_time: datetime
    elapsed: float
    timer: float
    work: float


class Activity(FitModel):
    session: Session
    workout: Workout | None = None
    workout_steps: list[WorkoutStep] = []

    @computed_field
    @property
    def time(self) -> TimeStat:
        return TimeStat(
            timestamp=self.session.timestamp,
            start_time=self.session.start_time,
            elapsed=self.session.total_elapsed_time,
            timer=self.session.total_timer_time,
            work=self.session.total_timer_time
        )

    @property
    def name(self) -> str:
        return self.session.sport

    @property
    def sport(self) -> str:
        return self.session.sport

    @property
    def sub_sport(self) -> str:
        return self.session.sub_sport

    @property
    def heart_rate(self) -> DoubleStat:
        return DoubleStat(
            max=self.session.max_heart_rate,
            avg=self.session.avg_heart_rate
        )

    @property
    def temperature(self) -> TripleStat:
        return TripleStat(
            max=self.session.max_temperature,
            min=self.session.min_temperature,
            avg=self.session.avg_temperature
        )

    @property
    def total_calories(self) -> int:
        return self.session.total_calories


class MultiActivity(FitModel):
    sessions: list[Session]


class Record(BaseModel):
    timestamp: datetime
    activity_type: str | None = None
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

    compressed_speed_distance: list[str | int] | None = None
    time_from_course: int | None = None
    speed_1s: list[int] | None = None
    compressed_accumulated_power: int | None = None
    accumulated_power: int | None = None
    left_right_balance: int | None = None
    vertical_oscillation: int | None = None
    stance_time_percent: int | None = None
    stance_time: int | None = None
    left_torque_effectiveness: int | None = None
    right_torque_effectiveness: int | None = None
    left_pedal_smoothness: int | None = None
    right_pedal_smoothness: int | None = None
    combined_pedal_smoothness: int | None = None
    time128: int | None = None
    stroke_type: str | None = None
    zone: int | None = None
    ball_speed: int | None = None
    cadence256: int | None = None
    fractional_cadence: float | None = None
    total_hemoglobin_conc: int | None = None
    total_hemoglobin_conc_min: int | None = None
    total_hemoglobin_conc_max: int | None = None
    saturated_hemoglobin_percent: int | None = None
    saturated_hemoglobin_percent_min: int | None = None
    saturated_hemoglobin_percent_max: int | None = None
    device_index: int | None = None
    left_pco: int | None = None
    right_pco: int | None = None
    left_power_phase: list[int] | None = None
    left_power_phase_peak: list[int] | None = None
    right_power_phase: list[int] | None = None
    right_power_phase_peak: list[int] | None = None
    battery_soc: int | None = None
    motor_power: int | None = None
    vertical_ratio: int | None = None
    stance_time_balance: int | None = None
    step_length: int | None = None
    cycle_length16: float | None = None
    absolute_pressure: int | None = None
    depth: int | None = None
    next_stop_depth: int | None = None
    next_stop_time: int | None = None
    time_to_surface: int | None = None
    ndl_time: int | None = None
    cns_load: int | None = None
    n2_load: int | None = None
    grit: float | None = None
    flow: float | None = None
    ebike_travel_range: int | None = None
    ebike_battery_level: int | None = None
    ebike_assist_mode: int | None = None
    ebike_assist_level_percent: int | None = None
    air_time_remaining: int | None = None
    pressure_sac: int | None = None
    volume_sac: int | None = None
    rmv: int | None = None
    po2: int | None = None
    core_temperature: int | None = None

    @property
    def datetime_utc(self) -> datetime:
        return self.timestamp

    @property
    def location(self) -> LocationRecordStat:
        return LocationRecordStat(
            lat=self.position_lat,
            lon=self.position_long,
            altitude=self.enhanced_altitude or self.altitude,
            gps_accuracy=self.gps_accuracy
        )


class Lap(BaseModel):
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

    @property
    def time(self) -> TimeStat:
        return TimeStat(
            timestamp=self.timestamp,
            start_time=self.start_time,
            elapsed=self.total_elapsed_time,
            timer=self.total_timer_time,
            work=self.total_elapsed_time
        )

    @property
    def speed(self) -> DoubleStat:
        return DoubleStat(
            max=self.enhanced_max_speed or self.max_speed,
            avg=self.enhanced_avg_speed or self.avg_speed
        )

    @property
    def heart_rate(self) -> DoubleStat:
        return DoubleStat(max=self.max_heart_rate, avg=self.avg_heart_rate)

    @property
    def altitude(self) -> AltitudeStat:
        return AltitudeStat(
            max=self.enhanced_max_altitude or self.max_altitude,
            min=self.enhanced_min_altitude or self.min_altitude,
            gain=self.total_ascent,
            loss=self.total_descent
        )

    @property
    def cadence(self) -> DoubleStat:
        return DoubleStat(
            max=self.max_cadence or self.max_running_cadence,
            avg=self.avg_cadence or self.avg_running_cadence
        )

    def start_location(self) -> LocationStat:
        return LocationStat(
            lat=self.start_position_lat, lon=self.start_position_long
        )

    def end_location(self) -> LocationStat:
        return LocationStat(
            lat=self.end_position_lat, lon=self.end_position_long
        )


class DistanceActivity(Activity):
    records: list[Record]
    laps: list[Lap] = []

    @property
    def altitudes(self) -> list[float]:
        return [
            record.enhanced_altitude or record.altitude or 0 for record in self.records
        ]

    @property
    def total_distance(self) -> float | None:
        return self.session.total_distance

    @property
    def speed(self) -> DoubleStat:
        return DoubleStat(
            max=self.session.enhanced_max_speed or self.session.max_speed,
            avg=self.session.enhanced_avg_speed or self.session.avg_speed
        )

    @property
    def cadence(self) -> DoubleStat:
        return DoubleStat(
            max=self.session.max_cadence or self.session.max_running_cadence,
            avg=self.session.avg_cadence or self.session.avg_running_cadence
        )

    @property
    def altitude(self) -> AltitudeStat:
        return AltitudeStat(
            max=max(self.altitudes),
            min=min(self.altitudes),
            gain=self.session.total_ascent,
            loss=self.session.total_descent
        )

    @property
    def total_strides(self) -> int | None:
        self.session.total_strides

    @property
    def start_location(self) -> LocationStat:
        return LocationStat(
            lat=self.session.start_position_lat,
            lon=self.session.start_position_long
        )

    @property
    def end_location(self) -> LocationStat:
        return LocationStat(
            lat=self.session.end_position_lat,
            lon=self.session.end_position_long
        )


class LapActivity(DistanceActivity):
    """Distance activity based on Lap(s).

    Because of that working time can be computed from laps.

    An example of this kind of activities are lap swimming sport.
    """

    @property
    def time(self) -> TimeStat:
        return TimeStat(
            timestamp=self.session.timestamp,
            start_time=self.session.start_time,
            elapsed=self.session.total_elapsed_time,
            timer=self.session.total_timer_time,
            work=self._computed_elapsed_time()
        )

    def _computed_elapsed_time(self):
        computed_elapsed_time = sum(
            [l.total_elapsed_time for l in self.laps if l.total_distance > 0]
        )
        if computed_elapsed_time:
            return computed_elapsed_time
        return self.session.total_timer_time


class Split(BaseModel):
    split_type: str
    total_elapsed_time: float
    total_timer_time: float
    start_time: datetime

    # I figured out what this fields are in my activities recorded with a
    # Garmin Fenix 6s. For example: in split messages there's a key which value
    # is 15 with heart rate's average.
    avg_hr: int | None = Field(None, validation_alias=AliasChoices("15", "avg_hr"))
    max_hr: int | None = Field(None, validation_alias=AliasChoices("16", "max_hr"))
    total_calories: int | None = Field(None, validation_alias=AliasChoices("28", "total_calories"))
    difficulty: int | None = Field(None, validation_alias=AliasChoices("70", "difficulty"))
    result: int | None = Field(None, validation_alias=AliasChoices("71", "result"))  # completed (3) or try (2)
    discarded: int | None = Field(None, validation_alias=AliasChoices("80", "discarded"))  # discarded (0)


class Climb(BaseModel):
    split: Split

    @property
    def time(self) -> TimeStat:
        return TimeStat(
            timestamp=self.split.start_time,
            start_time=self.split.start_time,
            elapsed=self.split.total_elapsed_time,
            timer=self.split.total_timer_time,
            work=(
                self.split.total_elapsed_time
                if self.split.split_type == SplitType.CLIMB_ACTIVE.value
                else 0.0
            )
        )

    @property
    def split_type(self) -> SplitType:
        return (
            self.split.split_type if self.split.split_type in list(SplitType)
            else SplitType.UNKNOWN
        )

    @property
    def heart_rate(self) -> DoubleStat:
        return DoubleStat(max=self.split.max_hr, avg=self.split.avg_hr)

    @property
    def total_calories(self) -> int:
        return self.split.total_calories

    @property
    def difficulty(self) -> int:
        return self.split.difficulty

    @property
    def result(self) -> ClimbResult:
        return (
            ClimbResult.COMPLETED if self.split.result == 3 else (
                ClimbResult.ATTEMPTED
                if self.split.result == 2 else ClimbResult.DISCARDED
            )
        )


class ClimbActivity(Activity):
    splits: list[Split] = []

    @property
    def climbs(self) -> list[Climb]:
        return [Climb(split=s) for s in self.splits]

    @property
    def time(self) -> TimeStat:
        return TimeStat(
            timestamp=self.session.timestamp,
            start_time=self.session.start_time,
            elapsed=self.session.total_elapsed_time,
            timer=self.session.total_timer_time,
            work=sum([c.time.work for c in self.climbs])
        )


class Set(BaseModel):
    timestamp: datetime
    set_type: SetType
    duration: float | None = None
    repetitions: int | None = None
    weight: float | None = None
    start_time: datetime | None = None
    category: list[str | int | None] | None = None
    category_subtype: list[str | int | None] | None = None
    weight_display_unit: str | None = None
    message_index: int | None = None
    wkt_step_index: int | None = None

    @field_validator("set_type", mode="before")
    @classmethod
    def convert_set_type(cls, value):
        return value if value in list(SetType) else SetType.UNKNOWN

    @property
    def order(self) -> int:
        return self.message_index or 0

    @property
    def exercise(self) -> str:
        if self.category is None:
            return UNKNOWN

        categories = [
            EXERCISE_CATEGORIES.get(value, str(value))
            if value is not None else value for value in self.category
        ]
        valid_categories = [cat for cat in categories if cat is not None]

        return UNKNOWN if not valid_categories else ", ".join(valid_categories)

    @property
    def time(self) -> TimeStat:
        return TimeStat(
            timestamp=self.timestamp,
            start_time=self.start_time,
            elapsed=self.duration,
            timer=self.duration,
            work=(
                self.duration
                if self.set_type.value == SetType.ACTIVE.value
                else 0.0
            )
        )

    def is_active_set(self) -> bool:
        """Check if this set is an active one.

        A set can be an active or a rest one.
        """
        return self.set_type == SetType.ACTIVE


class SetActivity(Activity):
    sets: list[Set] = []

    @property
    def time(self) -> TimeStat:
        return TimeStat(
            timestamp=self.session.timestamp,
            start_time=self.session.start_time,
            elapsed=self.session.total_elapsed_time,
            timer=self.session.total_timer_time,
            work=sum([s.time.work for s in self.sets])
        )


class TransitionActivity(Activity):
    pass


class MultisportActivity(MultiActivity):
    records: list[Record]
    laps: list[Lap]

    @property
    def activities(self) -> list[Activity]:
        activity_list: list[Activity] = []
        for session in self.sessions:
            if session.sport == TRANSITION_SPORT:
                activity = TransitionActivity(
                    fit_file_path=self.fit_file_path,
                    file_id=self.file_id,
                    zone_info=self.zone_info,
                    session=session
                )
            elif is_distance_sport(session.sport):
                session_records, session_laps = self.filter_by_session(session)
                activity = DistanceActivity(
                    fit_file_path=self.fit_file_path,
                    file_id=self.file_id,
                    zone_info=self.zone_info,
                    session=session,
                    workout=None,
                    workout_steps=[],
                    records=session_records,
                    laps=session_laps
                )
            else:
                activity = Activity(self.fit_file_path, Activity(session=session))
            activity_list.append(activity)
        return activity_list

    def filter_by_session(self, session: Session) -> RecordsAndLaps:
        if not isinstance(session.start_time, datetime):
            return RecordsAndLaps([], [])
        if not isinstance(session.total_timer_time, int | float):
            return RecordsAndLaps([], [])

        datetime_from: datetime = session.start_time
        datetime_to: datetime = (
            session.start_time + timedelta(seconds=session.total_timer_time)
        )

        return RecordsAndLaps(
            [
                record for record in self.records
                if datetime_from <= record.timestamp <= datetime_to
            ],
            [
                lap for lap in self.laps
                if datetime_from <= lap.timestamp <= datetime_to
            ]
        )


class Monitoring(BaseModel):
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


class Steps(BaseModel):
    steps: int
    distance: float
    calories: int


class HeartRate(BaseModel):
    heart_rate: int
    datetime_utc: datetime


class ActivityIntensity(BaseModel):
    moderate_minutes: int
    vigorous_minutes: int
    datetime_utc: datetime | None = None


class MonitoringInfo(BaseModel):
    timestamp: datetime
    activity_type: list[str] | None = None
    cycles_to_distance: list[float] | None = None
    cycles_to_calories: list[float] | None = None
    resting_metabolic_rate: int | None = None


class MonitoringHrData(BaseModel):
    timestamp: datetime
    resting_heart_rate: int
    current_day_resting_heart_rate: int


class StressLevel(BaseModel):
    stress_level_value: int
    stress_level_time: datetime


class RespirationRate(BaseModel):
    timestamp: datetime
    respiration_rate: float  # breaths/min


class Monitor(FitModel):
    monitoring_info: MonitoringInfo
    monitorings: list[Monitoring]
    hr_datas: list[MonitoringHrData] = []
    stress_levels: list[StressLevel] = []
    respiration_rates: list[RespirationRate] = []

    def is_daily_log(self, dt_utc: datetime) -> bool:
        """Check if datetime is a daily log.

        In monitoring messages the timestamp must align to logging interval, for
        example, time must be 00:00:00 for daily log.

        It returns True if utc_dt has 00:00:00 time in the local datetime.
        """
        if not dt_utc:
            return False
        local_dt: datetime = dt_utc.astimezone(
            ZoneInfo(self.zone_info) if self.zone_info else None
        )
        return local_dt.hour == 0 and local_dt.minute == 0 and local_dt.second == 0

    @computed_field
    @property
    def datetime_utc(self) -> datetime:
        return self.monitoring_info.timestamp

    @property
    def datetime_local(self) -> datetime:
        return self.monitoring_info.timestamp.astimezone(
            ZoneInfo(self.zone_info) if self.zone_info else None
        )

    @property
    def monitoring_date(self) -> date:
        return date(
            year=self.datetime_local.year,
            month=self.datetime_local.month,
            day=self.datetime_local.day
        )

    @computed_field
    @property
    def metabolic_calories(self) -> int:
        return self.monitoring_info.resting_metabolic_rate or 0

    @computed_field
    @property
    def activities(self) -> list[str]:
        return self._activity_types_as_str()

    @computed_field
    @property
    def active_calories(self) -> int:
        return sum([
            (value if value is not None else 0)
            for m in self.monitorings if self.is_daily_log(m.timestamp)
            for value in [m.active_calories, m.calories] if value is not None
        ])

    @computed_field
    @property
    def total_calories(self) -> int:
        return self.metabolic_calories + self.active_calories

    @computed_field
    @property
    def steps(self) -> list[Steps]:
        return [
            Steps(
                steps=m.steps,
                distance=m.distance or 0,
                calories=m.active_calories or m.calories or 0
            ) for m in self.monitorings if self.is_daily_log(m.timestamp) and m.steps
        ]

    @computed_field
    @property
    def total_steps(self) -> int:
        return sum([step.steps for step in self.steps])

    @computed_field
    @property
    def total_distance(self) -> int:
        return sum([step.distance for step in self.steps])

    @computed_field
    @property
    def heart_rates(self) -> list[HeartRate]:
        return [
            HeartRate(
                heart_rate=m.heart_rate,
                datetime_utc=combine_date_and_seconds(
                    self.monitoring_date, m.timestamp_16
                )
            )
            for m in self.monitorings
            if (
                    self.monitoring_date is not None and
                    m.heart_rate is not None and
                    m.timestamp_16 is not None
            )
        ]

    @computed_field
    @property
    def activity_intensities(self) -> list[ActivityIntensity]:
        def compute_datetime(dt: datetime | None, ts_16: int | None) -> datetime | None:
            if dt is None or ts_16 is None:
                return None
            return combine_date_and_seconds(dt, ts_16)

        return [
            ActivityIntensity(
                moderate_minutes=m.moderate_activity_minutes or 0,
                vigorous_minutes=m.vigorous_activity_minutes or 0,
                datetime_utc=compute_datetime(self.monitoring_date, m.timestamp_16)
            )
            for m in self.monitorings
            if m.timestamp_16 is not None and (
                    m.moderate_activity_minutes is not None or
                    m.vigorous_activity_minutes is not None
            )
        ]

    def _activity_types_as_str(self) -> list[str]:
        if self.monitoring_info.activity_type is None:
            return []

        activity_types: list[str] = []
        for at in self.monitoring_info.activity_type:
            if at in ACTIVITY_TYPES:
                activity_types.append(ACTIVITY_TYPES[at])
            elif type(at) is str:
                activity_types.append(at)
            else:
                activity_types.append(ACTIVITY_TYPE_UNKNOWN)

        return activity_types


class HrvStatusSummary(BaseModel):
    timestamp: datetime | None = None
    weekly_average: float | None = None
    last_night_average: float | None = None
    last_night_5_min_high: float | None = None
    baseline_low_upper: float | None = None
    baseline_balanced_lower: float | None = None
    baseline_balanced_upper: float | None = None
    status: str | int | None = None  # see HRV_STATUS in definitions


class HrvValue(BaseModel):
    timestamp: datetime
    value: int | None = None  # in ms (5 minute RMSSD)


class Hrv(FitModel):
    summary: HrvStatusSummary
    values: list[HrvValue] = []

    @property
    def datetime_utc(self) -> datetime | None:
        return self.summary.timestamp

    @property
    def weekly_average(self) -> float | None:
        return self.summary.weekly_average

    @property
    def last_night_average(self) -> float | None:
        return self.summary.last_night_average

    @property
    def last_night_5_min_high(self) -> float | None:
        return self.summary.last_night_5_min_high

    @property
    def baseline_low_upper(self) -> float | None:
        return self.summary.baseline_low_upper

    @property
    def baseline_balanced_lower(self) -> float | None:
        return self.summary.baseline_balanced_lower

    @property
    def baseline_balanced_upper(self) -> float | None:
        return self.summary.baseline_balanced_upper

    @computed_field
    @property
    def status(self) -> str:
        if isinstance(self.summary.status, int):
            return (
                HRV_STATUS[self.summary.status]
                if self.summary.status in HRV_STATUS
                else HRV_STATUS[0]
            )
        return self.summary.status


class SleepLevel(BaseModel):
    timestamp: datetime
    sleep_level: str | int | None = None  # see SLEEP_LEVEL in definitions

    @property
    def datetime_utc(self) -> datetime:
        return self.timestamp

    @computed_field
    @property
    def level(self) -> str:
        return (
            self.sleep_level
            if isinstance(self.sleep_level, str)
            else (
                SLEEP_LEVEL[self.sleep_level]
                if self.sleep_level in SLEEP_LEVEL else SLEEP_LEVEL[0]
            )
        )


class SleepAssessment(BaseModel):
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


class Sleep(FitModel):
    assessment: SleepAssessment
    levels: list[SleepLevel] = []

    @computed_field
    @property
    def dates(self) -> list[datetime]:
        sorted_dates: list[datetime] = sorted(
            [level.datetime_utc for level in self.levels]
        )
        if sorted_dates == 0:
            return []
        elif sorted_dates == 1:
            return [sorted_dates[0], sorted_dates[0]]
        else:
            return [sorted_dates[0], sorted_dates[-1]]

    @property
    def combined_awake_score(self) -> int | None:
        return self.assessment.combined_awake_score

    @property
    def awake_time_score(self) -> int | None:
        return self.assessment.awake_time_score

    @property
    def awakenings_count_score(self) -> int | None:
        return self.assessment.awakenings_count_score

    @property
    def deep_sleep_score(self) -> int | None:
        return self.assessment.deep_sleep_score

    @property
    def sleep_duration_score(self) -> int | None:
        return self.assessment.sleep_duration_score

    @property
    def light_sleep_score(self) -> int | None:
        return self.assessment.light_sleep_score

    @property
    def overall_sleep_score(self) -> int | None:
        return self.assessment.overall_sleep_score

    @property
    def sleep_quality_score(self) -> int | None:
        return self.assessment.sleep_quality_score

    @property
    def sleep_recovery_score(self) -> int | None:
        return self.assessment.sleep_recovery_score

    @property
    def rem_sleep_score(self) -> int | None:
        return self.assessment.rem_sleep_score

    @property
    def sleep_restlessness_score(self) -> int | None:
        return self.assessment.sleep_restlessness_score

    @property
    def awakenings_count(self) -> int | None:
        return self.assessment.awakenings_count

    @property
    def interruptions_score(self) -> int | None:
        return self.assessment.interruptions_score

    @property
    def average_stress_during_sleep(self) -> float | None:
        return self.assessment.average_stress_during_sleep
