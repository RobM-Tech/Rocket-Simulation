import physics, time, math
from stage import stage_state, Stage, empty_stage
from enum import Enum

class rocket_state(Enum):
    IDLE = 1
    LAUNCH = 2
    PITCH_INITIATION = 3
    ASCENT_BURN = 4
    STAGE1_SEPARATION = 5
    COAST = 6
    STAGE2_IGNITION = 7
    STAGE2_ASCENT = 8
    ORBIT_COAST = 9
    

class Rocket:
    def __init__(self, x=0.0, y=0.0, vx=0.0, vy=0.0, ax=0.0, ay=0.0, ref_area=0.0, payload_weight=0.0):
        
        # ────────────────────────────────────────────────
        #  Simulation control & book-keeping
        # ────────────────────────────────────────────────
        self.state          = rocket_state.IDLE
        self.t              = 0.0
        self.sim_running    = False
        self.orbit_initialized = False
        self.max_Q          = 0.0
        self.max_G          = 3.5 * 9.81

        # ────────────────────────────────────────────────
        #  Target & orbit parameters
        # ────────────────────────────────────────────────
        self.target_orbit_altitude = 290_000          # m
        self.target_r       = physics.R_e + self.target_orbit_altitude

        # ────────────────────────────────────────────────
        #  State — kinematics
        # ────────────────────────────────────────────────
        self.x              = x
        self.y              = y
        self.vx             = vx
        self.vy             = vy
        self.ax             = ax
        self.ay             = ay
        self.total_velocity = 0.0
        self.v_r            = 0.0                   # radial velocity component

        # ────────────────────────────────────────────────
        #  Attitude & guidance
        # ────────────────────────────────────────────────
        self.pitch_angle        = math.radians(0.0)
        self.command_pitch      = math.radians(8.0)
        self.command_pitch_done = False
        self.last_pitch         = 0.0               # possibly unused → candidate for removal

        # ────────────────────────────────────────────────
        #  Staging & stage references
        # ────────────────────────────────────────────────
        self.stages         = []
        self.current_stage  = None
        self.next_stage     = None
        self.time_since_sep = 0.0
        self.MECO_delay        = 3.0     # s
        self.s2_ignition_delay = 3.0     # s   (real Falcon 9 is ~10–12 s — consider tuning)

        self.max_stage2_Vy  = 0.0

        # ────────────────────────────────────────────────
        #  Tuning parameters — Stage 1
        # ────────────────────────────────────────────────
        self.s1_ramp_dur          = 110      # s
        self.s1_ramp_delay        = 5.0      # s
        self.s1_min_vel           = 2350     # m/s
        self.s1_sep_min_alt       = 65_000   # m
        self.s1_nominal_burn_time = 160      # s
        self.s1_start_pitch       = self.command_pitch
        self.s1_end_pitch         = math.radians(70)
        self.s1_throttle_dwn_time = 60       # s
        self.s1_throttle_up_time  = 90       # s

        # ────────────────────────────────────────────────
        #  Tuning parameters — throttling
        # ────────────────────────────────────────────────
        self.throttle_rate_limit    = 0.05    # fraction per second
        self.launch_throttle        = 0.8
        self.max_q_throttle         = 0.7
        self.target_thrust_fraction = 1.0     # renamed for clarity (was target_thrust_friction)

        # ────────────────────────────────────────────────
        #  Tuning parameters — Stage 2
        # ────────────────────────────────────────────────
        self.s2_ramp_dur          = 200      # s
        self.s2_ramp_delay        = 60.0     # s
        self.s2_nominal_burn_time = 360      # s
        self.S2_orbital_velocity  = 7650     # m/s     ← consider renaming → s2_target_velocity
        self.s2_start_pitch       = math.radians(80)
        self.s2_end_pitch         = math.radians(90)

        # ────────────────────────────────────────────────
        #  Payload & ejectables
        # ────────────────────────────────────────────────
        self.reference_area     = ref_area            # m² (consider rename → drag_reference_area)
        self.payload_weight     = payload_weight      # kg
        self.fairing_weight     = 1750                # kg
        self.fairing_jettisoned = False

        # ────────────────────────────────────────────────
        #  Propulsion state
        # ────────────────────────────────────────────────
        self.current_thrust = 0.0



    @property
    def total_mass(self):
        stage_mass = sum(stage.calc_total_mass() for stage in self.stages if stage.is_attached() or stage.is_ignited() or stage.is_throttled())
        return stage_mass + self.payload_weight
    

    def __repr__(self):
        return f"Rocket(State: {self.state.name}, Current Stage: {self.current_stage.state.name}, Next Stage: {self.next_stage.state.name})"

    #Main loop
    def update(self, dt):
        self.t += dt
        #Update rocket state and stage
        self.set_rocket_state(dt)
        self.current_stage.update(dt)
        
        
        #Compute thrust based on current pitch

        # Thrust throttling
        target_fraction = 0.0

        if self.current_stage:
            if 0 < self.t < 60:
                if self.current_stage.is_ignited() and not self.current_stage.is_burned_out():
                    target_fraction = self.launch_throttle #throttle down to preserve energy
                    self.current_stage.throttle = self.launch_throttle
                    
            elif self.current_stage.is_throttled() and not self.current_stage.is_burned_out():
                target_fraction = self.max_q_throttle    #throttle down for max Q
                self.current_stage.throttle = self.max_q_throttle

            elif self.current_stage.is_ignited() and not self.current_stage.is_burned_out():
                target_fraction = 1.00  #max thrust
                self.current_stage.throttle = 1.0
            else:
                target_fraction = 0.0
        else:
            target_fraction = 0.0

        # Rate-limit the change
        max_change = self.throttle_rate_limit * dt
        current_fraction = self.current_thrust / self.current_stage.nominal_thrust if self.current_thrust > 0 else 1.0

        delta = target_fraction - current_fraction
        clamped_delta = max(min(delta, max_change), -max_change)

        new_fraction = current_fraction + clamped_delta

        self.current_thrust = self.current_stage.nominal_thrust * new_fraction
        self.target_thrust_fraction = target_fraction  # optional tracking
        

        T_x, T_y = physics.calc_thrust(self.current_thrust, self.pitch_angle)

        #Compute accelerations
        self.ay, self.ax = physics.acceleration(self, T_y, T_x)
        
        #Update radial velocity (after acceleration update)
        self.v_r = physics.radial_velocity(self.y, self.x, self.vx, self.vy)

        #Update velocities
        self.vy += self.ay * dt #Update velocity based on acceleration and time step
        self.vx += self.ax * dt

        # velocity Verlet step 1
        vx_half = self.vx + 0.5 * self.ax * dt
        vy_half = self.vy + 0.5 * self.ay * dt
        
        #Update positions
        self.x += vx_half * dt
        self.y += vy_half * dt

        if self.y < 0:
            print("CRASH")
            return
        
        # recompute acceleration at new position
        T_y = self.current_thrust * math.cos(self.pitch_angle)   # vertical
        T_x = self.current_thrust * math.sin(self.pitch_angle)   # horizontal
        self.ay, self.ax = physics.acceleration(self, T_y, T_x)

        # velocity Verlet step 2
        self.vx = vx_half + 0.5 * self.ax * dt
        self.vy = vy_half + 0.5 * self.ay * dt
               

        #Update total velocity
        self.total_velocity = physics.total_velocity(self.vx, self.vy)


        #Debug exit condition block, change to focus stop points to check telemetry
        if (
            self.state == rocket_state.STAGE1_SEPARATION
            or self.current_stage.state == stage_state.MECO
            or self.current_stage.state == stage_state.BURNED_OUT
            or self.t >= 300
        ):
            self.sim_running = False
        '''elif self.is_stage2_ascent():
            if self.vy <= 0:
                self.sim_running = False'''

       
            
        
    
    #Receive telemetry data and format in to readable data
    def get_telemetry(self):
        flight_path_angle = math.atan2(self.vy, self.vx)
        t_mass = self.total_mass
        
        pitch_deg = math.degrees(self.pitch_angle)
        current_Q = physics.dynamic_pressure(vy=self.vy, y=self.y) #Pa
        
        if current_Q > self.max_Q:
            self.max_Q = current_Q
        if self.max_Q > current_Q:
            self.sim_running = False
        

        V_r = abs(self.v_r)
        
        fuel = 0.0
        if self.current_stage is not None:
            fuel = self.current_stage.fuel_mass
            burn_rate = self.current_stage.current_burn_rate

        if self.state == rocket_state.IDLE:
            self.vy = 0
            self.ay = 0
        Fg_y, Fg_x = physics.gravity_force(self.total_mass, self.y, self.x)
        Fg_y = Fg_y / 1000
        Fg_x = Fg_x / 1000

        #For DEBUGGING
        mu = physics.G * physics.M_e
        r = math.sqrt(self.x**2 + (physics.R_e + self.y)**2)
        v2 = self.total_velocity**2
        epsilon = v2 / 2 - mu / r
        if epsilon >= 0:
            apo_str = "Hyperbolic escape"
        else:
            a = -mu / (2 * epsilon)
            h_sq = (self.x * self.vy - (physics.R_e + self.y) * self.vx)**2  # ang mom squared
            e_term = 1 + (2 * epsilon * h_sq / mu**2)
            e = math.sqrt(max(e_term, 0))  # clamp to avoid domain error
            r_a = a * (1 + e)
            apo_alt = r_a - physics.R_e
            apo_str = f"{apo_alt / 1000:.0f} km"
            if apo_alt > 800000:
                self.sim_running = False

        telemetry = (
            f"KINEMATICS:\n"
            f"V_total:       {self.total_velocity:10.2f} m/s²\n"
            f"y:             {self.y:10.2f} m\n"
            f"Vy:            {self.vy:10.2f} m/s\n"
            f"Ay:            {self.ay:10.2f} m/s²\n"
            f"x:             {self.x:10.2f} m\n"
            f"Vx:            {self.vx:10.2f} m/s\n"
            f"Ax:            {self.ax:10.2f} m/s²\n"
            f"Pitch:         {pitch_deg:10.2f}\n"
            f"Flight_path_a  {flight_path_angle:10.2f}\n"
            f"Fg_y:          {Fg_y:10.2f} kN\n"
            f"Fg_x:          {Fg_x:10.2f} kN\n"
            f"\n"
            f"AERODYNAMICS:\n"
            f"Q:             {current_Q:10.2f} Pa\n"
            f"max_Q:         {self.max_Q:10.2f} Pa\n"
            f"\n"
            f"PROPULSION / MASS:\n"
            f"Thrust:        {self.current_thrust:10.0f} N\n"
            f"Fuel:          {fuel:10.2f} kg\n"
            f"Burn_r         {burn_rate:10.2f} kg/s\n"
            f"Mass:          {t_mass:10.2f} kg\n"
            f"\n"
            f"Guidence:\n"
            f"V_r:           {V_r:10.2f}\n"
            f"r              {r:10.2f}\n"
            f"\n"
            f"FLIGHT STATE:\n"
            f"Rocket State:  {self.state}\n"
            f"Current Stage: {self.current_stage.state if self.current_stage else 'None'}\n"
            f"Next Stage:    {self.next_stage.state if self.next_stage else 'None'}\n"
            f"\n"
            f"Est apoapsis: {apo_str}\n"
            f"T:            {self.t:10.2f}"
        )

        return telemetry


    
    #Rocket state machine

    def set_rocket_state(self, dt):
        match self.state:
            case rocket_state.IDLE:
                self.set_current_stage()
                self.state = rocket_state.LAUNCH


            case rocket_state.LAUNCH:
                self.current_stage.state = stage_state.IGNITED
                if self.y > 75:
                    self.state = rocket_state.PITCH_INITIATION
            

            case rocket_state.PITCH_INITIATION:
                if self.pitch_angle > self.command_pitch:
                    self.pitch_angle -= math.radians(0.2)  # increment small step
                else:
                    self.command_pitch_done = True
                    
                if self.command_pitch_done:
                    self.state = rocket_state.ASCENT_BURN
                

            case rocket_state.ASCENT_BURN:
                
                if self.t > self.s1_throttle_dwn_time:
                    self.current_stage.state = stage_state.THROTTLE_DOWN

                if self.t > self.s1_throttle_up_time:
                    self.current_stage.state = stage_state.IGNITED

                #Time based pitch
                #Linear interpolation in time
                time_since_launch = self.t
                if time_since_launch > self.s1_ramp_delay:
                    k = min((time_since_launch - self.s1_ramp_delay) / self.s1_ramp_dur, 1)
                    target_pitch = self.s1_start_pitch + k * (self.s1_end_pitch - self.s1_start_pitch)
                else:
                    target_pitch = self.command_pitch

                if self.current_stage.is_throttled():
                    throttle_ratio = self.current_stage.thrust / self.current_stage.nominal_thrust
                    # At 80% thrust → ~5° bias toward horizontal
                    pitch_bias = math.radians(5) * (1 - throttle_ratio)
                    target_pitch -= pitch_bias

                # Smooth approach (avoid jumps)
                max_delta = math.radians(0.5)  # max pitch change per timestep
                delta_pitch = target_pitch - self.pitch_angle
                delta_pitch = max(min(delta_pitch, max_delta), -max_delta)
                self.pitch_angle += delta_pitch
                
            

                # Stage 1 separation trigger
                if (
                    (
                    self.y >= self.s1_sep_min_alt
                    and self.total_velocity >= self.s1_min_vel
                    )
                    or self.t > self.s1_nominal_burn_time
                ):

                    self.state = rocket_state.STAGE1_SEPARATION
                    self.current_stage.state = stage_state.MECO
                
                elif self.t > self.s1_nominal_burn_time + 20:
                    self.state = rocket_state.STAGE1_SEPARATION
                    self.current_stage.state = stage_state.MECO

            case rocket_state.STAGE1_SEPARATION:
                self.time_since_sep += dt
                if self.current_stage.is_meco():
                    
                    if self.time_since_sep >= self.MECO_delay:
                        self.detach_stage(self.current_stage)
                        self.current_stage = self.next_stage
                        self.next_stage = empty_stage()
                        self.next_stage.state = stage_state.EMPTY
                        self.state = rocket_state.COAST


            case rocket_state.COAST:
                self.time_since_sep += dt
                if self.time_since_sep >= self.s2_ignition_delay:
                    self.state = rocket_state.STAGE2_IGNITION


            case rocket_state.STAGE2_IGNITION:
                self.current_stage.state = stage_state.IGNITED
                self.time_s2_Ignition = self.t
                if self.vy > self.max_stage2_Vy:
                    self.max_stage2_Vy = self.vy
                    
                elif self.vy < self.max_stage2_Vy:
                    self.state = rocket_state.STAGE2_ASCENT


            case rocket_state.STAGE2_ASCENT:
                # Fairing jettison
                if not self.fairing_jettisoned and self.y >= 110000:
                    self.payload_weight -= self.fairing_weight
                    self.fairing_jettisoned = True

                time_since_ignition = self.t - self.time_s2_Ignition
                #Time based pitch ramp
                #Linear interpolation in time

                if time_since_ignition > self.s2_ramp_delay:
                    k = min((time_since_ignition - self.s2_ramp_delay) / self.s2_ramp_dur, 1)
                    target_pitch = self.s2_start_pitch + k * (self.s2_end_pitch - self.s2_start_pitch)
                else:
                    target_pitch = self.s2_start_pitch
                

                # Smooth approach (avoid jumps)
                max_delta = math.radians(0.5)
                delta_pitch = target_pitch - self.pitch_angle
                delta_pitch = max(min(delta_pitch, max_delta), -max_delta)
                self.pitch_angle += delta_pitch

                # Transition to orbit coast
                if (
                    self.vx >= self.S2_orbital_velocity 
                    or self.current_stage.state == stage_state.BURNED_OUT
                ):
                    self.state = rocket_state.ORBIT_COAST
                    self.current_stage.state = stage_state.SECO

            case rocket_state.ORBIT_COAST:
                
                self.current_stage.nominal_thrust = 0
                self.current_thrust = 0

                




            case _:
                pass


    ### Stage control
      
    def attach_stage(self, stage):
        if self.is_idle():
            self.stages.append(stage)
            stage.state = stage_state.ATTACHED


    def detach_stage(self, stage):
        return self.stages.remove(self.current_stage)
    

    #Helpers

    def stage_is_eligible(self, stage):
        if (stage.state in (stage_state.ATTACHED, stage_state.IGNITED)
            and stage.fuel_mass > 0):
            return True
        return False
    

    def set_current_stage(self):
        for stage in self.stages:
            if self.current_stage == None and self.stage_is_eligible(stage):
                self.current_stage = stage

            elif self.current_stage != None and self.stage_is_eligible(stage):
                self.next_stage = stage


    def is_idle(self):
        return self.state == rocket_state.IDLE

    def is_launch(self):
        return self.state == rocket_state.LAUNCH
    
    def is_pitch_initiation(self):
        return self.state == rocket_state.PITCH_INITIATION
    
    def is_ascent_burn(self):
        return self.state == rocket_state.ASCENT_BURN
        
    def is_stage1_separation(self):
        return self.state == rocket_state.STAGE1_SEPARATION
    
    def is_stage2_ignition(self):
        return self.state == rocket_state.STAGE2_IGNITION

    def is_coast(self):
        return self.state == rocket_state.COAST
    
    def is_stage2_ascent(self):
        return self.state == rocket_state.STAGE2_ASCENT
    
    def is_orbit_coast(self):
        return self.state == rocket_state.ORBIT_COAST

    