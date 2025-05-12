from rendering_app.scripts.import_config import KernelSetting, FilterSettings

class TestImportConfig:
    # Checks that KernelSetting parses data correctly
    def test_kernel_setting_from_dict(self):
        data = {
            "name": "Test",
            "filterType": "gauss",
            "blurOrSharpenCheckbox": True,
            "kernelSize": 5,
            "sigma": 1.5,
            "sigma2": 0.0,
            "timeFiltersApllied": 2
        }
        setting = KernelSetting.from_dict(data)
        assert setting.filterType == "gauss"

    # Checks that FilterSettings converts a list into a list of KernelSetting objects
    def test_filter_settings_from_dict(self):
        data = {"settings": [{
            "name": "Test",
            "filterType": "gauss",
            "blurOrSharpenCheckbox": True,
            "kernelSize": 5,
            "sigma": 1.5,
            "sigma2": 0.0,
            "timeFiltersApllied": 2
        }] * 3}
        config = FilterSettings.from_dict(data)
        assert len(config.settings) == 3
