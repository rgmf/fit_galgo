from enum import Enum, StrEnum

UNKNOWN = "unknown"


# Split's type.
class SplitType(StrEnum):
    ASCENT_SPLIT = "ascent_split"
    DESCENT_SPLIT = "descent_split"
    INTERVAL_ACTIVE = "interval_active"
    INTERVAL_REST = "interval_rest"
    INTERVAL_WARMUP = "interval_warmup"
    INTERVAL_COOLDOWN = "interval_cooldown"
    INTERVAL_RECOVERY = "interval_recovery"
    INTERVAL_OTHER = "interval_other"
    CLIMB_ACTIVE = "climb_active"
    CLIMB_REST = "climb_rest"
    SURF_ACTIVE = "surf_active"
    RUN_ACTIVE = "run_active"
    RUN_REST = "run_rest"
    WORKOUT_ROUND = "workout_round"
    RWD_RUN = "rwd_run"
    RWD_WALK = "rwd_walk"
    WINDSURF_ACTIVE = "windsurf_active"
    RWD_STAND = "rwd_stand"
    TRANSITION = "transition"
    SKI_LIFT_SPLIT = "ski_lift_split"
    SKI_RUN_SPLIT = "ski_run_split"
    UNKNOWN = "unknown"


# Split's result.
class ClimbResult(Enum):
    COMPLETED = 1
    ATTEMPTED = 2
    DISCARDED = 3


# Set types.
class SetType(StrEnum):
    UNKNOWN = "unknown"
    ACTIVE = "active"
    REST = "rest"


# Training's excercise categories.
EXERCISE_CATEGORIES = {
    0: "bench_press",
    1: "calf_raise",
    2: "cardio",
    3: "carry",
    4: "chop",
    5: "core",
    6: "crunch",
    7: "curl",
    8: "deadlift",
    9: "flye",
    10: "hip_raise",
    11: "hip_stability",
    12: "hip_swing",
    13: "hyperextension",
    14: "lateral_raise",
    15: "leg_curl",
    16: "leg_raise",
    17: "lunge",
    18: "olympic_lift",
    19: "plank",
    20: "plyo",
    21: "pull_up",
    22: "push_up",
    23: "row",
    24: "shoulder_press",
    25: "shoulder_stability",
    26: "shrug",
    27: "sit_up",
    28: "squat",
    29: "total_body",
    30: "triceps_extension",
    31: "warm_up",
    32: "run",
    65534: "unknown"
}


class ExerciseCategories(StrEnum):
    BENCH_PRESS = "bench_press"
    CALF_RAISE = "calf_raise"
    CARDIO = "cardio"
    CARRY = "carry"
    CHOP = "chop"
    CORE = "core"
    CRUNCH = "crunch"
    CURL = "curl"
    DEADLIFT = "deadlift"
    FLYE = "flye"
    HIP_RAISE = "hip_raise"
    HIP_STABILITY = "hip_stability"
    HIP_SWING = "hip_swing"
    HYPEREXTENSION = "hyperextension"
    LATERAL_RAISE = "lateral_raise"
    LEG_CURL = "leg_curl"
    LEG_RAISE = "leg_raise"
    LUNGE = "lunge"
    OLYMPIC_LIFT = "olympic_lift"
    PLANK = "plank"
    PLYO = "plyo"
    PULL_UP = "pull_up"
    PUSH_UP = "push_up"
    ROW = "row"
    SHOULDER_PRESS = "shoulder_press"
    SHOULDER_STABILITY = "shoulder_stability"
    SHRUG = "shrug"
    SIT_UP = "sit_up"
    SQUAT = "squat"
    TOTAL_BODY = "total_body"
    TRICEPS_EXTENSION = "triceps_extension"
    WARM_UP = "warm_up"
    RUN = "run"
    UNKNOWN = "unknown"
    REST = "rest"


# Supported sports organized by categories.
# Each category contains a list of sports, each with a list of sub-sport.
# The values used for 'sport' and 'sub-sport' are from the FIT standard (Profile).
DISTANCE_CATEGORY = "distance"
SET_CATEGORY = "set"
CLIMB_CATEGORY = "climbing"
MULTISPORT_CATEGORY = "multisport"

RUNNING_SPORT = "running"
WALKING_SPORT = "walking"
HIKING_SPORT = "hiking"
CYCLING_SPORT = "cycling"
SWIMMING_SPORT = "swimming"

ROCK_CLIMBING_SPORT = "rock_climbing"
TRAINING_SPORT = "training"

TRANSITION_SPORT = "transition"

GENERIC_SUB_SPORT = "generic"
TRAIL_SUB_SPORT = "trail"
ROAD_SUB_SPORT = "road"
MOUNTAIN_SUB_SPORT = "mountain"
SWIMMING_SUB_SPORT = "lap_swimming"
BOULDERING_SUB_SPORT = "bouldering"
STRENGTH_TRAINING_SUB_SPORT = "strength_training"

SPORTS = {
    DISTANCE_CATEGORY: {
        RUNNING_SPORT: [GENERIC_SUB_SPORT, TRAIL_SUB_SPORT],
        WALKING_SPORT: [GENERIC_SUB_SPORT],
        HIKING_SPORT: [GENERIC_SUB_SPORT],
        CYCLING_SPORT: [GENERIC_SUB_SPORT, ROAD_SUB_SPORT, MOUNTAIN_SUB_SPORT],
        SWIMMING_SPORT: [GENERIC_SUB_SPORT, SWIMMING_SUB_SPORT]
    },
    SET_CATEGORY: {
        TRAINING_SPORT: [GENERIC_SUB_SPORT, STRENGTH_TRAINING_SUB_SPORT]
    },
    CLIMB_CATEGORY: {
        ROCK_CLIMBING_SPORT: [GENERIC_SUB_SPORT, BOULDERING_SUB_SPORT]
    },
    MULTISPORT_CATEGORY: {
        TRANSITION_SPORT: [GENERIC_SUB_SPORT]
    }
}

ACTIVITY_TYPES = {
    0: "generic",
    1: "running",
    2: "cycling",
    3: "transition",
    4: "fitness_equipment",
    5: "swimming",
    6: "walking",
    8: "sedentary",
    254: "all"
}
ACTIVITY_TYPE_UNKNOWN = "unknown"

HRV_STATUS = {
    0: "none",
    1: "poor",
    2: "low",
    3: "unbalanced",
    4: "balanced"
}

SLEEP_LEVEL = {
    0: "unmeasurable",
    1: "awake",
    2: "light",
    3: "deep",
    4: "rem"
}


def is_distance_sport(sport: str) -> bool:
    return sport in SPORTS[DISTANCE_CATEGORY]


def is_climb_sport(sport: str) -> bool:
    return sport in SPORTS[CLIMB_CATEGORY]


def is_set_sport(sport: str) -> bool:
    return sport in SPORTS[SET_CATEGORY]
