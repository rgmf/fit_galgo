from abc import ABC, abstractmethod

from pydantic import ValidationError, BaseModel

from fit_galgo.fit.definitions import (
    SPORTS, is_distance_sport, is_climb_sport, is_set_sport
)
from fit_galgo.fit.exceptions import (
    NotFitMessageFoundException,
    NotSupportedFitSportException,
    UnexpectedDataMessageException,
    FitMessageValidationException
)
from fit_galgo.fit.models import (
    FitModel,
    FitError,
    Activity,
    DistanceActivity,
    ClimbActivity,
    SetActivity,
    MultisportActivity,
    Monitor,
    Hrv,
    Sleep,
    FileId,
    Workout,
    WorkoutStep,
    Session,
    MonitoringInfo,
    Monitoring,
    MonitoringHrData,
    StressLevel,
    RespirationRate,
    HrvStatusSummary,
    HrvValue
)


class FitAbstractParser(ABC):
    @abstractmethod
    def __init__(
            self,
            fit_file_path: str,
            messages: dict[str, list[BaseModel]],
            zone_info: str | None = None
    ) -> None:
        pass

    @abstractmethod
    def parse(self) -> FitModel | FitError:
        pass


class FitActivityParser(FitAbstractParser):
    """Parser for fit activity files.

    It parses a fit file using the Garmin SDK library and build a FitActivity
    object that contains all stats from the FIT file.

    Also, it handles the errors that save into an array of errors.
    """

    def __init__(
            self,
            fit_file_path: str,
            messages: dict[str, list[BaseModel]],
            zone_info: str | None = None
    ) -> None:
        self._fit_file_path: str = fit_file_path
        self._messages: dict[str, list] = messages
        self._zone_info: str | None = zone_info

    def parse(self) -> Activity | FitError:
        if "FILE_ID" not in self._messages:
            return FitError(
                self._fit_file_path,
                [NotFitMessageFoundException("file_id")]
            )
        if len(self._messages["FILE_ID"]) != 1:
            return FitError(
                self._fit_file_path,
                [
                    UnexpectedDataMessageException(
                        "file_id",
                        "expected one message per file but got "
                        f"{len(self._messages['FILE_ID'])} messages"
                    )
                ]
            )
        if not self._messages["SESSION"]:
            return FitError(self._fit_file_path, [NotFitMessageFoundException("session")])

        if not self._supported_sport_in_session():
            return FitError(
                self._fit_file_path,
                [
                    NotSupportedFitSportException(
                        self._messages["SESSION"][0].sport,
                        self._messages["SESSION"][0].sub_sport
                    )
                ]
            )

        try:
            return self._build_activity()
        except ValidationError as error:
            return FitError(self._fit_file_path, [FitMessageValidationException(error)])
        except NotSupportedFitSportException as error:
            return FitError(self._fit_file_path, [error])

    def _supported_sport_in_session(self) -> bool:
        supported: list[str] = [n for k, v in SPORTS.items() for n in v.keys()]
        not_supported: list[str] = [
            s for s in self._messages["SESSION"] if s.sport not in supported
        ]

        if not_supported:
            return False
        return True

    def _build_activity(self) -> Activity:
        """Try to build the activity model.

        :return: the BaseModel built upon messages.

        :raise: NotSupportedFitSportException if the sport in the message is
                not supported.
        """
        file_id: FileId = self._messages["FILE_ID"][0]

        if len(self._messages["SESSION"]) > 1:
            return MultisportActivity(
                fit_file_path=self._fit_file_path,
                file_id=file_id,
                zone_info=self._zone_info,
                sessions=[session_model for session_model in self._messages["SESSION"]],
                records=[record_model for record_model in self._messages["RECORD"]],
                laps=[lap_model for lap_model in self._messages["LAP"]]
            )

        workout: Workout | None = (
            self._messages["WORKOUT"][0] if self._messages["WORKOUT"] else None
        )
        workout_steps: list[WorkoutStep] = self._messages["WORKOUT_STEP"]
        session: Session = self._messages["SESSION"][0]

        if is_distance_sport(session.sport):
            return DistanceActivity(
                fit_file_path=self._fit_file_path,
                file_id=file_id,
                zone_info=self._zone_info,
                session=session,
                records=[r for r in self._messages["RECORD"]],
                laps=[lap for lap in self._messages["LAP"]],
                workout=workout,
                workout_steps=workout_steps
            )

        if is_climb_sport(session.sport):
            return ClimbActivity(
                fit_file_path=self._fit_file_path,
                file_id=file_id,
                zone_info=self._zone_info,
                session=session,
                splits=[s for s in self._messages["SPLIT"]],
                workout=workout,
                workout_steps=workout_steps
            )

        if is_set_sport(session.sport):
            return SetActivity(
                fit_file_path=self._fit_file_path,
                file_id=file_id,
                zone_info=self._zone_info,
                session=session,
                sets=[s for s in self._messages["SET"]],
                workout=workout,
                workout_steps=workout_steps
            )

        raise NotSupportedFitSportException(session.sport, session.sub_sport)


