from utils.command_utils import check_docker_installed, run_cmd
from variables import IMAGE_NAME


def main() -> None:
    """Main function to build the docker image"""

    check_docker_installed()
    run_cmd(f"docker build -f ./docker/Dockerfile -t {IMAGE_NAME} .")


if __name__ == "__main__":
    main()
