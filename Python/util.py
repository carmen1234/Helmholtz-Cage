import csv
from globals import HW_params

def read_csv_into_dict(csv_path):
    csv_file = open(csv_path,"r")
    return csv.DictReader(csv_file) #default delim is ","

def get_current_from_mag_field(mag_field):
    # using B = u*n*I
    #u of copper = 1.257x10^(-6) from wikipedia
    n = 5 #for demo on nov 24

    I = mag_field/(pow(1.257,-6)*n)
    return I

def convert_raw_mag_input_to_gauss(raw_mag_data): # might need to change this if conversion is 3000 raw = 1 Gauss
    mag_val = (((HW_params.max_guass - HW_params.min_gauss)*(raw_mag_data - HW_params.raw_mag_min))/(HW_params.raw_mag_max - HW_params.raw_mag_min)) + HW_params.raw_mag_min
    return mag_val

def tesla_to_gauss(tesla_val):
    return 10000*tesla_val  #1T = 10000G

def gauss_to_tesla(gauss_val):
    return gauss_val/10000





