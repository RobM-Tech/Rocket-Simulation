import argparse
import time
from rocket_sim.models.stage import stage_state

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


def run_mode():
    parser = argparse.ArgumentParser()

    parser.add_argument('--fast', 
                        action='store_true', 
                        help='Enable fast CLI mode for faster overhead runtime')

    parser.add_argument('--until',
                    choices=["MECO", "SECO", "FULL"],
                    type=str.upper,
                    default="FULL",
                    help='Sets stop point for sim, default is full run.')

    args = parser.parse_args()

    return args.fast, args.until


def should_stop(stop_at, rkt):
    if stop_at == "FULL":
        return False
    
    if stop_at == "MECO" and rkt.current_stage.state == stage_state.MECO:
        return True
    
    if stop_at == "SECO" and rkt.current_stage.state == stage_state.SECO:
        return True
    
    return False


def phase_tag(stop_at):
    if stop_at == "MECO":
        tag = "_MECO"
    elif stop_at == "SECO":
        tag = "_SECO"
    elif stop_at == "FULL":
        tag = "_FULL"
    else:
        tag = "_FULL"

    return tag