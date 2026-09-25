import time, math
from rocket_sim.physics import physics
from rocket_sim.models.stage import stage_state, empty_stage, Stage
from rocket_sim.config.rocket_config import RocketConfig
from rocket_sim.guidance import pitch_init, stage_one_guidance, stage_two_guidance
from rocket_sim.config.sim_config import SimConfig



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
    def __init__(self, rocket_config: RocketConfig, y):
        self.rkt_config     = rocket_config
        self.stage_config   = rocket_config.stages
        self.pitch_init     = rocket_config.pitch_init
        self.s1_guidance    = rocket_config.s1_guidance
        self.s2_guidance    = rocket_config.s2_guidance
        self.state          = rocket_state.IDLE
        self.stages         = []
        

        stage1 = Stage(self.stage_config[0])
        stage2 = Stage(self.stage_config[1])

        self.attach_stage(stage1)
        self.attach_stage(stage2)

        self.current_stage  = None
        self.next_stage     = None

        self.fairing_jettisoned = False

        self.current_pitch      = math.radians(self.pitch_init.starting_pitch)
        self.command_pitch_done = False
        self.est_apo            = 0

        self.time_since_sep = 0.0


        self.target_thrust_fraction = 1.0     
        self.curr_thrust_frac       = 0.0

        self.applied_thrust = 0.0

        # ────────────────────────────────────────────────
        #  State — kinematics
        # ────────────────────────────────────────────────
        self.x              = 0.0
        self.y              = y
        self.vx             = 0.0
        self.vy             = 0.0
        self.ax             = 0.0
        self.ay             = 0.0
        self.total_velocity = 0.0
        self.total_accel    = 0.0
        self.v_r            = 0.0                   # radial velocity component
        self.r              = 0.0


        # ────────────────────────────────────────────────
        #  Simulation control & book-keeping
        # ────────────────────────────────────────────────
        
        self.t              = 0.0
        self.sim_running    = False
        self.orbit_initialized = False
        self.max_Q          = 0.0
        self.current_Q      = 0.0 #Pa
        self.target_r       = physics.R_e + SimConfig.target_orbit_altitude



        
        


    @property
    def total_mass(self):
        total_mass = sum(stage.calc_total_mass() 
                         for stage in self.stages 
                         if not stage.is_separated()) + self.rkt_config.payload_weight
        
        if not self.fairing_jettisoned:
            total_mass = total_mass + self.rkt_config.fairing_weight
        return  total_mass
    

    def __repr__(self):
        return f"Rocket(State: {self.state.name}, Current Stage: {self.current_stage.state.name}, Next Stage: {self.next_stage.state.name})"

    # ────────────────────────────────────────────────
    # Main loop
    # ────────────────────────────────────────────────
    def update(self, dt):

        self.t += dt
        #Update rocket state and stage
        self.set_rocket_state(dt)
        self.current_stage.update(dt)

        
        #Compute thrust based on current pitch

        # Thrust throttling
        self.applied_thrust = self.thrust_throttle(dt)        

        T_x, T_y = physics.calc_thrust(self.applied_thrust, self.current_pitch)

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
        
        # recompute acceleration at new position
        T_y = self.applied_thrust * math.cos(self.current_pitch)   # vertical
        T_x = self.applied_thrust * math.sin(self.current_pitch)   # horizontal
        self.ay, self.ax = physics.acceleration(self, T_y, T_x)

        # velocity Verlet step 2
        self.vx = vx_half + 0.5 * self.ax * dt
        self.vy = vy_half + 0.5 * self.ay * dt
               

        #Update total velocity and accel
        self.total_velocity = physics.total_velocity(self.vx, self.vy)
        self.total_accel = physics.total_accel(self.ay, self.ax)

        # update dynamic pressure
        self.current_Q   = physics.dynamic_pressure(vy=self.vy, y=self.y) #Pa
        if self.current_Q > self.max_Q:
            self.max_Q = self.current_Q

        #calculate est apo
        self.est_apo = self.get_est_apo()
    
            
    
    # ────────────────────────────────────────────────
    #Rocket state machine
    # ────────────────────────────────────────────────

    def set_rocket_state(self, dt):
        match self.state:
            case rocket_state.IDLE:
                self.vy = 0
                self.ay = 0
                self.set_current_stage()
                self.state = rocket_state.LAUNCH


            case rocket_state.LAUNCH:
                self.current_stage.state = stage_state.IGNITED
                if self.y > self.pitch_init.init_height:
                    self.state = rocket_state.PITCH_INITIATION
            

            case rocket_state.PITCH_INITIATION:
                self.current_pitch, self.command_pitch_done = pitch_init.initialize_pitch(self.pitch_init,
                                                                                          self.current_pitch,
                                                                                          self.command_pitch_done)
                    
                if self.command_pitch_done:
                    self.state = rocket_state.ASCENT_BURN
                

            case rocket_state.ASCENT_BURN:
                
                if self.t > self.s1_guidance.s1_throttle_dwn_time:
                    self.current_stage.state = stage_state.THROTTLE_DOWN

                if self.t > self.s1_guidance.s1_throttle_up_time:
                    self.current_stage.state = stage_state.IGNITED

                # Stage 1 guidance
                self.current_pitch = stage_one_guidance.s1_guidance(self.s1_guidance,
                                                                    self.t,
                                                                    self.current_pitch,
                                                                    self.current_stage.throttle,
                                                                    self.current_stage.is_throttled()
                                                                    )

                # Stage 1 separation trigger
                if (
                    (
                    self.y >= self.s1_guidance.s1_sep_min_alt
                    and self.total_velocity >= self.s1_guidance.s1_min_vel
                    )
                    or self.t >= self.s1_guidance.s1_nominal_burn_time
                ):
                    
                    self.state = rocket_state.STAGE1_SEPARATION
                    self.current_stage.state = stage_state.MECO
                
                elif self.t > self.s1_guidance.s1_nominal_burn_time + 20:
                    
                    self.state = rocket_state.STAGE1_SEPARATION
                    self.current_stage.state = stage_state.MECO

            case rocket_state.STAGE1_SEPARATION:
                self.time_since_sep += dt
                if self.current_stage.is_meco():
                    
                    if self.time_since_sep >= self.s1_guidance.s1_MECO_delay:
                        self.detach_stage(self.current_stage)
                        self.current_stage = self.next_stage
                        self.next_stage = empty_stage()
                        self.next_stage.state = stage_state.EMPTY
                        self.state = rocket_state.COAST


            case rocket_state.COAST:
                self.time_since_sep += dt
                if self.time_since_sep >= self.s2_guidance.s2_ignition_delay:
                    self.state = rocket_state.STAGE2_IGNITION


            case rocket_state.STAGE2_IGNITION:
                self.time_s2_Ignition = self.t
                self.current_stage.state = stage_state.IGNITED
                if self.current_stage.state == stage_state.IGNITED:
                    self.state = rocket_state.STAGE2_ASCENT            


            case rocket_state.STAGE2_ASCENT:
                # Fairing jettison
                if not self.fairing_jettisoned and self.y >= self.s2_guidance.s2_fairing_jettison_height:
                    self.fairing_jettisoned = True

                # Stage 2 guidance
                self.current_pitch = stage_two_guidance.s2_guidance(self.s2_guidance,
                                                                    self.current_pitch,
                                                                    self.est_apo,
                                                                    self.y,
                                                                    self.vy)

                # Transition to orbit coast
                if (
                    self.vx >= self.s2_guidance.s2_orbital_velocity
                    or self.current_stage.state == stage_state.BURNED_OUT
                ):
                    self.state = rocket_state.ORBIT_COAST
                    self.current_stage.state = stage_state.SECO

            case rocket_state.ORBIT_COAST:
                
                self.sim_running = False

            case _:
                pass

    # ────────────────────────────────────────────────             
    # Stage control
    # ────────────────────────────────────────────────  
    def attach_stage(self, stage):
        if self.is_idle():
            self.stages.append(stage)
            stage.state = stage_state.ATTACHED


    def detach_stage(self, stage):
        return self.stages.remove(self.current_stage)
    
    # ────────────────────────────────────────────────
    # Helpers
    # ────────────────────────────────────────────────

    def thrust_throttle(self, dt):
        if self.current_stage is None:
            return 0.0
        if (self.is_orbit_coast() 
            or self.current_stage.state in (stage_state.SECO, stage_state.MECO)
            ):
            self.curr_thrust_frac = 0
            return 0.0

        goal_fraction = self.target_thrust_fraction
        
        #Manage thrust output for first 15km then full burn

        if self.current_stage:
            if 0 < self.t < 35 and self.y < 2500:
                if self.ay > 2.1:
                    goal_fraction = 0.80
                                        
            elif 35 < self.t < 55 and self.y < 5000:
                if self.ay > 3.3:
                    goal_fraction = 0.75
                    
            elif 55 < self.t < 80 and self.y < 10000:
                goal_fraction = self.s1_guidance.s1_max_q_throttle
                if self.ay > 15:
                    goal_fraction = self.s1_guidance.s1_max_q_throttle
            
            elif self.t > 75 and self.current_stage.state == stage_state.THROTTLE_DOWN:
                goal_fraction = self.s1_guidance.s1_max_q_throttle
                    
            else:           
                goal_fraction = self.target_thrust_fraction  #max thrust
            
            #Manage G limit and total velocity throttling
            if self.is_ascent_burn:
                max_total_vel = 1950
            elif self.is_stage2_ascent:
                max_total_vel = 7650

            if self.total_accel > SimConfig.g_limit or self.total_velocity > max_total_vel:
                # Calculate the exact throttle needed to stay at 3.5Gs
                # Force = Mass * Acceleration
                required_force = self.total_mass * SimConfig.g_limit

                if self.current_stage.stage_config.thrust == 0:
                    goal_fraction = 0.0
                else:
                    goal_fraction = required_force / self.current_stage.stage_config.thrust

                goal_fraction = max(0.4, min(goal_fraction, 1.0))
                
        else:
            goal_fraction = 0.0

        # Rate-limit the change
        if self.current_stage.stage_config.thrust == 0:
            self.curr_thrust_frac = 0.0
            return 0.0
        
        current_fraction = self.applied_thrust / self.current_stage.stage_config.thrust if self.applied_thrust > 0 else 1.0
        max_change = self.s1_guidance.s1_throttle_rate_limit * dt
    
        delta = goal_fraction - current_fraction

        clamped_delta = max(min(delta, max_change), -max_change)
        new_fraction = current_fraction + clamped_delta

        self.current_stage.throttle = new_fraction
        self.applied_thrust = self.current_stage.stage_config.thrust * new_fraction
        self.curr_thrust_frac = new_fraction
        
        return self.applied_thrust
    
    def get_est_apo(self):
        mu       = physics.G * physics.M_e
        self.r   = math.sqrt(self.x**2 + (physics.R_e + self.y)**2)
        v2       = self.total_velocity**2
        epsilon  = v2 / 2 - mu / self.r
        if epsilon >= 0:
            apo_str = "Hyperbolic escape"
        else:
            a = -mu / (2 * epsilon)
            h_sq = (self.x * self.vy - (physics.R_e + self.y) * self.vx)**2  # ang mom squared
            e_term = 1 + (2 * epsilon * h_sq / mu**2)
            e = math.sqrt(max(e_term, 0))  # clamp to avoid domain error
            r_a = a * (1 + e)
            apo_alt = r_a - physics.R_e
            est_apo = apo_alt/1000
            if apo_alt > 800000:
                self.sim_running = False
            return est_apo

    def stage_is_eligible(self, stage):
        if (stage.state in (stage_state.ATTACHED, stage_state.IGNITED)
            and stage.current_fuel_mass > 0):
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

    # ────────────────────────────────────────────────
    # Receive telemetry data and format in to readable data
    # ────────────────────────────────────────────────

    def get_telemetry(self):
        telemetry_data    = {}

        flight_path_angle = math.atan2(self.vy, self.vx)
        t_mass            = self.total_mass
        pitch_deg         = math.degrees(self.current_pitch)
        V_r               = abs(self.v_r)
        fuel              = 0.0
        burn_rate         = 0.0
        if self.current_stage is not None:
            fuel = self.current_stage.current_fuel_mass
            burn_rate = self.current_stage.current_burn_rate

        Fg_y, Fg_x        = physics.gravity_force(self.total_mass, self.y, self.x)
        Fg_y              = Fg_y / 1000
        Fg_x              = Fg_x / 1000

        telemetry_data["v_total"] = self.total_velocity
        telemetry_data["total_accel"] = self.total_accel
        telemetry_data["y"] = self.y
        telemetry_data["vy"] = self.vy
        telemetry_data["ay"] = self.ay
        telemetry_data["x"] = self.x
        telemetry_data["vx"] = self.vx
        telemetry_data["ax"] = self.ax
        telemetry_data["pitch"] = pitch_deg
        telemetry_data["flight_path_a"] = flight_path_angle
        telemetry_data["fg_y"] = Fg_y
        telemetry_data["fg_x"] = Fg_x
        telemetry_data["q"] = self.current_Q
        telemetry_data["max_q"] = self.max_Q
        telemetry_data["thrust_%"] = self.curr_thrust_frac
        telemetry_data["thrust"] = self.applied_thrust
        telemetry_data["fuel"] = fuel
        telemetry_data["burn_r"] = burn_rate
        telemetry_data["mass"] = t_mass
        telemetry_data["v_r"] = V_r
        telemetry_data["r"] = self.r
        telemetry_data["rocket_state"] = self.state.name
        telemetry_data["current_stage"] = self.current_stage.state.name if self.current_stage else 'None'
        telemetry_data["next_stage"] = self.next_stage.state.name if self.next_stage else 'None'
        telemetry_data["est_apoapsis"] = self.est_apo
        telemetry_data["t"] = self.t

        return telemetry_data
        