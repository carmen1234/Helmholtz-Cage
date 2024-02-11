import sys
sys.path.append("../")

from control import PID_controller

#for graphing
import matplotlib.pyplot as plt
import numpy as np

# PWM<->Gauss conversion functions
def mag_to_pwm(mag_guass):
    return int(float(255)*float(mag_guass))

def pwm_to_mag(pwm):
    return float(pwm)/float(255)

# starting values
setpoint = -0.4
measurement = 0.1
pwm = mag_to_pwm(measurement) 
time_interval = 0.1 


# tune these
Kp = 0.1
Ki = 0.6
Kd = 0.1

c = PID_controller(setpoint, measurement, time_interval, Kp, Kd, Ki)

# for graphing
measured_vals = []
time = []
setpoint_list = [setpoint]*100



for t in range(0,100):
    print("PWM = " + str(pwm) + " | measurement = " + str(measurement) +  " | setpoint = " + str(setpoint))

    measured_vals.append(measurement)
    time.append(t*time_interval)

    pid_val = c.get_PID()


    # this would likely be how we would use the PID controller in our code
    pwm = pwm + pid_val*mag_to_pwm(pid_val)
    measurement = pid_val + measurement

    c.update_values(setpoint, measurement, time_interval)



xpoints = np.array(time)
ypoints = np.array(measured_vals)
setpoint_graph = np.array(setpoint_list)

plt.plot(xpoints, ypoints, label="response with PID")
plt.plot(xpoints,setpoint_list, label="setpoint")

plt.xlabel("Time(s)")
plt.ylabel("Guass")

plt.title("PID Controller")

plt.legend()

plt.show()