class FitMonitoringParser(FitAbstractParser):
    def __init__(
            self,
            fit_file_path: str,
            messages: dict[str, list[BaseModel]],
            zone_info: str | None = None
    ) -> None:
        self._fit_file_path: str = fit_file_path
        self._messages: dict[str, list] = messages
        self._zone_info: str | None = zone_info

    def parse(self) -> Monitor | FitError:
        if "FILE_ID" not in self._messages:
            return FitError(
                self._fit_file_path,
                [NotFitMessageFoundException("file_id")]
            )
        if len(self._messages["FILE_ID"]) != 1:
            return FitError(
                self._fit_file_path,
                [
                    UnexpectedDataMessageException(
                        "file_id",
                        "expected one message per file but got "
                        f"{len(self._messages['FILE_ID'])} messages"
                    )
                ]
            )
        if "MONITORING_INFO" not in self._messages:
            return FitError(
                self._fit_file_path,
                [NotFitMessageFoundException("monitoring_info")]
            )

        if len(self._messages["MONITORING_INFO"]) != 1:
            return FitError(
                self._fit_file_path,
                [
                    UnexpectedDataMessageException(
                        "monitoring_info",
                        "expected one message per file but got "
                        f"{len(self._messages['MONITORING_INFO'])} messages"
                    )
                ]
            )

        try:
            file_id: FileId = self._messages["FILE_ID"][0]
            monitoring_info: MonitoringInfo = self._messages["MONITORING_INFO"][0]
            monitorings: list[Monitoring] = (
                [message for message in self._messages["MONITORING"]]
                if "MONITORING" in self._messages else []
            )
            hr_datas: list[MonitoringHrData] = (
                [message for message in self._messages["MONITORING_HR_DATA"]]
                if "MONITORING_HR_DATA" in self._messages else []
            )
            stress_levels: list[StressLevel] = (
                [message for message in self._messages["STRESS_LEVEL"]]
                if "STRESS_LEVEL" in self._messages else []
            )
            respiration_rates: list[RespirationRate] = (
                [message for message in self._messages["RESPIRATION_RATE"]]
                if "RESPIRATION_RATE" in self._messages else []
            )
            return Monitor(
                fit_file_path=self._fit_file_path,
                file_id=file_id,
                zone_info=self._zone_info,
                monitoring_info=monitoring_info,
                monitorings=monitorings,
                hr_datas=hr_datas,
                stress_levels=stress_levels,
                respiration_rates=respiration_rates
            )
        except ValidationError as error:
            return FitError(self._fit_file_path, [FitMessageValidationException(error)])


