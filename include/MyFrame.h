#ifndef MYFRAME_H
#define MYFRAME_H

#include <wx/wx.h>


class MyFrame : public wxFrame
{
public:
    MyFrame();
    
 
private:
    wxButton *TestButton1;
    wxButton *TestButton2;
    wxButton *TestButton3;
    void OnHello(wxCommandEvent& event);
    void OnExit(wxCommandEvent& event);
    void OnAbout(wxCommandEvent& event);
    void OnButton1(wxCommandEvent& event);
    void OnButton2(wxCommandEvent& event);
    void OnButton3(wxCommandEvent& event);
};
 


enum
{
    ID_Hello = 1,
    BUTTON1_Hello = 2, // declares an id which will be used to call our button
    BUTTON2_Hello = 3, // declares an id which will be used to call our button
    BUTTON3_Hello = 4 // declares an id which will be used to call our button
};

#endif