"""The FileFinder widget for selecting logfiles to view."""

from pathlib import Path
from typing import Iterable
import os
import subprocess

from textual.app import App, ComposeResult
from textual.containers import Vertical, Horizontal
from textual.message import Message
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

                if path.is_file() and self.is_text_file(path):
                    result.append(path)

            except PermissionError:
                continue
        return result

    def is_text_file(self, path: str) -> bool:
        """Use `file` shell command to identify binary file formats."""
        guessed_type = str(subprocess.check_output(["file", "--mime", "-b", path]))
        for t in ["text", "json"]:
            if t in guessed_type:
                return True
        return False


class FileFinder(Widget):
    """An enhanced DirectoryTree widget to support typing and selection."""

    class PathSelected(Message):
        """Path selected message."""

        def __init__(self, selected_path: str) -> None:
            self.selected_path = selected_path
            super().__init__()

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

    #ff_tree {
        border-top: solid gray;
    }
    """

    def validate_path(self, path: str) -> str:
        """Is the path acceptable for the directory tree?
        Returns an empty string or the selected/containing directory."""
        if not os.path.exists(path):
            self.notify("This path does not appear to exist.")
            return ""

        if not os.path.isdir(path):
            self.post_message(self.PathSelected(path))
            return os.path.dirname(path)

        return path

    def change_path(self) -> None:
        """Update the _FilteredDirectoryTree widget or display an error."""
        path_input = self.query_one("#path_input")
        new_path = self.validate_path(path_input.value)
        if not path_input:
            path_input.value = ""
            return
        self.query_one("#ff_tree").path = new_path

    def on_directory_tree_file_selected(
        self, message: DirectoryTree.FileSelected
    ) -> None:
        """Handle the event triggered by selecting a file in the widget."""
        # self.post_message(self.PathSelected(path))
        self.post_message(self.PathSelected(message.path))

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
                yield Button(
                    ":mag:", id="go_btn", classes="ff_button", variant="default"
                )
            with Vertical():
                yield _FilteredDirectoryTree("/", id="ff_tree")


class DebugApp(App):
    """App for manually testing this widget in isolation."""

    def compose(self) -> ComposeResult:
        yield FileFinder()


if __name__ == "__main__":
    app = DebugApp()
    app.run()
