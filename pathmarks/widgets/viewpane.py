"""The ViewPane widget for interacting with logfile contents."""

from rich.errors import MarkupError
from textual import work
from textual.app import App, ComposeResult
from textual.containers import Vertical
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Input, RichLog, LoadingIndicator

from pathmarks.parser.parser import Parser


class ViewPane(Widget):
    """Augmented log viewer with search controls."""

    DEFAULT_CSS = """
    .input_row {
        height: 5;
        padding-top: 1;
        padding-bottom: 1;
    }
    """

    parser: Parser = None

    rich_log: RichLog = None

    loading_indicator: LoadingIndicator = None

    logfile_path: reactive[str | None] = reactive("")

    search_pattern: str = ""

    def write_log_content(self, content):
        """Write the rich log contenet, handling errors."""
        self.rich_log.clear()
        try:
            self.rich_log.write(content)
        except MarkupError:
            self.rich_log.markup = False
            self.rich_log.write(content)

    @work
    async def watch_logfile_path(self) -> None:
        """Respond to changes in the selected logfile path."""
        self.rich_log.clear()

        self.loading_indicator.display = True

        self.parser = Parser(self.logfile_path)
        content, err = await self.parser.load_content()
        if err != "":
            self.notify(f"Error loading file: {err}")
            return

        if content == "" and self.logfile_path != "":
            self.notify("Empty file.")

        self.write_log_content(content)
        self.loading_indicator.display = False

    def on_input_changed(self, event) -> None:
        """Handle a change in the search pattern input."""
        if self.parser.raw_content == "":
            self.notify("No content to search.")
            return
        self.write_log_content(self.parser.filter_content_basic(event.value))

    def compose(self) -> ComposeResult:
        """Return the widgets that make up the ViewPane."""

        self.rich_log = RichLog(id="log_view", highlight=True, markup=False)
        self.loading_indicator = LoadingIndicator(id="loading_indicator")
        self.loading_indicator.display = False

        with Vertical():
            yield Input(
                id="search_pattern", classes="input_row", placeholder="(search pattern)"
            )
            yield self.rich_log
            yield self.loading_indicator


class DebugApp(App):
    """App for manually testing this widget in isolation."""

    def compose(self) -> ComposeResult:
        yield ViewPane()


if __name__ == "__main__":
    app = DebugApp()
    app.run()
