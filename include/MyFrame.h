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
    wxButton *TestButton3;

    /*CSV Functionality*/
    wxButton *ReadCSVButton;
    wxTextCtrl *CSVPathBox;

    /*Debug dialogue, WIP*/
    wxTextCtrl *DebugBox;

    /*Read Magnetic Field Input (from magnanenomter)*/
    wxStaticText *ReadMagX;
    wxStaticText *ReadMagY;
    wxStaticText *ReadMagZ;
    wxTextCtrl *MagXInput;
    wxTextCtrl *MagYInput;
    wxTextCtrl *MagZInput;

    /*Read Current (from current sensor)*/
    wxStaticText *ReadCurrent;
    wxTextCtrl *CurrentInput;

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
    DebugBoxID = 7,
    ID_MagXRead = 8,
    ID_MagYRead = 9,
    ID_MagZRead = 10,
    ID_MagXInput = 11,
    ID_MagYInput = 12,
    ID_MagZInput = 13,
    ID_CurrentRead = 14,
    ID_CurrentInput = 15,

};

#endif