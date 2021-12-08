import argparse
from typing import Any, Callable, List, Tuple
import unittest

from utils.arg_parser import ArgParser
from utils.logger import logger


class TestArguments(unittest.TestCase):
    """Tests for command line arguments"""

    def setUp(self) -> None:
        self.default_args = ["-s", "./test"]

    def assertTypeEqual(self, first, _type) -> None:
        """Helper function to assert a value is equal to a given type"""

        self.assertEqual(type(first), _type)

    def assertRaisesSysExit(self, f: Callable[[], Any], code) -> None:
        """Helper function to assert that a sys error is raised"""

        with self.assertRaises(SystemExit) as cm:
            f()
        the_exception = cm.exception
        self.assertEqual(the_exception.code, code)

    def parse_args(self, args=None) -> argparse.Namespace:
        """Helper function that parses the arguments with the default arguments"""

        if args is None:
            args = []
        return ArgParser().parse_args(args)

    def test_without_src_folder(self) -> None:
        """
        Test that when no src arg folder is provided, the ArgumentParser
        throws a SystemExit exception
        """
        self.assertRaisesSysExit(lambda: self.parse_args([]), 2)

    def test_with_src_folder(self) -> None:
        """Test that nothing fails if a src folder is provided"""

        self.parse_args(self.default_args)
        self.assertTrue(True)

    def test_defaults(self) -> None:
        """Test that the default values are set correctly"""

        args = self.parse_args(self.default_args)

        self.assertEqual(args.dest, "./out")
        self.assertEqual(args.fps, 10)
        self.assertEqual(args.width, None)
        self.assertEqual(args.height, None)
        self.assertEqual(args.cxmin, None)
        self.assertEqual(args.cxmax, None)
        self.assertEqual(args.cymin, None)
        self.assertEqual(args.cymax, None)
        self.assertEqual(args.gray, False)
        self.assertEqual(args.silent, False)
        self.assertEqual(args.threads, 4)
        self.assertEqual(args.no_input, False)

    def test_types(self) -> None:
        """Test that the default types are set correctly"""

        args = self.parse_args(self.default_args)

        self.assertTypeEqual(args.src, str)
        self.assertTypeEqual(args.dest, str)
        self.assertTypeEqual(args.fps, int)
        self.assertTypeEqual(args.width, type(None))
        self.assertTypeEqual(args.height, type(None))
        self.assertTypeEqual(args.cxmin, type(None))
        self.assertTypeEqual(args.cxmax, type(None))
        self.assertTypeEqual(args.cymin, type(None))
        self.assertTypeEqual(args.cymax, type(None))
        self.assertTypeEqual(args.gray, bool)
        self.assertTypeEqual(args.silent, bool)
        self.assertTypeEqual(args.threads, int)
        self.assertTypeEqual(args.no_input, bool)

    def test_size_types(self) -> None:
        """Test that the by default None args, types are set correctly"""

        extra_args = [
            "--width",
            "100",
            "--height",
            "100",
            "--cxmin",
            "25",
            "--cxmax",
            "75",
            "--cymin",
            "25",
            "--cymax",
            "75",
        ]
        args = self.parse_args(self.default_args + extra_args)

        self.assertTypeEqual(args.width, int)
        self.assertTypeEqual(args.height, int)
        self.assertTypeEqual(args.cxmin, int)
        self.assertTypeEqual(args.cxmax, int)
        self.assertTypeEqual(args.cymin, int)
        self.assertTypeEqual(args.cymax, int)

    def test_gt_zero_validation(self) -> None:
        """Test the some arguments must be greater than zero"""

        arg_names = [
            "fps",
            "width",
            "height",
            "threads",
        ]

        for n in arg_names:
            self.assertRaisesSysExit(
                lambda: self.parse_args(self.default_args + [f"--{n}", "-1"]), 1
            )

        for n in arg_names:
            self.assertRaisesSysExit(
                lambda: self.parse_args(self.default_args + [f"--{n}", "0"]), 1
            )

    def test_positive_validation(self) -> None:
        """Test the some arguments must be positive"""

        arg_names = [
            "cxmin",
            "cxmax",
            "cymin",
            "cymax",
        ]

        for n in arg_names:
            self.assertRaisesSysExit(
                lambda: self.parse_args(self.default_args + [f"--{n}", "-1"]), 1
            )

        for n in arg_names:
            args = [f"--{n}", "0"]
            try:
                # Should not raise error
                self.parse_args(self.default_args + args)
                self.assertTrue(True)
            except SystemExit:
                self.assertEqual("", f"FAILED TEST with args: {args}")

    def get_crop_args(self, axis_repr: str) -> Tuple[List[str], List[str]]:
        """Helper function for getting all the cases for the the crop arguments"""

        w_or_h = "width" if axis_repr == "x" else "height"
        valid_args = [
            [f"--{w_or_h}", "100", f"--c{axis_repr}min", "0"],
            [f"--{w_or_h}", "100", f"--c{axis_repr}min", "50"],
            [f"--{w_or_h}", "100", f"--c{axis_repr}max", "100"],
            [
                f"--{w_or_h}",
                "100",
                f"--c{axis_repr}min",
                "0",
                f"--c{axis_repr}max",
                "50",
            ],
            [
                f"--{w_or_h}",
                "100",
                f"--c{axis_repr}min",
                "0",
                f"--c{axis_repr}max",
                "100",
            ],
            [
                f"--{w_or_h}",
                "100",
                f"--c{axis_repr}min",
                "50",
                f"--c{axis_repr}max",
                "100",
            ],
        ]

        invalid_args = [
            [f"--{w_or_h}", "100", f"--c{axis_repr}min", "100"],
            [f"--{w_or_h}", "100", f"--c{axis_repr}min", "150"],
            [f"--{w_or_h}", "100", f"--c{axis_repr}max", "0"],
            [f"--{w_or_h}", "100", f"--c{axis_repr}max", "150"],
            [
                f"--{w_or_h}",
                "100",
                f"--c{axis_repr}min",
                "50",
                f"--c{axis_repr}max",
                "50",
            ],
            [
                f"--{w_or_h}",
                "100",
                f"--c{axis_repr}min",
                "0",
                f"--c{axis_repr}max",
                "150",
            ],
        ]

        return valid_args, invalid_args

    def test_crop_x_validation(self) -> None:
        """Test invalid crop x arguments raise SystemExit"""

        d_args = self.default_args
        valid_args, invalid_args = self.get_crop_args("x")

        for a in valid_args:
            try:
                # Should not raise error
                self.parse_args(d_args + a)
                self.assertTrue(True)
            except SystemExit:
                self.assertEqual("", f"FAILED TEST with args: {a}")

        for a in invalid_args:
            self.assertRaisesSysExit(lambda: self.parse_args(d_args + a), 1)

    def test_crop_y_validation(self) -> None:
        """Test invalid crop y arguments raise SystemError"""

        d_args = self.default_args
        valid_args, invalid_args = self.get_crop_args("y")

        for a in valid_args:
            try:
                # Should not raise error
                self.parse_args(d_args + a)
                self.assertTrue(True)
            except SystemExit:
                self.assertEqual("", f"FAILED TEST with args: {a}")

        for a in invalid_args:
            self.assertRaisesSysExit(lambda: self.parse_args(d_args + a), 1)


if __name__ == "__main__":
    unittest.main()
