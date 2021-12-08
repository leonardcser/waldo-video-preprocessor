import os
import subprocess
import sys


def check_docker_installed() -> None:
    """
    Util function that checks if docker is installed by running
    the docker command and checking whether the return code is 0.
    """
    code = run_cmd("docker", True)
    if code != 0:
        readme_path = os.path.join(os.getcwd(), "README.md")
        print(
            (
                "[ERROR]: Docker is not installed. You can find how to install "
                f"it in the README ({readme_path})"
            ),
            file=sys.stderr,
        )
        exit(1)


def run_cmd(cmd: str, slient=False) -> int:
    """
    Util function that executes a shell command, prints the command to the console
    and returns the return code.
    """
    slient_args = {}
    if not slient:
        print(f"[INFO]: Running command '{cmd}'\n")
    else:
        slient_args = {"stdout": subprocess.DEVNULL, "stderr": subprocess.DEVNULL}

    p = subprocess.Popen(cmd, shell=True, **slient_args)
    p.wait()
    return p.returncode
