import magic
from pathlib import Path
from typing import Iterable

from textual.app import App, ComposeResult
from textual.containers import Vertical, Horizontal
from textual.widget import Widget
from textual.widgets import DirectoryTree, Input, Button


class _FilteredDirectoryTree(DirectoryTree):
    """Modified DirectoryTree that displays only directories and plain text files."""

    def filter_paths(self, paths: Iterable[Path]) -> Iterable[Path]:
        """Filter out non-text files."""
        result = []
        m = magic.Magic(mime=True)
        for path in paths:
            try:
                if path.is_dir():
                    result.append(path)

                if path.is_file() and m.from_file(path) == "text/plain":
                    result.append(path)
            except PermissionError:
                continue
        return result


class FileFinder(Widget):
    """An enhanced DirectoryTree widget to support typing and selection."""

    DEFAULT_CSS = """
    .ff_input_row {
        height: 5;
        padding-top: 1;
        padding-bottom: 1;
    }

    .ff_text_input {
        width: 3fr;
    }

    .ff_button {
        width: 1fr;
    }
    """

    def compose(self) -> ComposeResult:
        """Return the widgets that make up the FileFinder."""
        with Vertical():
            with Horizontal(classes="ff_input_row"):
                yield Input(placeholder="/var/log", classes="ff_text_input")
                yield Button("Go", classes="ff_button")
            with Vertical():
                yield _FilteredDirectoryTree("/")


class DebugApp(App):
    """App for manually testing this widget in isolation."""

    def compose(self) -> ComposeResult:
        yield FileFinder()


if __name__ == "__main__":
    app = DebugApp()
    app.run()
