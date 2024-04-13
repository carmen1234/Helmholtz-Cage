from globals import sensor_data
from arduino import arduino
from logger import logger
from time import sleep
from util import read_csv_into_dict
import os

class PID_controller:
    def __init__(self, axis, setpoint, Kp, Ki, Kd):
        self.axis = axis
        self.setpoint = setpoint
        self.process_var = sensor_data[f"mag_field_{self.axis}"]
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
        sensor_data[f"mag_field_{self.axis}_setpoint"] = setpoint
        self.err_integ = 0 # need to reset these for next value I think
        self.prev_err = 0

    def tune_constants(self, Kp, Ki, Kd):
        logger.info(f"Updated {self.axis}-axis PID Constants -- Kp: {Kp}, Ki: {Ki}, Kd: {Kd}")
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd

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
        if self.setpoint == '-':
            return None
        mag_field_setpoint = self.proportional(self.setpoint,self.process_var) \
        + self.differential(self.setpoint,self.process_var,self.time_interval) \
        + self.integral(self.setpoint,self.process_var,self.time_interval)

        return mag_field_setpoint

class MegaController:
    def __init__(self):
        self.pid_x = PID_controller("x",0,0.05,0.0009,0)
        self.pid_y = PID_controller("y",0,0.05,0.004,0)
        self.pid_z = PID_controller("z",0,0.1,0.001,0)
        self.setpoints = {"x_setpoint": 0.0,
                          "y_setpoint": 0.0,
                          "z_setpoint": 0.0}
        self.sim_on = 0  # sim refers to dynamic mode
        self.sim_data = []
        self.sim_step = 0 # basically which row its on, needed for pausing,restarting
        self.sim_step_len = 0 #number of simulation steps (rows in csv file)
        self.sim_data_len = 0
        self.enable_pid = False

    def get_sim(self, path):
        if os.path.exists(path) == False:
            logger.error(f"File {path} does not exist")
            return None

        reader = read_csv_into_dict(path)

        if reader != None:
            self.sim_data = list(read_csv_into_dict(path))
            self.sim_data_len = len(self.sim_data)
            if self.sim_data_len == 0:
                logger.error(f"File {path} is empty")
                return None
            logger.info(f"Read {self.sim_data_len} rows from {path}")
            return 1
        else:
            logger.error(f"Failed to read data from {path}")
            return None

    def turn_on_sim(self):
        if self.sim_data_len == 0:
            logger.error(f"Simulation data not loaded. Please load simulation data first.")
            return

        if self.enable_pid:
            logger.warn(f"Disabling static mode and starting dynamic mode")
        else:
            self.toggle_PID()
            logger.info(f"Starting dynamic simulation")

        self.sim_on = 1

    def turn_off_sim(self):
        self.sim_on = 0
        self.sim_step = 0
        self.toggle_PID()

    def reset_sim(self):
        if self.sim_data_len == 0:
            logger.error(f"Simulation data not loaded. Please load simulation data first.")
            return

        self.turn_off_sim()
        self.sim_step = 0

    def pause_sim(self):
        if self.sim_data_len == 0:
            logger.error(f"Simulation data not loaded. Please load simulation data first.")
            return

        self.sim_on = 0
        logger.info(f"Simulation paused")

    def resume_sim(self):
        if self.sim_data_len == 0:
            logger.error(f"Simulation data not loaded. Please load simulation data first.")
            return

        self.sim_on = 1
        logger.info(f"Simulation resumed")

    def toggle_PID(self):
        if self.sim_on == 1:
            logger.warn(f"Cannot toggle PID controller while simulation is running")
            return
        self.enable_pid = not self.enable_pid
        if self.enable_pid:
            logger.info(f"PID Controller enabled")
        else:
            # Reset pwm to 0
            sensor_data[f'pwm_{self.pid_x.axis}'] = 0
            sensor_data[f'pwm_{self.pid_y.axis}'] = 0
            sensor_data[f'pwm_{self.pid_z.axis}'] = 0
            arduino.set_coil_current(sensor_data['pwm_x'], sensor_data['pwm_y'], sensor_data['pwm_z'])
            logger.info(f"PID Controller disabled")

    def update_setpoint_data(self, setpoint_x, setpoint_y, setpoint_z):
        self.setpoints["x_setpoint"] = setpoint_x
        self.setpoints["y_setpoint"] = setpoint_y
        self.setpoints["z_setpoint"] = setpoint_z
        sensor_data["mag_field_x_setpoint"] = setpoint_x
        sensor_data["mag_field_y_setpoint"] = setpoint_y
        sensor_data["mag_field_z_setpoint"] = setpoint_z
        self.pid_x.set_setpoint(setpoint_x)
        self.pid_y.set_setpoint(setpoint_y)
        self.pid_z.set_setpoint(setpoint_z)
        logger.info(f"Setpoints updated to x: {setpoint_x}, y: {setpoint_y}, z: {setpoint_z}")

    def run_sim(self): #i think this will still need to be its own thread
        while True:
            if self.sim_on == 0:
                pass #no sim or its paused
            elif self.sim_on == 1:
                #time difference stuff will be done later cuz its giving me a headache
                current_step = self.sim_data[self.sim_step] #current dict that has data

                # self.pid_x.set_setpoint(float(current_step["Bx(G)"]))
                # self.pid_y.set_setpoint(float(current_step["By(G)"]))
                # self.pid_z.set_setpoint(float(current_step["Bz(G)"]))
                self.update_setpoint_data(float(current_step["Bx(G)"]), float(current_step["By(G)"]), float(current_step["Bz(G)"]))


                step_time = float(self.sim_data[self.sim_step]["Time(s)"])
                sleep(step_time)
                self.sim_step = self.sim_step + 1 # increment for next one

                if self.sim_step == self.sim_data_len:
                    self.turn_off_sim()
                    logger.info("Simulation completed")

                # print(f"sim_step: {self.sim_step}")
                # print(f"step_time: {step_time}")
            sleep(0.1)

    def run_pid_xyz(self): #this should be used for the thread
        while (True):
            self.pid_x.update_values(sensor_data["mag_field_x"],sensor_data["time_interval"])
            new_val_x = self.pid_x.get_PID()
            self.pid_y.update_values(sensor_data["mag_field_y"],sensor_data["time_interval"])
            new_val_y = self.pid_y.get_PID()
            self.pid_z.update_values(sensor_data["mag_field_z"],sensor_data["time_interval"])
            new_val_z = self.pid_z.get_PID()
            if self.enable_pid == True:
                #print(f"new_val_x: {new_val_x}\n")
                if new_val_x is None:
                    new_pwm_val_x = 0
                else:
                    new_pwm_val_x = sensor_data[f'pwm_{self.pid_x.axis}'] + (int(100*new_val_x))

                if new_val_y is None:
                    new_pwm_val_y = 0
                else:
                    new_pwm_val_y = sensor_data[f'pwm_{self.pid_y.axis}'] + (int(100*new_val_y))

                if new_val_z is None:
                    new_pwm_val_z = 0
                else:
                    new_pwm_val_z = sensor_data[f'pwm_{self.pid_z.axis}'] + (int(100*new_val_z))

                sensor_data[f'pwm_{self.pid_x.axis}'] = max(-100, min(100, new_pwm_val_x))
                sensor_data[f'pwm_{self.pid_y.axis}'] = max(-100, min(100, new_pwm_val_y))
                sensor_data[f'pwm_{self.pid_z.axis}'] = max(-100, min(100, new_pwm_val_z))
                #print(f"sensor_data[f'pwm_{self.pid_x.axis}']: ", sensor_data[f'pwm_{self.pid_x.axis}'])

                arduino.set_coil_current(sensor_data['pwm_x'], sensor_data['pwm_y'], sensor_data['pwm_z'])

            sleep(0.1)

main_controller = MegaController()


