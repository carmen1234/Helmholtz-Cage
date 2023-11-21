
# consts (tune) (should I move these to globals.py?)
epsilon = 0.000001
Kp = 1
Kd = 1
Ki = 1

def proportional(setpoint,process_var):
    err = setpoint - process_var
    return (Kp*err)
    


def differential(setpoint,process_var,time_interval):
    err = setpoint - process_var
    err_diff = err/time_interval
    return Kd*err_diff



def integral(setpoint,process_var,time_interval):
    err = setpoint - process_var
    err_integ = err*time_interval
    return Ki*err_integ





class PID_controller:
    def __init__(setpoint,process_var,time_interval):
        self.setpoint = setpoint
        self.process_var = process_var
        self.time_interval = time_interval
    
    def update_values(setpoint,process_var,time_interval):
        self.setpoint = setpoint
        self.process_var = process_var
        self.time_interval = time_interval

    def get_PID(self):
        return (proportional(self.setpoint,self.process_var,self.time_interval) 
                + differential(self.setpoint,self.process_var,self.time_interval) 
                + integral(self.setpoint,self.process_var,self.time_interval))

