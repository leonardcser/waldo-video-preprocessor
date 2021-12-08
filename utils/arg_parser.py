import argparse


class ArgParser(object):
    """Helper class to parse command line arguments"""

    def __init__(self) -> None:
        self._parser = argparse.ArgumentParser()
        self._parser.add_argument(
            "-s",
            "--src",
            dest="src",
            help=(
                "Provide the source folder path to preprocess (it will preprocess "
                "all video files from that folder)"
            ),
            required=True,
            type=str,
        )

        self._parser.add_argument(
            "-d",
            "--dest",
            dest="dest",
            default="./out",
            help=(
                "Provide the destination folder path. Defaults to "
                "'./out' (creates the dest folder if it doesn't exist)"
            ),
            type=str,
        )
        self._parser.add_argument(
            "-f",
            "--fps",
            default=10,
            dest="fps",
            help="Provide the fps to preprocess from input. Defaults to 10",
            type=int,
        )
        self._parser.add_argument(
            "--width",
            default=None,
            dest="width",
            help=(
                "Provide the width to rescale the frames to. It does not "
                "rescale the width by default."
            ),
            type=int,
        )
        self._parser.add_argument(
            "--height",
            default=None,
            dest="height",
            help=(
                "Provide the height to rescale the frames to. It does not "
                "rescale the height by default."
            ),
            type=int,
        )
        self._parser.add_argument(
            "-g",
            "--gray",
            default=False,
            action="store_true",
            dest="gray",
            help="Extract to grayscale",
        )
        self._parser.add_argument(
            "--silent",
            default=False,
            action="store_true",
            dest="silent",
            help="Silent output",
        )
        self._parser.add_argument(
            "-t",
            "--threads",
            default=4,
            dest="threads",
            help="Provide the number of threads for thread pool. Defaults to 4",
            type=int,
        )
        self._parser.add_argument(
            "-ni",
            "--noinput",
            default=False,
            action="store_true",
            dest="no_input",
            help="Disables input from user",
        )

    def get_parser(self) -> argparse.ArgumentParser:
        return self._parser

    def parse_args(self, args=None) -> argparse.Namespace:
        return self._parser.parse_args(args)
