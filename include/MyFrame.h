#ifndef MYFRAME_H
#define MYFRAME_H

#include <wx/wx.h>
#include <wx/textctrl.h>
#include <wx/richtext/richtextctrl.h>


class MyFrame : public wxFrame
{
public:
    MyFrame();
    
 
private:
    wxButton *XVal_SetButton;
    wxButton *YVal_SetButton;
    wxButton *ZVal_SetButton; 
    wxTextCtrl *SetX;
    wxTextCtrl *SetY;
    wxTextCtrl *SetZ;

    /*Panels*/
    wxPanel *XAxisPanel;
    wxPanel *YAxisPanel;
    wxPanel *ZAxisPanel;

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
    wxStaticText *ReadCurrentX;
    wxTextCtrl *CurrentInputX;
    wxStaticText *ReadCurrentY;
    wxTextCtrl *CurrentInputY;
    wxStaticText *ReadCurrentZ;
    wxTextCtrl *CurrentInputZ;

    //labels for X,Y,Z done with Richtext
    wxRichTextCtrl *XAxisLabel;
    wxRichTextCtrl *YAxisLabel;
    wxRichTextCtrl *ZAxisLabel;


    /*event functions*/
    void OnImport(wxCommandEvent& event);
    void OnExit(wxCommandEvent& event);
    void OnAbout(wxCommandEvent& event);
    void OnSetMagX(wxCommandEvent& event);
    void OnCSVButton(wxCommandEvent& event);
    void OnSetMagY(wxCommandEvent& event);
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
    Graph_ToggleX = 16,
    Graph_ToggleY = 17,
    Graph_ToggleZ = 18,
    Axis_LabelX = 19,
    Axis_LabelY = 20,
    Axis_LabelZ = 21,
    ID_SetMagX = 22,
    ID_SetMagY = 23,
    ID_SetMagZ = 24,
    ID_ValX = 25,
    ID_ValY = 26,
    ID_ValZ = 27
};

#endif