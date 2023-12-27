"""Log parsing support class."""
import asyncio
import json
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
            is_json = True
            with open(self.path, encoding="UTF-8") as f:
                for line in f:
                    # allow animations by yeilding control during the loop:
                    await asyncio.sleep(0)

                    # if the line is JSON we want to pretty-print it:
                    if is_json:
                        is_json = self.append_maybe_json(line)
                    else:
                        is_json = False
                        self.content_lines.append(line)
            self.raw_content = "".join(self.content_lines)
        except FileNotFoundError:
            err_msg = self.Messages["file_not_found"]

        return self.raw_content, err_msg

    def append_maybe_json(self, line: str) -> bool:
        """Attempt to add JSON to content_lines in a prettified way.
        Return True if this was JSON, False otherwise."""
        try:
            json_line = json.loads(line)
            json_lines = json.dumps(json_line, indent=4).splitlines()
            for l in json_lines:
                self.content_lines.append(l + "\n")

            return True

        except ValueError:
            self.content_lines.append(line)
            return False

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
