import csv


def read_csv_into_dict(csv_path):
    csv_file = open(csv_path,"r")
    return csv.DictReader(csv_file) #default delim is ","

