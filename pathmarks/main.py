"""The app entrypoint."""

from textual.app import App, ComposeResult
from textual.widgets import Header, Footer


class PathmarksApp(App):
    """A Textual app for viewing/searching logfiles."""

    def compose(self) -> ComposeResult:
        """Create the app widgets."""
        yield Header()
        yield Footer()


def start():
    """Launch the app."""
    app = PathmarksApp()
    app.run()
