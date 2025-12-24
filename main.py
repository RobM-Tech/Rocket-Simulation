import time
import rocket

def main():
    # Initialize the rocket
    my_rocket = rocket.Rocket(velocity=0, altitude=0, acceleration=9.81)
    dt =  0.1  # Time step in seconds
    t = 0  # Initial time
    escape_altitude = 10000  # Escape altitude in meters

    


    while my_rocket.altitude < escape_altitude:
        # Simulate the rocket's motion for one time step
        my_rocket.update(dt)
        t += dt
        telemetry = my_rocket.get_telemetry()
        print(f"\rTime: {t:.2f}s | Velocity: {telemetry["velocity"]:.2f} m/s | Altitude: {telemetry["altitude"]:.2f} m | Acceleration: {telemetry["acceleration"]:.2f} m/s^2", end="", flush=True)
        time.sleep(dt)  # Wait for one second before the next iteration
    print("\n")
    print("SPACE REACHED!!!")


if __name__ == "__main__":
    main()