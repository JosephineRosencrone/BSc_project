from .video.render import Video_render


def main():
    """
    The main function executes on command:
    `python -m rendering_app`.

    This is the program's entry point.
    """

    Video_render(name="test").run()
