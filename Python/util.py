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

def convert_raw_mag_input_to_gauss(raw_mag_data):
    mag_val = (((max_guass - min_gauss)*(raw_mag_data - raw_mag_min))/(raw_mag_max - raw_mag_min)) + raw_mag_min
    return mag_val




