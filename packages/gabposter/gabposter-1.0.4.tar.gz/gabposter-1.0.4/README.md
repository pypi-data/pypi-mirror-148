# Gabposter

Posts to a gab account text and image.

# Install

`python -m pip install gabposter`

# Api

```
from gabposter import gab_post, gab_test

USER = "gabusername"
PASS = "gabpassword"
FILE_JPG = "myfile.jpg"

assert gab_test(), "Webdriver doesn't work on your system"

gab_post(USER, PASS, "test", jpg_path=FILE_JPG)
```

# Tests

Just simply run `tox` at the command line and everything should be tested. You may need to install `tox` with `python -m pip tox`.

# Changes

  * 1.0.4: Adds gab_test() for testing that connecting to gab works using the webdriver.
  * 1.0.3: Fixed a bug where posts would sometimes not go through, due to the browser exiting too quickly.
  * 1.0.0: Initial code submit