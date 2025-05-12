from rendering_app.scripts.process import process_video

# Check errors when loading fails
class TestProcess:
    def test_process_video_invalid_path(self):
        output = process_video("invalid_path.mp4", "output.mp4", lambda x: x)
        assert output == (None, None, None)

