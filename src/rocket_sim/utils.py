import argparse
import time

def get_time_str(t):
    #HH:MM:SS.ss setup
    hh = int(t // 3600)
    mm = int((t % 3600) // 60)
    ss = t % 60

    time_str = (
                f"{hh:02d}:"
                f"{mm:02d}:"
                f"{ss:05.2f}"
                )

    return time_str


def fast_mode_argparse(Fast_mode: bool):
    parser = argparse.ArgumentParser()

    parser.add_argument('--fast', 
                        action='store_true', 
                        help='Enable fast CLI mode for faster overhead runtime')

    args = parser.parse_args()

    return args.fast
