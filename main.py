import time
import rocket

def main():
    # Initialize the rocket
    Falcon_9 = rocket.Rocket(0, 15, 0)
    #Initialize Stage(s)
    stage1 = rocket.Stage(31300, 502170, 7607000)
    Falcon_9.attach_stage(stage1)


    dt =  0.1  # Time step in seconds
    t = 0  # Initial time
    escape_altitude = 80000  # Escape altitude in meters

    '''cd = 10
    while cd > 0:
            print(f"\rLaunch in t-minus: {cd:.1f}s", end="", flush=True)
            cd -= 1
            time.sleep(1)'''

    while Falcon_9.altitude < escape_altitude:
        # Simulate the rocket's motion for one time step
        Falcon_9.update(dt)
        t += dt

        telemetry = Falcon_9.get_telemetry()
        print(f"\r| Time: {t:.2f}s{telemetry}", end="", flush=True)
        time.sleep(dt)  # Wait for one second before the next iteration
    print("\n")
    print("SPACE REACHED!!!")


if __name__ == "__main__":
    main()