#ifndef UTILS_H
#define UTILS_H

#include <utility>
#include <vector>
#include <string>

/*
@def
    utility functions that reads CSV files and formats them into a more useful structure

@param sim
    vector of pairs, where each pair is an increment of time and a corresponding magnetic field strings

@param data_file_path
    path to csv to read from, provided by GUI

@param status_str
    string with status of if opening file was successful
*/
void read_csv(std::vector<std::pair<double, double>> & sim, std::string & data_file_path, std::string & status_str);



#endif 