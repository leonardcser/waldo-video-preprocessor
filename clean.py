from utils.command_utils import check_docker_installed, run_cmd
from variables import IMAGE_NAME
from utils.logger import logger


def main() -> None:
    """Main function to remove the docker image"""

    check_docker_installed()
    user_input = input(
        (
            "[INPUT] Are you sure you want to delete the container? "
            "You can always rebuild it. (Y/n): "
        )
    )
    if user_input.lower() == "y":
        run_cmd(f"docker rmi $(docker images '{IMAGE_NAME}' -a -q) --force")
        logger.success(f"Sucessfully removed '{IMAGE_NAME}' image!")
    else:
        logger.info("Cancelled.")


if __name__ == "__main__":
    main()
