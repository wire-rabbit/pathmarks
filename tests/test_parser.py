"""Testing the logfile Parser."""
import json
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

        # Search term is not present in the results at all:
        assert "Lorem ipsum" not in parser.filter_content_basic("not-present")

        # Exact match is found:
        assert "applesauce" in parser.filter_content_basic("applesauce")

        # Match is case-insensitive:
        assert "applesauce" in parser.filter_content_basic("appleSAUCE")

        # Lines not containing a match are not returned:
        assert "bleary" not in parser.filter_content_basic("applesauce")

    def test_filter_content_regex(self, multiline_file_content):
        """Assert that we can retrieve only lines matching a given regular expression"""

        parser = Parser("no-file")
        parser.raw_content = multiline_file_content
        parser.content_lines = parser.raw_content.splitlines()

        # Search term is not present in the results at all:
        assert "Lorem ipsum" not in parser.filter_content_regex("not-present")

        # Exact match is found:
        assert "applesauce" in parser.filter_content_regex(".*applesauce*")

        # Match is case-insensitive:
        assert "applesauce" in parser.filter_content_regex(".*appleSAUCE*")

        # Lines not containing a match are not returned:
        assert "bleary" not in parser.filter_content_regex(".*applesauce*")

    def test_json_single_line_content_is_prettified(self, single_line_json_content):
        """Assert that single line JSON content will be expanded over mulitple lines"""

        parser = Parser("no-file")
        parser.raw_content = single_line_json_content
        parser.append_maybe_json(single_line_json_content)

        # The fixture is really giving us a single line:
        assert "\n" not in single_line_json_content

        # The list has multiple elements:
        assert len(parser.content_lines) > 1

        # The list should contain a specific string:
        found = False
        for line in parser.content_lines:
            if "Leanne Graham" in line:
                found = True
                break

        assert found

    @pytest.fixture
    def simple_text_file_content(self):
        """Fixture content for a simple text file."""
        return "a single line"

    @pytest.fixture
    def multiline_file_content(self):
        """Fixture content for unstructured multi-line content."""
        return """
        1. Applesauce cranberry excursion 10 marbles.
        2. bleary Nuisance sawdust 99 nettles.
        3. cranberry applesauce leading _?! leastaways.
        """

    @pytest.fixture
    def single_line_json_content(self):
        """Test data is from: jsonplaceholder.typicode.com/users."""
        multiline_json = """
        [
          {
            "id": 1,
            "name": "Leanne Graham",
            "username": "Bret",
            "email": "Sincere@april.biz",
            "address": {
              "street": "Kulas Light",
              "suite": "Apt. 556",
              "city": "Gwenborough",
              "zipcode": "92998-3874",
              "geo": {
                "lat": "-37.3159",
                "lng": "81.1496"
              }
            },
            "phone": "1-770-736-8031 x56442",
            "website": "hildegard.org",
            "company": {
              "name": "Romaguera-Crona",
              "catchPhrase": "Multi-layered client-server neural-net",
              "bs": "harness real-time e-markets"
            }
          }
        ]
        """
        return json.dumps(json.loads(multiline_json))
