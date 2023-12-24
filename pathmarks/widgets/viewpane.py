"""The ViewPane widget for interacting with logfile contents."""

from textual.app import App, ComposeResult
from textual.containers import Vertical
from textual.reactive import reactive
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

    rich_log: RichLog = None

    logfile_path: reactive[str | None] = reactive("")

    search_pattern: str = ""

    def watch_logfile_path(self) -> None:
        """Respond to changes in the selected logfile path."""

        # For now just write the logfile path. We're just getting wired up.
        self.rich_log.clear()
        self.rich_log.write(self.logfile_path)

    def get_logfile_content(self) -> str:
        """Get the filtered content of a given logfile."""
        return self.logfile_path

    def compose(self) -> ComposeResult:
        """Return the widgets that make up the ViewPane."""

        self.rich_log = RichLog(id="log_view", highlight=True, markup=True)
        self.rich_log.write(self.get_logfile_content())

        with Vertical():
            yield Input(
                id="search_pattern", classes="input_row", placeholder="(search pattern)"
            )
            yield self.rich_log


class DebugApp(App):
    """App for manually testing this widget in isolation."""

    def compose(self) -> ComposeResult:
        yield ViewPane()


if __name__ == "__main__":
    app = DebugApp()
    app.run()
