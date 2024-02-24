from globals import sensor_data
from arduino import arduino
from logger import logger
from time import sleep

class PID_controller:
    def __init__(self, axis, setpoint, process_var,time_interval, Kp, Kd, Ki):
        self.axis = axis
        self.setpoint = setpoint
        self.process_var = sensor_data["mag_field_x"]
        self.time_interval = sensor_data["time_interval"] #in seconds
        self.Kp = Kp
        self.Kd = Kd
        self.Ki = Ki
        self.err_integ = 0
        self.prev_err = 0
        self.enable = 1

    def update_values(self, process_var,time_interval):
        self.process_var = process_var
        self.time_interval = time_interval

    def set_setpoint(self, setpoint):
        self.setpoint = setpoint
        logger.info(f"Setpoint for {self.axis} updated to {setpoint}")
        self.err_integ = 0 # need to reset these for next value I think
        self.prev_err = 0

    def tune_constants(self, Kp, Ki, Kd):
        logger.info(f"Updated PID Constants -- Kp: {Kp}, Ki: {Ki}, Kd: {Kd}")
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd

    def toggle_PID(self):
        self.enable = not self.enable
        if self.enable:
            logger.info(f"PID Controller for {self.axis} enabled")
        else:
            logger.info(f"PID Controller for {self.axis} disabled")

    def proportional(self,setpoint,process_var):
        err = setpoint - process_var
        return (self.Kp*err)

    def differential(self, setpoint,process_var,time_interval):
        err = setpoint - process_var
        err_diff = self.Kd*(self.prev_err - err)/time_interval
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

    def run_PID(self):
        while (True):
            self.update_values(sensor_data["mag_field_x"],sensor_data["time_interval"])
            print("Current Mag Field: ", self.process_var)
            print("Current PWM: ", sensor_data[f'pwm_{self.axis}'])
            print("Setpoint: ", self.setpoint)
            new_val = self.get_PID()
            print("New Value: ", new_val)
            # Ensure that the PWM value is between -255 and 255 (also multiplied by -1 to match the direction of the current)
            if self.enable:
                sensor_data[f'pwm_{self.axis}'] = (sensor_data[f'pwm_{self.axis}'] + (int(255*new_val)*-1))
                print("PWM Value: ", sensor_data[f'pwm_{self.axis}'])
                arduino.set_coil_current((sensor_data[f'pwm_{self.axis}'] + int(255*new_val)))
                sleep(0.1)
            else:
                sleep(0.5) # sleep for 0.5 seconds if PID is disabled
                # TODO: change this so thread sleeps when controller is off



pid = PID_controller("x",-0.2,0,0,0.1,0,0)

