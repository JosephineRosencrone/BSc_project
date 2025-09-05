import os
import tempfile
from rendering_app.scripts.import_config import FilterSettings
from rendering_app.scripts.filter import Filter_With_Config
from rendering_app.scripts.vid_process import process_video
from moviepy import ColorClip


def test_video_integration():
    # Generate a short dummy video
    temp_dir = tempfile.mkdtemp()
    input_path = os.path.join(temp_dir, "input.mp4")
    output_path = os.path.join(temp_dir, "output.mp4")

    clip = ColorClip(size=(320, 240), color=(255, 0, 0)).set_duration(1)
    clip.write_videofile(input_path, fps=24, codec="libx264")

    # Simulate config
    config = {
        "settings": [{
            "name": "Red",
            "filterType": "boxBlur",
            "blurOrSharpenCheckbox": False,
            "kernelSize": 3,
            "sigma": 1.0,
            "sigma2": 0.0,
            "timeFiltersApllied": 1
        }] * 3
    }

    filter_settings = FilterSettings.from_dict(config)
    filter_func = Filter_With_Config(filter_settings).apply_to_image

    # Process video
    result_path, resolution, fps = process_video(input_path, output_path, filter_func)

    # Check output
    assert os.path.exists(result_path)
    assert resolution == (320, 240)
    assert fps == 24
