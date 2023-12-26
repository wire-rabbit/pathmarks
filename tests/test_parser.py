"""Testing the logfile Parser."""
import asyncio
import pytest

from pathmarks.parser.parser import Parser


class TestParser:
    """Testing the pathmarks.parser class."""

    @pytest.mark.asyncio
    async def test_load_content_handles_file_not_found(self):
        """Assert that the content loader returns only error text for missing files."""
        parser = Parser("./does-not-exist.foo")
        content, err = await parser.load_content()

        assert err == Parser.Messages["file_not_found"]
        assert content == ""

    @pytest.mark.asyncio
    async def test_load_content_returns_content(self, tmpdir, simple_text_file_content):
        """Assert that the content loader returns simple text file content."""
        p = tmpdir.mkdir("fake_logs").join("foo.log")
        p.write(simple_text_file_content)
        parser = Parser(str(p))
        content, err = await parser.load_content()

        assert content == simple_text_file_content
        assert err == ""

    def test_filter_content_basic(self, multiline_file_content):
        """Assert that we can retrieve only lines matching a given pattern."""

        parser = Parser("no-file")
        parser.raw_content = multiline_file_content
        parser.content_lines = parser.raw_content.splitlines()

        assert "Lorem ipsum" not in parser.filter_content_basic("not-present")

    @pytest.fixture
    def simple_text_file_content(self):
        """Fixture content for a simple text file."""
        return "a single line"

    @pytest.fixture
    def multiline_file_content(self):
        """Fixture content for unstructured multi-line content."""
        return """
        Lorem ipsum dolor sit amet, consectetur adipiscing elit.
        Etiam finibus, est non gravida bibendum, augue ipsum 
        consectetur nisl, interdum facilisis est tortor non magna. 
        Integer ante nunc, viverra nec massa non, pharetra scelerisque 
        nisl. 

        Praesent convallis viverra turpis, quis interdum urna varius
        ultricies. Nunc et tincidunt nunc. Sed rhoncus nibh erat, vel
        maximus lacus rutrum egestas. Nam sed fringilla nunc. Ut 
        pellentesque, ante sed aliquet accumsan, odio urna posuere
        diam, nec vehicula dui sapien non lacus. Donec efficitur odio
        arcu, vel facilisis orci congue at. Quisque sollicitudin elit 
        nunc, vel tincidunt magna vulputate sed.
        """
