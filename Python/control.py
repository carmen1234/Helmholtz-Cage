from globals import sensor_data
from arduino import arduino
from logger import logger
from time import sleep
from util import read_csv_into_dict

class PID_controller:
    def __init__(self, axis, setpoint, Kp, Ki, Kd):
        self.axis = axis
        self.setpoint = setpoint
        self.process_var = sensor_data["mag_field_x"]
        self.time_interval = sensor_data["time_interval"] # in seconds
        self.Kp = Kp
        self.Kd = Kd
        self.Ki = Ki
        self.err_integ = 0
        self.prev_err = 0
        self.enable = False

    def update_values(self, process_var,time_interval):
        self.process_var = process_var
        self.time_interval = time_interval

    def set_setpoint(self, setpoint):
        self.setpoint = setpoint
        logger.info(f"Updated setpoint for {self.axis}-axis  to {setpoint} Gauss")
        self.err_integ = 0 # need to reset these for next value I think
        self.prev_err = 0

    def tune_constants(self, Kp, Ki, Kd):
        logger.info(f"Updated {self.axis}-axis PID Constants -- Kp: {Kp}, Ki: {Ki}, Kd: {Kd}") 
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd

    def toggle_PID(self): #i think I can remove this from here?
        self.enable = not self.enable
        if self.enable:
            logger.info(f"PID Controller for {self.axis} enabled")
        else:
            # Reset pwm to 0
            arduino.set_coil_current(0)
            sensor_data[f'pwm_{self.axis}'] = 0
            logger.info(f"PID Controller for {self.axis} disabled")

    def proportional(self,setpoint,process_var):
        err = setpoint - process_var
        return (self.Kp*err)

    def differential(self, setpoint,process_var,time_interval):
        err = setpoint - process_var
        #err_diff = self.Kd*(self.prev_err - err)/time_interval
        err_diff = self.Kd*(err - self.prev_err)/time_interval
        self.prev_err = err
        return err_diff

    def integral(self, setpoint,process_var,time_interval):
        err = setpoint - process_var
        self.err_integ += err*self.Ki*time_interval
        return self.err_integ

    def get_PID(self):
        mag_field_setpoint = self.proportional(self.setpoint,self.process_var) \
        + self.differential(self.setpoint,self.process_var,self.time_interval) \
        + self.integral(self.setpoint,self.process_var,self.time_interval)

        sensor_data[f"mag_field_{self.axis}_setpoint"] = mag_field_setpoint

        return mag_field_setpoint

    def run_PID(self): #can also be removed?
        while (True):
            self.update_values(sensor_data["mag_field_x"],sensor_data["time_interval"])
            new_val = self.get_PID()
            if self.enable:
                new_pwm_val = sensor_data[f'pwm_{self.axis}'] + (-1 * int(100*new_val))
                sensor_data[f'pwm_{self.axis}'] = max(-100, min(100, new_pwm_val))
                arduino.set_coil_current(sensor_data[f'pwm_{self.axis}'])
                sleep(0.1)
            else:
                sleep(0.5) # sleep for 0.5 seconds if PID is disabled
                # TODO: change this so thread sleeps when controller is off

    


class MegaController:
    def __init__(self):
        self.pid_x = PID_controller("x",0,0.05,0,0) #todo: change pid to pid_x
        self.pid_y = PID_controller("y",0,0.05,0,0)
        self.pid_z = PID_controller("z",0,0.05,0,0)
        self.sim_on = 0  # sim refers to dynamic mode 
        self.sim_data = []
        self.sim_step = 0 # basically which row its on, needed for pausing,restarting
        self.sim_step_len = 0 #number of simulation steps (rows in csv file)
        self.enabl_pid = False
    
    def get_sim(self, path):
        reader = read_csv_into_dict(path)
        if reader != None:
            self.sim_data = list(read_csv_into_dict(path))
            self.sim_data_len = len(self.sim_data)
            return 1
        else:
            return None

    def turn_on_sim(self):
        self.sim_on = 1
        self.enable_pid = True #enable the feedback loop

    def turn_off_sim(self):
        self.sim_on = 0
        self.enable_pid = False

    def toggle_PID(self):
        self.enable_pid = not self.enable_pid
        if self.enable_pid:
            logger.info(f"PID Controller for {self.axis} enabled")
        else:
            # Reset pwm to 0
            arduino.set_coil_current(0)
            sensor_data[f'pwm_{self.axis}'] = 0
            logger.info(f"PID Controller for {self.axis} disabled")
        

    def run_sim(self): #i think this will still need to be its own thread
        if self.sim_on == 0:
            pass #no sim or its paused
        elif self.sim_on == 1:
            #time difference stuff will be done later cuz its giving me a headache
            current_step = self.sim_data[self.sim_step] #current dict that has data
            
            self.pid_x.set_setpoint(float(current_step["Bx(G)"]))
            self.pid_y.set_setpoint(float(current_step["By(G)"]))
            self.pid_z.set_setpoint(float(current_step["Bz(G)"]))

            #have it sleep until next step, but check if it is last step
            if self.sim_step == (self.sim_step_len - 1):
                self.turn_off_sim()
            else:
                next_step_time = float(self.sim_data[self.sim_step]["Time(s)"])
                sleep(next_step_time - current_step["Time(s)"])
                self.sim_step = self.sim_step + 1 # increment for next one

    def run_pid_xyz(self): #this should be used for the thread 
        while (True):
            self.pid_x.update_values(sensor_data["mag_field_x"],sensor_data["time_interval"])
            new_val_x = self.pid_x.get_PID()    
            self.pid_y.update_values(sensor_data["mag_field_y"],sensor_data["time_interval"])
            new_val_y = self.pid_y.get_PID()
            self.pid_z.update_values(sensor_data["mag_field_z"],sensor_data["time_interval"])
            new_val_z = self.pid_z.get_PID()
            if self.enable_pid:
                new_pwm_val_x = sensor_data[f'pwm_{self.pid_x.axis}'] + (-1 * int(100*new_val_x))
                new_pwm_val_y = sensor_data[f'pwm_{self.pid_y.axis}'] + (-1 * int(100*new_val_y))
                new_pwm_val_z = sensor_data[f'pwm_{self.pid_z.axis}'] + (-1 * int(100*new_val_z))
                sensor_data[f'pwm_{self.pid_x.axis}'] = max(-100, min(100, new_pwm_val_x))
                sensor_data[f'pwm_{self.pid_y.axis}'] = max(-100, min(100, new_pwm_val_y))
                sensor_data[f'pwm_{self.pid_z.axis}'] = max(-100, min(100, new_pwm_val_z))

                #modify this func so it can set multiple
                arduino.set_coil_current(sensor_data[f'pwm_{self.axis}'])
                sleep(0.1)
            else:
                sleep(0.5) # sleep for 0.5 seconds if PID is disabled
                # TODO: change this so thread sleeps when controller is off


pid = PID_controller("x",0,0.05,0,0) #todo: delete later
pid_y = PID_controller("y",0,0.05,0,0)
pid_z = PID_controller("z",0,0.05,0,0)

