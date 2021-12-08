import concurrent.futures
from pathlib import Path
from utils.arg_parser import ArgParser
from utils.logger import logger
from processing.io_video_manager import IOVideoManager
from processing.video_preprocessor import VPOptions, VideoPreprocessor


def main() -> None:
    """Main function that runs the threaded video processing"""

    args = ArgParser().parse_args()
    vp_opts = VPOptions(
        fps=args.fps,
        width=args.width,
        height=args.height,
        cxmin=args.cxmin,
        cxmax=args.cxmax,
        cymin=args.cymin,
        cymax=args.cymax,
        gray=args.gray,
        silent=args.silent,
    )

    def worker(video_path_obj: Path, vm: IOVideoManager) -> None:
        """Worker function that processes 1 video file"""
        try:
            pp = VideoPreprocessor(
                vm=vm,
                video_path_obj=video_path_obj,
                dest=args.dest,
                opts=vp_opts,
            )
            pp.process()
        except Exception as e:
            logger.error(e, print_exc=True)
            raise e

    vm = IOVideoManager(
        src_folder=Path(args.src), dest_folder=Path(args.dest), silent=args.silent
    )
    valid_paths = vm.get_video_paths()

    if not args.no_input:
        input("[INPUT] Press enter to confirm...")

    # Creating a thread pool to process each file individually and asynchronously
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.threads) as executor:
        for p in valid_paths:
            executor.submit(worker, p, vm)
            # Delete thead from the queue so when the main thread finishes, all the
            # created threads are killed
            del concurrent.futures.thread._threads_queues[list(executor._threads)[0]]


if __name__ == "__main__":
    main()
