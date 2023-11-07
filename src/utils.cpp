#include "utils.h"
#include <fstream>
#include <iostream>
#include <iomanip>
#include "../mathplot/mathplot.h"

void read_csv(std::vector<std::pair<double, double>> & sim, std::string & data_file_path, std::string & status_str){

    std::ifstream data_file (data_file_path);

    //error checking won't be necessary for GUI but probably good to have from API perspective
    std::string line;
    if(data_file.fail()){
        std::cout << "Unable to open file, check file path and permissions" << std::endl;
        status_str = "Unable to open file: " + data_file_path;
    } else {
        //read from file
        status_str = "Successfully opened file: " + data_file_path;
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

// //temp, for testing, from stackoverflow
// void mpFXYVector::AddData(float x, float y, std::vector<double> &xs, std::vector<double> &ys)
//     {
//         // Check if the data vectora are of the same size
//         if (xs.size() != ys.size()) {
//             wxLogError(_("wxMathPlot error: X and Y vector are not of the same length!"));
//             return;
//         }

//         //Delete first point if you need a filo buffer (i dont need it)
//         //xs.erase(xs.begin());
//         //xy.erase(xy.begin());

//         //Add new Data points at the end
//         xs.push_back(x);
//         ys.push_back(y);


//         // Copy the data:
//         m_xs = xs;
//         m_ys = ys;

//         // Update internal variables for the bounding box.
//         if (xs.size()>0)
//         {
//             m_minX  = xs[0];
//             m_maxX  = xs[0];
//             m_minY  = ys[0];
//             m_maxY  = ys[0];

//             std::vector<double>::const_iterator  it;

//             for (it=xs.begin();it!=xs.end();it++)
//             {
//                 if (*it<m_minX) m_minX=*it;
//                 if (*it>m_maxX) m_maxX=*it;
//             }
//             for (it=ys.begin();it!=ys.end();it++)
//             {
//                 if (*it<m_minY) m_minY=*it;
//                 if (*it>m_maxY) m_maxY=*it;
//             }
//             m_minX-=0.5f;
//             m_minY-=0.5f;
//             m_maxX+=0.5f;
//             m_maxY+=0.5f;
//         }
//         else
//         {
//             m_minX  = -1;
//             m_maxX  = 1;
//             m_minY  = -1;
//             m_maxY  = 1;
//         }
//     }



//for testing
// int main(){

//     std::vector<std::pair<double, double>> dummy;
//     std::string file_path = "test.csv";

//     read_csv(dummy, file_path);

//     return 0;
// }


//TODO: ADD BETTER ERROR CHECKING