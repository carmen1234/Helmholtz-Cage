class PID_controller:
    def __init__(self, setpoint,process_var,time_interval, Kp, Kd, Ki):
        self.setpoint = setpoint
        self.process_var = process_var
        self.time_interval = time_interval
        self.Kp = Kp
        self.Kd = Kd
        self.Ki = Ki
        self.err_integ = 0
        self.prev_err = 0
    
    def update_values(self, setpoint,process_var,time_interval):
        self.setpoint = setpoint
        self.process_var = process_var
        self.time_interval = time_interval

    def tune_constants(self, Kp, Kd, Ki):
        self.Kp = Kp
        self.Kd = Kd
        self.Ki = Ki

    def proportional(self,setpoint,process_var):
        err = setpoint - process_var
        return (self.Kp*err)     

    def differential(self, setpoint,process_var,time_interval):
        err = setpoint - process_var
        err_diff = (self.prev_err - err)/time_interval
        self.prev_err = err
        return self.Kd*err_diff

    def integral(self, setpoint,process_var,time_interval):
        err = setpoint - process_var
        self.err_integ += err*time_interval
        return self.Ki*self.err_integ

    def get_PID(self):
        return (self.proportional(self.setpoint,self.process_var) 
                + self.differential(self.setpoint,self.process_var,self.time_interval) 
                + self.integral(self.setpoint,self.process_var,self.time_interval))

