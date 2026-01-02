import time
import rocket

def main():
    # Initialize the rocket
    my_rocket = rocket.Rocket()
    dt =  0.1  # Time step in seconds
    t = 0  # Initial time
    escape_altitude = 10000  # Escape altitude in meters

    


    while my_rocket.altitude < escape_altitude:
        # Simulate the rocket's motion for one time step
        my_rocket.update(dt)
        t += dt
        telemetry = my_rocket.get_telemetry()
        print(f"\r| Time: {t:.2f}s{telemetry}", end="", flush=True)
        time.sleep(dt)  # Wait for one second before the next iteration
    print("\n")
    print("SPACE REACHED!!!")


if __name__ == "__main__":
    main()