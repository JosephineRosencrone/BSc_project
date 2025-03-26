import json
from dataclasses import dataclass
from typing import Any, List


@dataclass
class KernelSetting:
    name: str
    filterType: str
    blurOrSharpenCheckbox: bool
    kernelSize: int
    sigma: float
    sigma2: float
    timeFiltersApllied: int

    @staticmethod
    def from_dict(obj: Any) -> "KernelSetting":
        _name = str(obj.get("name"))
        _filterType = str(obj.get("filterType"))
        _blurOrSharpenCheckbox = bool(obj.get("blurOrSharpenCheckbox"))
        _kernelSize = int(obj.get("kernelSize"))
        _sigma = float(obj.get("sigma"))
        _sigma2 = float(obj.get("sigma2"))
        _timeFiltersApllied = int(obj.get("timeFiltersApllied"))
        return KernelSetting(
            _name,
            _filterType,
            _blurOrSharpenCheckbox,
            _kernelSize,
            _sigma,
            _sigma2,
            _timeFiltersApllied,
        )


@dataclass
class FilterSettings:
    settings: List[KernelSetting]

    @staticmethod
    def from_dict(obj: Any) -> "FilterSettings":
        _settings = [KernelSetting.from_dict(y) for y in obj.get("settings")]
        return FilterSettings(_settings)

    @staticmethod
    def import_config(file_path: str) -> "FilterSettings":
        # Open and read the file context
        with open(file_path, "r") as file:
            json_string = file.read()

        # Parse the JSON string into a Python dictionary
        json_data = json.loads(json_string)
        return FilterSettings.from_dict(json_data)


# ___________ Test for developers ___________
if __name__ == "__main__":
    filter_settings = FilterSettings.import_config(
        file_path=r"C:\Users\josep\Desktop\config.txt"
    )
    print(filter_settings.settings)
