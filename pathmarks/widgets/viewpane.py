"""The ViewPane widget for interacting with logfile contents."""

from textual.app import App, ComposeResult
from textual.containers import Vertical
from textual.widget import Widget
from textual.widgets import Input, RichLog


class ViewPane(Widget):
    """Augmented log viewer with search controls."""

    DEFAULT_CSS = """
    .input_row {
        height: 5;
        padding-top: 1;
        padding-bottom: 1;
    }
    """

    logfile_path: str = ""

    search_pattern: str = ""

    def get_logfile_content(self) -> str:
        """Get the filtered content of a given logfile."""
        return "TODO"

    def compose(self) -> ComposeResult:
        """Return the widgets that make up the ViewPane."""

        with Vertical():
            yield Input(
                id="search_pattern", classes="input_row", placeholder="(search pattern)"
            )
            yield RichLog(id="log_view", highlight=True, markup=True)


class DebugApp(App):
    """App for manually testing this widget in isolation."""

    def compose(self) -> ComposeResult:
        yield ViewPane()


if __name__ == "__main__":
    app = DebugApp()
    app.run()
