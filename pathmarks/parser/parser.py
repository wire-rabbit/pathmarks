"""Log parsing support class."""
import asyncio
import re


class Parser:
    """Text-based logfile parsing support."""

    Messages = {"file_not_found": "File not found."}

    context_above: int = 3
    context_below: int = 3

    raw_content: str = ""

    content_lines: list[str] = []
    current_subset: list[str] = []

    def __init__(self, path: str) -> None:
        self.path = path

    async def load_content(self) -> tuple[str, str]:
        """Read the file contents from the path and return
        (content, error) as a tuple of strings."""

        # reset:
        self.content_lines = []
        self.raw_content = ""

        err_msg = ""
        if self.path == "":
            return "", ""

        try:
            with open(self.path, encoding="UTF-8") as f:
                for line in f:
                    # allow animations by yeilding control during the loop:
                    await asyncio.sleep(0)

                    self.content_lines.append(line)
            self.raw_content = "".join(self.content_lines)
        except FileNotFoundError:
            err_msg = self.Messages["file_not_found"]

        return self.raw_content, err_msg

    def prep_raw_content(self, s) -> str:
        """Add formatting and store metadata about content."""
        self.raw_content = s
        self.current_subset = self.content_lines = self.raw_content.splitlines()

    def get_reset_content(self) -> str:
        """Get the initial state with no search terms or added markup"""
        self.current_subset = self.content_lines = self.raw_content.splitlines()
        return "\n".join(self.content_lines)

    def filter_content_basic(self, s: str) -> str:
        """Return lines from raw content that contain the supplied substring.
        Case-insensitive."""
        if s == "":
            return self.get_reset_content()

        subset = []
        for line in self.content_lines:
            if s.lower() in line.lower():
                subset.append(line)

        self.current_subset = subset
        return "\n".join(subset)

    def filter_content_regex(self, pattern: str) -> str:
        """Return lines from raw content that match the supplied pattern."""
        try:
            regexp = re.compile(pattern, re.I)

            subset = []
            for line in self.content_lines:
                if regexp.match(line):
                    subset.append(line)

        except re.error:
            return "\n".join(self.current_subset)

        return "\n".join(subset)
