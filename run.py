from pathlib import Path
import sys

from variables import IMAGE_NAME, MOUNT_IMAGE_DEST, MOUNT_IMAGE_SRC
from utils.arg_parser import ArgParser
from utils.command_utils import check_docker_installed, run_cmd


def main() -> None:
    """Main function to run the docker container with the arguments"""

    check_docker_installed()
    args = ArgParser().parse_args()
    # Remove the file name arg and replace it with the image src mount
    new_args = sys.argv[1:].copy()
    new_args[new_args.index("-s") + 1] = MOUNT_IMAGE_SRC

    # Run docker docker (image='IMAGE_NAME') and mount 2 volumes
    # The first volume allows the container to read the src folder
    # The second volume allows the container to write the dest folder
    vol1_mount = f"{Path(args.src).absolute().as_posix()}:{MOUNT_IMAGE_SRC}"
    vol2_mount = f"{Path(args.dest).absolute().as_posix()}:{MOUNT_IMAGE_DEST}"
    full_cmd = (
        f"docker run {'-it' if not args.no_input else ''} --rm "
        f"-v {vol1_mount} -v {vol2_mount} {IMAGE_NAME} "
    ) + " ".join(new_args)
    run_cmd(full_cmd)


if __name__ == "__main__":
    main()
