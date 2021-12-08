import unittest
import os
import shutil
import cv2

from utils.command_utils import run_cmd
from variables import IS_DOCKER


class TestProcessing(unittest.TestCase):
    """Tests for processing videos"""

    def setUp(self):
        # TODO: Update so that we can test creating files on github actions ci
        self.ON_GITHUB_CI = os.environ.get("ON_GITHUB_CI", 0)
        self.src_dir = os.path.join(os.getcwd(), "tests/videos")
        self.out_dir = os.path.join(os.getcwd(), "tests/out")
        if IS_DOCKER:
            self.default_cmd = (
                f"python3 run.py -s '{self.src_dir}' -d '{self.out_dir}' -ni"
            )
        else:
            self.default_cmd = (
                f"python3 main.py -s '{self.src_dir}' -d '{self.out_dir}' -ni"
            )
        self.blank_2s_save_path = os.path.join(self.out_dir, "blank_2s_30fps_mp4")
        self.blank_2s_fps = 30
        self.blank_2s_w = 1920
        self.blank_2s_h = 1080

    def tearDown(self):
        # We delete the files that are created by the processing
        if os.path.isdir(self.out_dir):
            shutil.rmtree(self.out_dir)

    def test_1_fps(self):
        """Test for 1 requested fps"""

        if not self.ON_GITHUB_CI:
            run_cmd(self.default_cmd + " -f 1")
            # Because 30fps * 2s and requesting 1fps * 2s == 2 frames
            self.assertEqual(len(os.listdir(self.blank_2s_save_path)), 2)

    def test_10_fps(self):
        """Test a general case for a requested 10 fps"""

        if not self.ON_GITHUB_CI:
            run_cmd(self.default_cmd + " -f 10")
            self.assertEqual(len(os.listdir(self.blank_2s_save_path)), 20)

    def test_100_fps(self):
        """
        Test that when requested fps > video fps,
        requested fps == video fps
        """
        if not self.ON_GITHUB_CI:
            run_cmd(self.default_cmd + " -f 100")
            self.assertEqual(len(os.listdir(self.blank_2s_save_path)), 60)

    def test_no_grayscale(self):
        """
        Test that when no grayscale in args, the frames are not converted
        to grayscale
        """
        if not self.ON_GITHUB_CI:
            run_cmd(self.default_cmd + " -f 1")
            for p in os.listdir(self.blank_2s_save_path):
                frame = cv2.imread(os.path.join(self.blank_2s_save_path, p))
                # We check if the three rgb values are equal (<=> grayscrale)
                # R=frame[0][0][0], G=frame[0][0][1], B=frame[0][0][2]
                self.assertFalse(frame[0][0][0] == frame[0][0][1] == frame[0][0][2])

    def test_grayscale(self):
        """
        Test that when grayscale in args, the frames are converted
        to grayscale
        """
        if not self.ON_GITHUB_CI:
            run_cmd(self.default_cmd + " -f 1 -g")
            for p in os.listdir(self.blank_2s_save_path):
                frame = cv2.imread(os.path.join(self.blank_2s_save_path, p))
                # Same here as function 'test_no_grayscale'
                self.assertTrue(frame[0][0][0] == frame[0][0][1] == frame[0][0][2])

    def test_no_resize(self):
        """
        Test that when no width or height in args, the frames are not
        resized
        """
        if not self.ON_GITHUB_CI:
            run_cmd(self.default_cmd + " -f 1")
            for p in os.listdir(self.blank_2s_save_path):
                frame = cv2.imread(os.path.join(self.blank_2s_save_path, p))
                self.assertEqual(frame.shape[0], self.blank_2s_h)
                self.assertEqual(frame.shape[1], self.blank_2s_w)

    def test_resize_width(self):
        """
        Test that when width in args, only the width of the frame is
        resized
        """
        if not self.ON_GITHUB_CI:
            run_cmd(self.default_cmd + " -f 1 --width 100")
            for p in os.listdir(self.blank_2s_save_path):
                frame = cv2.imread(os.path.join(self.blank_2s_save_path, p))
                self.assertEqual(frame.shape[0], self.blank_2s_h)
                self.assertEqual(frame.shape[1], 100)

    def test_resize_height(self):
        """
        Test that when height in args, only the height of the frame is
        resized
        """
        if not self.ON_GITHUB_CI:
            run_cmd(self.default_cmd + " -f 1 --height 100")
            for p in os.listdir(self.blank_2s_save_path):
                frame = cv2.imread(os.path.join(self.blank_2s_save_path, p))
                self.assertEqual(frame.shape[0], 100)
                self.assertEqual(frame.shape[1], self.blank_2s_w)

    def test_resize_both(self):
        """
        Test that when width and height in args, both the width and the height
        of the frame are resized
        """
        if not self.ON_GITHUB_CI:
            run_cmd(self.default_cmd + " -f 1 --width 100 --height 100")
            for p in os.listdir(self.blank_2s_save_path):
                frame = cv2.imread(os.path.join(self.blank_2s_save_path, p))
                self.assertEqual(frame.shape[0], 100)
                self.assertEqual(frame.shape[1], 100)

    def test_crop_x(self):
        """
        Test that when width and height in args, both the width and the height
        of the frame are resized
        """
        if not self.ON_GITHUB_CI:
            run_cmd(self.default_cmd + " -f 1 --width 100 --height 100")
            for p in os.listdir(self.blank_2s_save_path):
                frame = cv2.imread(os.path.join(self.blank_2s_save_path, p))
                self.assertEqual(frame.shape[0], 100)
                self.assertEqual(frame.shape[1], 100)


if __name__ == "__main__":
    unittest.main()
