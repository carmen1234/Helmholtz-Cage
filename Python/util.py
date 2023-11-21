import csv


def read_csv_into_dict(csv_path):
    csv_file = open(csv_path,"r")
    return csv.DictReader(csv_file) #default delim is ","

def get_current_from_mag_field(mag_fielld):
    # using B = u*n*I
    #u of copper = 1.257x10^(-6) from wikipedia
    n = 6 #for demo on nov 24

    I = mag_fielld/(pow(1.257,-6)*n)



