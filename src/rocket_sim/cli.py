import time
from rocket_sim.models import rocket
from rocket_sim.config import falcon9_config
from rocket_sim.config.sim_config import SimConfig
from rocket_sim.telemetry.console import format_telemetry
from rocket_sim.telemetry.exporters import recorder
from rocket_sim.utils import get_time_str, run_mode, should_stop, phase_tag
from scripts.plot_run import plot_csv_data

def main():
    # Runtime settings
    fast_mode, stop_at = run_mode()
    p_tag = phase_tag(stop_at)
    csv_path = recorder.generate_path(p_tag)
    data_step = 0

    #Time
    t = 0  # Initial time 

    # Initialize the rocket
    Falcon_9 = rocket.Rocket(falcon9_config.falcon9_rocket, y=15.0)
    # Initialize Sim
    Falcon_9.sim_running = True
    
    while Falcon_9.sim_running:

        # Simulate the rocket's motion for one time step
        Falcon_9.update(SimConfig.dt)
        if should_stop(stop_at, Falcon_9):
            Falcon_9.sim_running = False

        t += SimConfig.dt
        data_step += 1
        time_str = get_time_str(t)
        
        # Prints updated telemetry on one line
        print("\033c", end="")  # clear screen (portable)
        print(f"Time: {time_str}s")
        print(format_telemetry(Falcon_9.get_telemetry()))
        
        if not fast_mode:
            time.sleep(SimConfig.dt)  # Wait before the next iteration
        if data_step % 100 == 0:
            recorder.record_telemetry(Falcon_9.get_telemetry(), csv_path)

    print("\n")
    recorder.record_telemetry(Falcon_9.get_telemetry(), csv_path)
    print(f"Sim completed in {time_str}")
    plot_csv_data(p_tag)


if __name__ == "__main__":
    main()