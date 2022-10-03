#!/usr/bin/env python3
import os
import pathlib
import shutil
import subprocess
import tempfile


def main():
    with tempfile.TemporaryDirectory() as tmpdirname:
        # The directory that we'll clone the devdata git repo into.
        git_dir = os.path.join(tmpdirname, "devdata")

        subprocess.check_call(
            ["git", "clone", "https://github.com/hypothesis/devdata.git", git_dir]
        )

        # Copy devdata env file into place.
        shutil.copyfile(
            os.path.join(git_dir, "publisher-account-test-site", "devdata.env"),
            os.path.join(pathlib.Path(__file__).parent.parent, ".devdata.env"),
        )


if __name__ == "__main__":
    main()
