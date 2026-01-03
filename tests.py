import rocket
import time


def main():
    # Initialize the rocket
    Falcon_9 = rocket.Rocket(0, 15, 0,)
    #Initialize Stage(s)
    stage1 = rocket.Stage(31300, 502170, 7607000)
    Falcon_9.attach_stage(stage1)
    dt = 0.1

    Falcon_9.update(dt)
    print(Falcon_9.get_telemetry())
    #for stage in Falcon_9.stages:
     #   stage.active = True
      #  print(Falcon_9.calc_acceleration())

if __name__ == "__main__":
    main()