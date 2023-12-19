"""The ViewPane widget for interacting with logfile contents."""

from textual.app import App, ComposeResult
from textual.widget import Widget
from textual.widgets import Label


class ViewPane(Widget):
    """Augmented log viewer with search controls."""

    def compose(self) -> ComposeResult:
        """Return the widgets that make up the ViewPane."""
        yield Label("Hello ViewPane")


class DebugApp(App):
    """App for manually testing this widget in isolation."""

    def compose(self) -> ComposeResult:
        yield ViewPane()


if __name__ == "__main__":
    app = DebugApp()
    app.run()
