import rocket
import time
import string
import stage


def main():
    # Initialize the rocket
    Falcon_9 = rocket.Rocket(0, 15, 0,)
    #Initialize Stage(s)
    stage1 = stage.Stage(25600, 409500, 7607000, 2848)
    Falcon_9.attach_stage(stage1)
    #stage2 = stage.Stage(4000, 92670, 981000, 280)
    #Falcon_9.attach_stage(stage2)
    dt = 0.1



    
    print(Falcon_9.stages)
    print(Falcon_9.get_telemetry())
    

if __name__ == "__main__":
    main()