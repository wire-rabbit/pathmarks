# Pathmarks: Log Search TUI

A log viewer built on [Textualize](https://www.textualize.io) with a file explorer, simple and regular expression searching, and JSON pretty-printing.

Tested on Linux and macOS. (Relies on the `file` shell command to detect plausible text files.)

Packaged with [Poetry](https://python-poetry.org).

```bash
# To download dependencies:
poetry install

# To run:
poetry run pathmarks

# To run tests:
poetry run pytest
```
*Example*: Inspect a logfile containing minified JSON and view just one field's values (data from [JSONPlaceholder](https://jsonplaceholder.typicode.com/users)):

![json-log-example](https://github.com/wire-rabbit/pathmarks/assets/17692361/8c775128-454d-41e1-ab90-251eec040325)

