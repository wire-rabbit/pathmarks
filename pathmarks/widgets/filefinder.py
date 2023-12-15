import magic
from pathlib import Path
from typing import Iterable

from textual.app import App, ComposeResult
from textual.widget import Widget
from textual.widgets import DirectoryTree


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

    def compose(self) -> ComposeResult:
        """Return the widgets that make up the FileFinder."""
        yield _FilteredDirectoryTree("/")


class DebugApp(App):
    """App for manually testing this widget in isolation."""

    def compose(self) -> ComposeResult:
        yield FileFinder()


if __name__ == "__main__":
    app = DebugApp()
    app.run()
