import argparse
from typing import List, Tuple, Union

from utils.logger import logger


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
            "--cxmin",
            default=None,
            dest="cxmin",
            help=(
                "Provide the x min value to crop the frames to. It does not "
                "crop the frame by default."
            ),
            type=int,
        )
        self._parser.add_argument(
            "--cxmax",
            default=None,
            dest="cxmax",
            help=(
                "Provide the x max value to crop the frames to. It does not "
                "crop the frame by default."
            ),
            type=int,
        )
        self._parser.add_argument(
            "--cymin",
            default=None,
            dest="cymin",
            help=(
                "Provide the y min value to crop the frames to. It does not "
                "crop the frame by default."
            ),
            type=int,
        )
        self._parser.add_argument(
            "--cymax",
            default=None,
            dest="cymax",
            help=(
                "Provide the y max value to crop the frames to. It does not "
                "crop the frame by default."
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

    def _validate_gt_zero(
        self, arg: Union[int, None], str_repr: str
    ) -> Tuple[bool, str]:
        """Helper function that validates if a given arg is greater than 0"""

        if arg is not None and arg <= 0:
            return False, f"'--{str_repr}' argument must be greater than 0"
        return True, ""

    def _validate_positive(
        self, arg: Union[int, None], str_repr: str
    ) -> Tuple[bool, str]:
        """Helper function that validates if a given arg is positive"""

        if arg is not None and arg < 0:
            return False, f"'--{str_repr}' argument must be greater or equal to 0"
        return True, ""

    @staticmethod
    def validate_crop_axis(
        cmin: Union[int, None],
        cmax: Union[int, None],
        axis: Union[int, None],
        axis_repr: str,
    ) -> Tuple[bool, str]:
        """
        Helper function that determines if a given cmin, cmax and axis is valid for
        cropping
        """
        w_or_h = "width" if axis == "x" else "height"
        if axis and cmin is None:
            cmin = 0
        if axis and cmax is None:
            cmax = axis

        if axis:
            if cmin == cmax:
                return (
                    False,
                    (
                        f"'--c{axis_repr}min' and '--c{axis_repr}max' should "
                        "not be equal"
                    ),
                )
            if cmin >= axis:
                return (
                    False,
                    (
                        f"'--c{axis_repr}min' should not be greater or equal "
                        f"to '--{w_or_h}'"
                    ),
                )
            if cmax > axis:
                return (
                    False,
                    f"'--c{axis_repr}max' should not be greater than '--{w_or_h}'",
                )
            if cmax - cmin > axis:
                return (
                    False,
                    (
                        f"'--c{axis_repr}max' - '--c{axis_repr}min' should not be "
                        f"greater than '--{w_or_h}'"
                    ),
                )
        return True, ""

    def _validate_args(self, args: argparse.Namespace) -> Tuple[bool, List[str]]:
        """Helper function that ensures that all arguments are valid"""

        valids = []
        msgs = []
        to_validate_gt_zero = {
            "fps": args.fps,
            "width": args.width,
            "height": args.height,
            "threads": args.threads,
        }
        to_validate_positive = {
            "cxmin": args.cxmin,
            "cxmax": args.cxmax,
            "cymin": args.cymin,
            "cymax": args.cymax,
        }

        # Is greater than 0 validation
        for k, v in to_validate_gt_zero.items():
            v, m = self._validate_gt_zero(v, k)
            valids.append(v)
            msgs.append(m)

        # Is positive validation
        for k, v in to_validate_positive.items():
            v, m = self._validate_positive(v, k)
            valids.append(v)
            msgs.append(m)

        # Crop validation
        v, m = self.validate_crop_axis(args.cxmin, args.cxmax, args.width, "x")
        valids.append(v)
        msgs.append(m)

        v, m = self.validate_crop_axis(args.cymin, args.cymax, args.height, "y")
        valids.append(v)
        msgs.append(m)

        return all(valids), [m for m in msgs if m]

    def parse_args(self, args=None) -> argparse.Namespace:
        """Parses the arguments from and valdates them"""

        parsed_args = self._parser.parse_args(args)
        valid, msgs = self._validate_args(parsed_args)
        if valid:
            return parsed_args
        for m in msgs:
            logger.error(m)
            exit(1)
