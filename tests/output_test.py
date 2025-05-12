from unittest.mock import patch, MagicMock
from rendering_app.scripts.output import save_output_video

class TestOutput:
    @patch("rendering_app.scripts.output.filedialog.asksaveasfilename", return_value="test_output.mp4")
    @patch("rendering_app.scripts.output.VideoFileClip")
    
    # Checks saving logic works
    def test_save_output_video_success(self, mock_video_clip, mock_asksave):
        mock_clip = MagicMock()
        mock_video_clip.return_value = mock_clip
        mock_clip.with_audio.return_value = mock_clip

        save_output_video("temp_video.mp4", "original_video.mp4")
        mock_clip.write_videofile.assert_called_once()

    # Checks it doesn't try to save when user cancels save dialog
    @patch("rendering_app.scripts.output.filedialog.asksaveasfilename", return_value="")
    def test_save_output_video_no_path(self, mock_asksave):
        result = save_output_video("temp_video.mp4", "original_video.mp4")
        assert result is None