class FitHrvParser(FitAbstractParser):
    def __init__(
            self,
            fit_file_path: str,
            messages: dict[str, list[BaseModel]],
            zone_info: str | None = None
    ) -> None:
        self._fit_file_path: str = fit_file_path
        self._messages: dict[str, list[BaseModel]] = messages
        self._zone_info: str | None = zone_info

    def parse(self) -> Hrv | FitError:
        if "FILE_ID" not in self._messages:
            return FitError(
                self._fit_file_path,
                [NotFitMessageFoundException("file_id")]
            )
        if len(self._messages["FILE_ID"]) != 1:
            return FitError(
                self._fit_file_path,
                [
                    UnexpectedDataMessageException(
                        "file_id",
                        "expected one message per file but got "
                        f"{len(self._messages['FILE_ID'])} messages"
                    )
                ]
            )
        if "HRV_STATUS_SUMMARY" not in self._messages:
            return FitError(self._fit_file_path, [NotFitMessageFoundException("hrv_status_summary")])

        if "HRV_VALUE" not in self._messages:
            return FitError(self._fit_file_path, [NotFitMessageFoundException("hrv_value")])

        if len(self._messages["HRV_STATUS_SUMMARY"]) != 1:
            return FitError(
                self._fit_file_path,
                [
                    UnexpectedDataMessageException(
                        "hrv_status_summary",
                        "expected one message per file but got "
                        f"{len(self._messages['HRV_STATUS_SUMMARY'])} messages"
                    )
                ]
            )

        try:
            file_id: FileId = self._messages["FILE_ID"][0]
            summary: HrvStatusSummary = self._messages["HRV_STATUS_SUMMARY"][0]
            values: list[HrvValue] = self._messages["HRV_VALUE"]
            return Hrv(
                fit_file_path=self._fit_file_path,
                file_id=file_id,
                zone_info=self._zone_info,
                summary=summary,
                values=values
            )
        except ValidationError as error:
            return FitError(self._fit_file_path, [FitMessageValidationException(error)])


class FitSleepParser(FitAbstractParser):
    def __init__(
            self,
            fit_file_path: str,
            messages: dict[str, list[BaseModel]],
            zone_info: str | None = None
    ) -> None:
        self._fit_file_path: str = fit_file_path
        self._messages: dict[str, list] = messages
        self._zone_info: str | None = zone_info

    def parse(self) -> Sleep | FitError:
        if "FILE_ID" not in self._messages:
            return FitError(
                self._fit_file_path,
                [NotFitMessageFoundException("file_id")]
            )
        if len(self._messages["FILE_ID"]) != 1:
            return FitError(
                self._fit_file_path,
                [
                    UnexpectedDataMessageException(
                        "file_id",
                        "expected one message per file but got "
                        f"{len(self._messages['FILE_ID'])} messages"
                    )
                ]
            )
        if "SLEEP_ASSESSMENT" not in self._messages:
            return FitError(
                self._fit_file_path,
                [NotFitMessageFoundException("sleep_assessment")]
            )

        if "SLEEP_LEVEL" not in self._messages:
            return FitError(
                self._fit_file_path,
                [NotFitMessageFoundException("sleep_level")]
            )

        if len(self._messages["SLEEP_ASSESSMENT"]) != 1:
            return FitError(
                self._fit_file_path,
                [
                    UnexpectedDataMessageException(
                        "sleep_assessment",
                        "expected one message per file but got "
                        f"{len(self._messages['SLEEP_ASSESSMENT'])} messages"
                    )
                ]
            )

        try:
            file_id = self._messages["FILE_ID"][0]
            assessment = self._messages["SLEEP_ASSESSMENT"][0]
            levels = [level for level in self._messages["SLEEP_LEVEL"]]
            return Sleep(
                fit_file_path=self._fit_file_path,
                file_id=file_id,
                zone_info=self._zone_info,
                assessment=assessment,
                levels=levels
            )
        except ValidationError as error:
            return FitError(self._fit_file_path, [FitMessageValidationException(error)])
