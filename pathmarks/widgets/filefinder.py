"""The FileFinder widget for selecting logfiles to view."""

from pathlib import Path
from typing import Iterable
import os
import mimetypes

from textual.app import App, ComposeResult
from textual.containers import Vertical, Horizontal
from textual.widget import Widget
from textual.widgets import DirectoryTree, Input, Button


class _FilteredDirectoryTree(DirectoryTree):
    """Modified DirectoryTree that displays only directories and plain text files."""

    def filter_paths(self, paths: Iterable[Path]) -> Iterable[Path]:
        """Filter out non-text files."""
        result = []
        for path in paths:
            try:
                if path.is_dir():
                    result.append(path)

                if path.is_file() and mimetypes.guess_type(path)[0] == "text/plain":
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

    def validate_path(self, path: str) -> bool:
        """Is the path acceptable for the directory tree?"""
        if not os.path.exists(path):
            self.notify("This path does not appear to exist.")
            return False

        if not os.path.isdir(path):
            self.notify("This path is not a directory.")
            return False

        return True

    def change_path(self) -> None:
        """Update the _FilteredDirectoryTree widget or display an error."""
        path_input = self.query_one("#path_input")
        if not self.validate_path(path_input.value):
            path_input.value = ""
            return
        self.query_one("#ff_tree").path = path_input.value

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Event handler for the 'Go' button in the input row."""
        if event.button.id == "go_btn":
            self.change_path()

    def on_input_submitted(self) -> None:
        """Event handler for the path input."""
        self.change_path()

    def compose(self) -> ComposeResult:
        """Return the widgets that make up the FileFinder."""
        with Vertical():
            with Horizontal(classes="ff_input_row"):
                yield Input(
                    id="path_input", placeholder="/var/log", classes="ff_text_input"
                )
                yield Button("Go", id="go_btn", classes="ff_button", variant="primary")
            with Vertical():
                yield _FilteredDirectoryTree("/", id="ff_tree")


class DebugApp(App):
    """App for manually testing this widget in isolation."""

    def compose(self) -> ComposeResult:
        yield FileFinder()


if __name__ == "__main__":
    app = DebugApp()
    app.run()
