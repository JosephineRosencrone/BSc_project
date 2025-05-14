import pytest
import numpy as np

from rendering_app.scripts.filter import Filter_With_Config
from rendering_app.scripts.import_config import FilterSettings, KernelSetting

class TestFilter:
    def setup_method(self):
        kernel = KernelSetting(
            name="red",
            filterType="boxBlur",
            blurOrSharpenCheckbox=False,
            kernelSize=3,
            sigma=1.0,
            sigma2=0.0,
            timeFiltersApllied=1,
        )
        self.settings = FilterSettings(settings=[kernel, kernel, kernel])
        self.filter = Filter_With_Config(filter_settings=self.settings)
        self.dummy_img = np.ones((100, 100, 3), dtype=np.uint8) * 255

    # Checks error when kernel size is invalid
    def test_blur_color_channel_invalid_kernel_size(self):
        self.settings.settings[0].kernelSize = -1
        with pytest.raises(ValueError):
            self.filter.blur_color_channel(self.dummy_img[:, :, 0], 0, 0)

    # Applies filter to dummy image
    def test_apply_to_image(self):
        result = self.filter.apply_to_image(self.dummy_img)
        assert result.shape == self.dummy_img.shape
