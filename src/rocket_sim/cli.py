import time
from rocket_sim.models import rocket
from rocket_sim.config import falcon9_config

def main():
    # Initialize the rocket

    Falcon_9 = rocket.Rocket(falcon9_config.falcon9_rocket, y=15.0)

    orbit_velocity = 9000  # Escape altitude in meters

    #Time
    MAX_SIM_TIME = 3600
    dt =  0.01  # Time step in seconds
    t = 0  # Initial time 
    

    # Launch count down. For fun!
    cd = 1
    
    while cd > 0:
            print(f"Launch in t-minus: {cd:.2f}s\r", end="", flush=True)
            cd -= dt
            time.sleep(dt)
            if cd == 0:
                print("\nLaunch!!")
                time.sleep(.5)
    Falcon_9.sim_running = True
    
    while Falcon_9.sim_running:

        # Simulate the rocket's motion for one time step
        Falcon_9.update(dt)
        t += dt
        #HH:MM:SS.ss setup
        hh = int(t // 3600)
        mm = int((t % 3600) // 60)
        ss = t % 60

        time_str = (
                    f"{hh:02d}:"
                    f"{mm:02d}:"
                    f"{ss:05.2f}"
                    )
        
        telemetry = Falcon_9.get_telemetry()
        #prints updated telemetry on one line
        
        print("\033c", end="")  # clear screen (portable)
        print(f"Time: {time_str}s")
        print(telemetry)
        
        time.sleep(dt)  # Wait before the next iteration
    print("\n")
    print("SPACE REACHED!!!")


if __name__ == "__main__":
    main()