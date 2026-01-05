import time
import rocket, stage

def main():
    # Initialize the rocket

    Falcon_9 = rocket.Rocket(0, 15, 0)

    #Initialize Stage(s)

    stage1 = stage.Stage(25600, 409500, 7607000, 2848)
    Falcon_9.attach_stage(stage1)
    stage2 = stage.Stage(4000, 92670, 981000, 280)
    Falcon_9.attach_stage(stage2)
    stage_one_seperation = 80000  # Escape altitude in meters

    #Time
     
    dt =  0.1  # Time step in seconds
    t = 0  # Initial time
    

    # Launch count down. For fun!
    cd = 3
    while cd > 0:
            print(f"Launch in t-minus: {cd:.2f}s\r", end="", flush=True)
            cd -= dt
            time.sleep(dt)

    print("\nLaunch!!")
    time.sleep(.5)
    
    while Falcon_9.altitude < stage_one_seperation:
  
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
        print(f"\r| Time: {time_str}s {telemetry}", end="", flush=True)
        
        time.sleep(dt)  # Wait for one second before the next iteration
    print("\n")
    print("SPACE REACHED!!!")


if __name__ == "__main__":
    main()