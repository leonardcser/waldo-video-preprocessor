import unittest
from utils.arg_parser import ArgParser


class TestArguments(unittest.TestCase):
    """Tests for command line arguments"""

    def assertTypeEqual(self, first, _type):
        """Helper function to assert a value is equal to a given type"""

        self.assertEqual(type(first), _type)

    def test_without_src_folder(self):
        """
        Test that when no src arg folder is provided, the ArgumentParser
        throws a SystemExit exception
        """
        args = []

        with self.assertRaises(SystemExit) as cm:
            ArgParser().parse_args(args)

        the_exception = cm.exception
        self.assertEqual(the_exception.code, 2)

    def test_with_src_folder(self):
        """Test that nothing fails if a src folder is provided"""

        args = ["-s", "./test"]
        ArgParser().parse_args(args)

        self.assertTrue(True)

    def test_defaults(self):
        """Test that the default values are set correctly"""

        args = ["-s", "./test"]
        args = ArgParser().parse_args(args)

        self.assertEqual(args.dest, "./out")
        self.assertEqual(args.fps, 10)
        self.assertEqual(args.width, None)
        self.assertEqual(args.height, None)
        self.assertEqual(args.gray, False)
        self.assertEqual(args.silent, False)
        self.assertEqual(args.threads, 4)
        self.assertEqual(args.no_input, False)

    def test_types(self):
        """Test that the default types are set correctly"""

        args = ["-s", "./test"]
        args = ArgParser().parse_args(args)

        self.assertTypeEqual(args.src, str)
        self.assertTypeEqual(args.dest, str)
        self.assertTypeEqual(args.fps, int)
        self.assertTypeEqual(args.width, type(None))
        self.assertTypeEqual(args.height, type(None))
        self.assertTypeEqual(args.gray, bool)
        self.assertTypeEqual(args.silent, bool)
        self.assertTypeEqual(args.threads, int)
        self.assertTypeEqual(args.no_input, bool)

    def test_size_types(self):
        """Test that the width and height types are set correctly"""

        args = ["-s", "./test", "--width", "100", "--height", "100"]
        args = ArgParser().parse_args(args)

        self.assertTypeEqual(args.width, int)
        self.assertTypeEqual(args.height, int)


if __name__ == "__main__":
    unittest.main()
