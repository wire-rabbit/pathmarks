"""Testing the logfile Parser."""
import pytest

from pathmarks.parser.parser import Parser


class TestParser:
    """Testing the pathmarks.parser class."""

    def test_load_content_handles_file_not_found(self):
        """Assert that the content loader returns only error text for missing files."""
        parser = Parser("./does-not-exist.foo")
        content, err = parser.load_content()

        assert err == Parser.Messages["file_not_found"]
        assert content == ""

    def test_load_content_returns_content(self, tmpdir, simple_text_file_content):
        """Assert that the content loader returns simple text file content."""
        p = tmpdir.mkdir("fake_logs").join("foo.log")
        p.write(simple_text_file_content)
        parser = Parser(str(p))
        content, err = parser.load_content()

        assert content == simple_text_file_content
        assert err == ""

    @pytest.fixture
    def simple_text_file_content(self):
        """Fixture content for a simple text file."""
        return "a single line"
