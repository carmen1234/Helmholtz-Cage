#include "../include/utils.h"
#include <fstream>
#include <iostream>
#include <iomanip>

void read_csv(std::vector<std::pair<double, double>> & sim, std::string & data_file_path){

    std::ifstream data_file (data_file_path);

    //error checking won't be necessary for GUI but probably good to have from API perspective
    std::string line;
    if(data_file.fail()){
        std::cout << "Unable to open file, check file path and permissions" << std::endl;
    } else {
        //read from file
        int i = 0; 
        while(std::getline(data_file, line)){

            //read_csv expects the format of CSV files to be: time,field
            std::string time_val = line.substr(0, line.find(","));
            std::string field_val = line.substr(line.find(",")+1, line.size()-1);

            std::cout << "time val = " << time_val << " | field_val = " << field_val << std::endl;

            //for every entry in the csv file, construct a pair and append to sim vector
            sim.emplace_back(std::make_pair(std::stod(time_val),std::stod(field_val)));

            std::cout << std::setprecision (4) << sim[i].first << "," << sim[i].second << std::endl;
            i++;
        }


    }
}


//for testing
// int main(){

//     std::vector<std::pair<double, double>> dummy;
//     std::string file_path = "test.csv";

//     read_csv(dummy, file_path);

//     return 0;
// }


//TODO: ADD BETTER ERROR CHECKING