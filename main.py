import time
import rocket, stage

def main():
    # Initialize the rocket

    Falcon_9 = rocket.Rocket(y=15.0, ref_area=10.52)

    #Initialize Stage(s)

    stage1 = stage.Stage(dry_mass=25600, fuel_mass=409500, thrust=7607000, burn_rate=2848)
    Falcon_9.attach_stage(stage1)
    stage2 = stage.Stage(dry_mass=4000, fuel_mass=92670, thrust=981000, burn_rate=280)
    Falcon_9.attach_stage(stage2)
    stage_one_seperation = 200000  # Escape altitude in meters

    #Time
     
    dt =  0.05  # Time step in seconds
    t = 0  # Initial time
    

    # Launch count down. For fun!
    cd = 3
    while cd > 0:
            print(f"Launch in t-minus: {cd:.2f}s\r", end="", flush=True)
            cd -= dt
            time.sleep(dt)

    print("\nLaunch!!")
    time.sleep(.5)
    
    while Falcon_9.y < stage_one_seperation:
  
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
        

        
        time.sleep(dt)  # Wait for one second before the next iteration
    print("\n")
    print("SPACE REACHED!!!")


if __name__ == "__main__":
    main()