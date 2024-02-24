from globals import sensor_data
from arduino import arduino
from time import sleep

class PID_controller:
    def __init__(self, setpoint,process_var,time_interval, Kp, Kd, Ki):
        self.setpoint = setpoint
        self.process_var = sensor_data["mag_field_x"]
        self.time_interval = sensor_data["time_interval"] #in seconds
        self.Kp = Kp
        self.Kd = Kd
        self.Ki = Ki
        self.err_integ = 0
        self.prev_err = 0

    def update_values(self, process_var,time_interval):
        self.process_var = process_var
        self.time_interval = time_interval

    def set_setpoint(self, setpoint):
        self.setpoint = setpoint
        self.err_integ = 0 # need to reset these for next value I think
        self.prev_err = 0

    def tune_constants(self, Kp, Ki, Kd):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd

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
        return (self.proportional(self.setpoint,self.process_var)
                + self.differential(self.setpoint,self.process_var,self.time_interval)
                + self.integral(self.setpoint,self.process_var,self.time_interval))

    def run_PID(self):
        while (True):
            self.update_values(sensor_data["mag_field_x"],sensor_data["time_interval"])
            #print("Mag Field X: " + str(sensor_data["mag_field_x"]))
            new_val = self.get_PID()
            sensor_data['pwm_x'] = sensor_data['pwm_x'] + int(255*new_val)
            arduino.set_coil_current(sensor_data['pwm_x']*-1)

            #print("New PWM Val:" + str(sensor_data['pwm_x']))
            #sleep(0.1)



PID = PID_controller(-0.3,0,0,0.08,0.06,0.005)

