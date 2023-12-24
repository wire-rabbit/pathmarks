"""The app entrypoint."""

from textual.app import App, ComposeResult
from textual.containers import Horizontal

from pathmarks.widgets.viewpane import ViewPane
from pathmarks.widgets.filefinder import FileFinder


class PathmarksApp(App):
    """A Textual app for viewing/searching logfiles."""

    DEFAULT_CSS = """
    .widget_filefinder {
        width: 25%;
    }

    .widget_viewpane {
        width: 75%;
    }
    """

    def on_file_finder_path_selected(self, message: FileFinder.PathSelected) -> None:
        """Handle the FileFinder path selected event."""
        self.query_one(".widget_viewpane").logfile_path = str(message.selected_path)

    def compose(self) -> ComposeResult:
        """Create the app widgets."""
        with Horizontal():
            yield FileFinder(classes="widget_filefinder")
            yield ViewPane(classes="widget_viewpane")


def start():
    """Launch the app."""
    app = PathmarksApp()
    app.run()
