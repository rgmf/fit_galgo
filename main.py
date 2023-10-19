import argparse
import os
import shutil
import zipfile

from fit_galgo.galgo import FitGalgo
from fit_galgo.fit.results import FitResult, FitError


# def compute_daily_steps(root_path: str, steps_data: dict[str, dict]) -> None:
#     for dirpath, dirnames, filenames in os.walk(root_path):
#         for filename in filenames:
#             file_path: str = os.path.join(dirpath, filename)
#             print(f">>>>>> {file_path}")
#             if filename.lower().endswith(".fit"):
#                 whiz: FitDataWhiz = FitDataWhiz(file_path)
#                 result: FitResult = whiz.parse()
#                 if isinstance(result, FitMonitor) and result.steps:
#                     steps_data[str(result.monitoring_date)] = {
#                         "steps": result.total_steps,
#                         "split_steps": [
#                             {
#                                 "steps": fit_steps.steps,
#                                 "distance": fit_steps.distance,
#                                 "calories": fit_steps.calories
#                             } for fit_steps in result.steps
#                         ],
#                         "calories": {
#                             "active": result.active_calories,
#                             "metabolic_calories": result.metabolic_calories,
#                             "total": result.total_calories
#                         },
#                         "intensities": [
#                             {
#                                 "datetime": i.datetime_local,
#                                 "vigorous": i.vigorous_minutes,
#                                 "moderate": i.moderate_minutes
#                             } for i in result.activity_intensities
#                         ]
#                     }
#             elif zipfile.is_zipfile(file_path):
#                 zip_file = zipfile.ZipFile(file_path)
#                 dir_to_unzip: str = filename + "_tmp"
#                 os.mkdir(dir_to_unzip)
#                 zip_file.extractall(dir_to_unzip)
#                 compute_daily_steps(dir_to_unzip, steps_data)
#                 shutil.rmtree(dir_to_unzip)


def compute_fit_files(
        root_path: str, fits: list[FitResult], errors: dict[str, FitError]
) -> None:
    for dirpath, dirnames, filenames in os.walk(root_path):
        for filename in filenames:
            file_path: str = os.path.join(dirpath, filename)
            if filename.lower().endswith(".fit"):
                galgo: FitGalgo = FitGalgo(file_path)
                result: FitResult = galgo.parse()
                if isinstance(result, FitError):
                    errors[file_path] = result
                else:
                    fits.append(result)
            elif zipfile.is_zipfile(file_path):
                zip_file = zipfile.ZipFile(file_path)
                dir_to_unzip: str = filename + "_tmp"
                os.mkdir(dir_to_unzip)
                zip_file.extractall(dir_to_unzip)
                compute_fit_files(dir_to_unzip, fits, errors)
                shutil.rmtree(dir_to_unzip)


# def show_steps(data: dict[str, dict]) -> None:
#     dates = list(data.keys())
#     dates.sort()
#     data_ordered = {d: data[d] for d in dates}
#     for d, s in data_ordered.items():
#         print("######################################################")
#         print(f"{d}: {s}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="FIT Data Whiz")
    parser.add_argument(
        "-p", "--path",
        required=True,
        help="Root path where FIT files will searched"
    )
    args = parser.parse_args()

    # steps_data: dict[str, dict] = {}
    # compute_daily_steps(args.path, steps_data)
    # show_steps(steps_data)

    fits: list[FitResult] = []
    errors: dict[str, FitError] = {}
    compute_fit_files(args.path, fits, errors)
    import pdb; pdb.set_trace()
