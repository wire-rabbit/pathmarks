"""The ViewPane widget for interacting with logfile contents."""

from rich.errors import MarkupError
from textual import work
from textual.app import App, ComposeResult
from textual.containers import Vertical, Horizontal
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Input, RichLog, LoadingIndicator, RadioButton, RadioSet

from pathmarks.parser.parser import Parser


class ViewPane(Widget):
    """Augmented log viewer with search controls."""

    DEFAULT_CSS = """
    .vp_search_pattern_row {
        margin-top: 1;
        height: 5;
    }
    #vp_search_pattern {
        width: 3fr;
    }
    #vp_search_type {
        width: 1fr;
    }
    """

    parser: Parser = None

    rich_log: RichLog = None

    regex_search: bool = False

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

        if self.regex_search:
            self.write_log_content(self.parser.filter_content_regex(event.value))
        else:
            self.write_log_content(self.parser.filter_content_basic(event.value))

    def on_radio_set_changed(self, event: RadioSet.Changed) -> None:
        """Handle a change in the search pattern type."""
        if event.index == 1:
            self.regex_search = True
        else:
            self.regex_search = False

    def compose(self) -> ComposeResult:
        """Return the widgets that make up the ViewPane."""

        self.rich_log = RichLog(id="log_view", highlight=True, markup=False)
        self.loading_indicator = LoadingIndicator(id="loading_indicator")
        self.loading_indicator.display = False

        with Vertical():
            with Horizontal(classes="vp_search_pattern_row"):
                yield Input(
                    id="vp_search_pattern",
                    classes="vp_input",
                    placeholder="(search pattern)",
                )
                with RadioSet(id="vp_search_type"):
                    yield RadioButton("Simple", value=True)
                    yield RadioButton("Regex")
            yield self.rich_log
            yield self.loading_indicator


class DebugApp(App):
    """App for manually testing this widget in isolation."""

    def compose(self) -> ComposeResult:
        yield ViewPane()


if __name__ == "__main__":
    app = DebugApp()
    app.run()
