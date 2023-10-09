#ifndef MYFRAME_H
#define MYFRAME_H

#include <wx/wx.h>
#include <wx/textctrl.h>


class MyFrame : public wxFrame
{
public:
    MyFrame();
    
 
private:
    wxButton *TestButton1;
    wxButton *ReadCSVButton;
    wxButton *TestButton3;
    wxTextCtrl *CSVPathBox;
    wxTextCtrl *DebugBox;
    void OnImport(wxCommandEvent& event);
    void OnExit(wxCommandEvent& event);
    void OnAbout(wxCommandEvent& event);
    void OnButton1(wxCommandEvent& event);
    void OnCSVButton(wxCommandEvent& event);
    void OnButton3(wxCommandEvent& event);
    void OnHowTo(wxCommandEvent& event);
};
 


enum
{
    ID_IMPORT = 1,
    BUTTON1_Hello = 2, // declares an id which will be used to call our button
    UseCSV = 3, // declares an id which will be used to call our button
    BUTTON3_Hello = 4, // declares an id which will be used to call our button
    CSVPathBoxE = 5,
    ID_Documentation = 6, 
    DebugBoxID = 7
};

#endif