#include <iostream>
#include <vector>
#include <ctime>
#include <chrono>
#include <utility>
#include <cmath>

/*LINUX*/
#include <unistd.h>
unsigned int s_to_us = 1000000;

/*WINDOWS*/
//#include <windows.h>

#define end_time 5

int main(){
    const auto start = std::chrono::system_clock::now(); //get start time

    double time_elapsed = 0; 

    std::vector<std::pair<double,double>> time_sine_pair; //vector of pairs, each pair is (x,y) = (x,sine(x)) 
    do {

        //get x,y vals, add to vector
        double y = sin(time_elapsed);
        std::pair<double,double> curr_x_y(time_elapsed,y); 
        time_sine_pair.push_back(curr_x_y);

        //wait like 2tenths of a second so as not to generate a trillion values
        usleep(0.2*s_to_us); //linux, commnent if on windows

        //Sleep(200); //windows


        //update time
        auto curr_time = std::chrono::system_clock::now();
        std::chrono::duration<double> dur = (curr_time-start);
        time_elapsed = dur.count();
    }while(time_elapsed < end_time); //change end_time in define
        
    /*for debugging*/
    // for(int pair = 0; pair < time_sine_pair.size() ; pair++){
    //     std::cout << "x (second) = " << time_sine_pair[pair].first << ", y (sine(x)) = " << time_sine_pair[pair].second << std::endl;
    // }

    

    return 0;
}