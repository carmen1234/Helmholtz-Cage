# Helmholtz-Cage



# Requirements and Setup 

## Requirements

- At least python 3.10 or greater
- wxPython 4.0.7 or greater


## Setup 

>     pip install wxPython

or 

>     sudo apt install python3-wxgtk4.0

# How to run

py main.py (Windows)


# Commands

The following commands can be used in the debug console

```set0```

Set all coils to 0 current


```tune_pid [axis] [kp] [ki] [kd]```

Adjusts the pid constants of \[axis\], specified by x,y,or z

For example:

>      tune_pid x 0.001 0.01 0 

will set the coil on the x-axis constants to Kp = 0.001, Ki = 0.01, and Kd = 0

To keep a constant the same, but modify others, use -

For example:

>      tune_pid x 0.001 - 0 

will modify Kp and Kd, but leave Ki untouched

```set_pwm [axis] [speed]```

will set the pwm for the axis specified by \[axis\], and where \[speed\] is an integer between -255 and 255

```clear```

clears the console output

Example gif: