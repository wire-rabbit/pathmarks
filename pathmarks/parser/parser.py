"""Log parsing support class."""


class Parser:
    """Text-based logfile parsing support."""

    Messages = {"file_not_found": "File not found."}

    def __init__(self, path: str) -> None:
        self.path = path

    def load_content(self) -> tuple[str, str]:
        """Read the file contents from the path and return (content, error) as a tuple of strings."""
        content = err_msg = ""
        if self.path == "":
            return "", ""

        try:
            with open(self.path) as f:
                content = f.read()
        except FileNotFoundError as err:
            err_msg = self.Messages["file_not_found"]

        return content, err_msg
