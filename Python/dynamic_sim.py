from util import read_csv_into_dict
from arduino import arduino
from control import pid, pid_y, pid_z
from time import sleep

class dynamic_simulation:
    def __init__(self):
        self.sim_on = 0 
        self.sim_data = []
        self.sim_step = 0 # basically which row its on, needed for pausing,restarting
        self.sim_step_len = 0 #number of simulation steps (rows in csv file)

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

    def turn_off_sim(self):
        self.sim_on = 0

    def run_sim(self):
        if self.sim_on == 0:
            pass #no sim or its paused
        elif self.sim_on == 1:
            #time difference stuff will be done later cuz its giving me a headache
            current_step = self.sim_data[self.sim_step] #current dict that has data
            
            pid.set_setpoint(float(current_step["Bz(G)"]))

            #have it sleep until next step, but check if it is last step
            if self.sim_step == (self.sim_step_len - 1):
                self.turn_off_sim()
            else:
                next_step_time = float(self.sim_data[self.sim_step]["Time(s)"])
                sleep(next_step_time = current_step["Time(s)"])
                self.sim_step = self.sim_step + 1 # increment for next one




dyna_sim = dynamic_simulation()
            
        

    

        
        
