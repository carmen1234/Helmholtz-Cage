#include <wx/wx.h>
#include <wx/textctrl.h>
#include <wx/wfstream.h>
#include "MyFrame.h"
#include "utils.h"
#include <string>

MyFrame::MyFrame()
    : wxFrame(nullptr, wxID_ANY, "HCageGui",wxDefaultPosition, wxSize(720,1280))
{
    wxMenu *menuFile = new wxMenu;
    menuFile->Append(ID_IMPORT, "&Import CSV File\tCtrl-M",
                     "Help string shown in status bar for this menu item");
    menuFile->AppendSeparator();
    menuFile->Append(wxID_EXIT);
 
    wxMenu *menuHelp = new wxMenu;
    menuHelp->Append(wxID_ABOUT);
    menuHelp->Append(ID_Documentation, "&How to Use\tCtrl-D",
                    "Help string shown in status bar for this menu item");
 
    wxMenuBar *menuBar = new wxMenuBar;
    menuBar->Append(menuFile, "&File");
    menuBar->Append(menuHelp, "&Help");
 
    SetMenuBar( menuBar );
 
    CreateStatusBar();
    SetStatusText("Designed for UTAT");

    
    /*Labels for Axis Data*/
    XAxisLabel = new wxRichTextCtrl(this,Axis_LabelX,wxEmptyString,wxDefaultPosition,wxSize(350,35),wxTE_READONLY);
    XAxisLabel->BeginAlignment(wxTEXT_ALIGNMENT_CENTRE);
    XAxisLabel->BeginFontSize(16);
    XAxisLabel->WriteText(wxT("                     X-Axis"));
    XAxisLabel->GetCaret()->Hide(); //hide the stupid blinking | in front of text
    XAxisLabel->SetBackgroundColour(0xF7E9DC);
    

    YAxisLabel = new wxRichTextCtrl(this,Axis_LabelX,wxEmptyString,wxPoint(0,160),wxSize(350,35),wxTE_READONLY);
    YAxisLabel->BeginAlignment(wxTEXT_ALIGNMENT_CENTRE);
    YAxisLabel->BeginFontSize(16);
    YAxisLabel->WriteText(wxT("                     Y-Axis"));
    YAxisLabel->GetCaret()->Hide(); //hide the stupid blinking | in front of text
    YAxisLabel->SetBackgroundColour(0xF7E9DC);

    ZAxisLabel = new wxRichTextCtrl(this,Axis_LabelX,wxEmptyString,wxPoint(0,320),wxSize(350,35),wxTE_READONLY);
    ZAxisLabel->BeginAlignment(wxTEXT_ALIGNMENT_CENTRE);
    ZAxisLabel->BeginFontSize(16);
    ZAxisLabel->WriteText(wxT("                     Z-Axis"));
    ZAxisLabel->GetCaret()->Hide(); //hide the stupid blinking | in front of text
    ZAxisLabel->SetBackgroundColour(0xF7E9DC);
    
    
    

    //for CSV file functionality
    CSVPathBox = new wxTextCtrl(this,CSVPathBoxE, _T("Type Path to CSV File Here"));
    DebugBox = new wxTextCtrl(this, DebugBoxID);

    Bind(wxEVT_MENU, &MyFrame::OnImport, this, ID_IMPORT);
    Bind(wxEVT_MENU, &MyFrame::OnHowTo, this, ID_Documentation);
    Bind(wxEVT_MENU, &MyFrame::OnAbout, this, wxID_ABOUT);
    Bind(wxEVT_MENU, &MyFrame::OnExit, this, wxID_EXIT);

    XVal_SetButton = new wxButton(this, ID_SetMagX , _T("Set Value"));
    XVal_SetButton->Move(40, 120, wxSIZE_USE_EXISTING );
    XVal_SetButton->SetBackgroundColour(0x886421);
    XVal_SetButton->SetForegroundColour(0xFFFFFF); //foreground is text
    YVal_SetButton = new wxButton(this, ID_SetMagY, _T("Set Value"));
    YVal_SetButton->Move(40, 280, wxSIZE_USE_EXISTING );
    YVal_SetButton->SetBackgroundColour(0x886421);
    YVal_SetButton->SetForegroundColour(0xFFFFFF); //foreground is text
    ZVal_SetButton = new wxButton(this, ID_SetMagZ, _T("Set Value"));
    ZVal_SetButton->Move(40, 440, wxSIZE_USE_EXISTING );
    ZVal_SetButton->SetBackgroundColour(0x886421);
    ZVal_SetButton->SetForegroundColour(0xFFFFFF); //foreground is text

    SetX = new wxTextCtrl(this,ID_ValX, _T(""),wxPoint(160,120),wxDefaultSize);
    SetY = new wxTextCtrl(this,ID_ValY, _T(""),wxPoint(160,280),wxDefaultSize);
    SetZ = new wxTextCtrl(this,ID_ValZ, _T(""),wxPoint(160,440),wxDefaultSize);
    

    ReadCSVButton = new wxButton(this, UseCSV, _T("Import CSV"));
    ReadCSVButton->Move(350, 80, wxSIZE_USE_EXISTING);
    CSVPathBox->Move(400,80, wxEXPAND | wxALL | wxHORIZONTAL | wxTE_CHARWRAP | wxGROW);
    
    DebugBox->SetSize(0,500,350,200, wxVERTICAL | wxGROW);
    CSVPathBox->SetSize(400,80, 250,40, wxHORIZONTAL | wxGROW);

    /*TEXT BOXES FOR READING INCOMING MAGENTIC FIELD DATA*/
    ReadMagX = new wxStaticText(this,ID_MagXRead,_T("M. Field Strength"));
    ReadMagY = new wxStaticText(this,ID_MagYRead,_T("M. Field Strength"));
    ReadMagZ = new wxStaticText(this,ID_MagZRead,_T("M. Field Strength"));
    
    ReadMagX->Move(40, 50, wxSIZE_USE_EXISTING);
    ReadMagY->Move(40, 210, wxSIZE_USE_EXISTING);
    ReadMagZ->Move(40, 370, wxSIZE_USE_EXISTING);

    /*TODO: add functions to write to the textbox (will basically be copying the debug box)*/
    MagXInput = new wxTextCtrl(this,ID_MagXInput, _T(""),wxPoint(160,43),wxDefaultSize,wxTE_READONLY);
    MagYInput = new wxTextCtrl(this,ID_MagYInput, _T(""),wxPoint(160,203),wxDefaultSize,wxTE_READONLY);
    MagZInput = new wxTextCtrl(this,ID_MagXInput, _T(""),wxPoint(160,363),wxDefaultSize,wxTE_READONLY);

    ReadCurrentX = new wxStaticText(this,ID_MagZRead,_T("Current"));
    ReadCurrentX->Move(55, 90, wxSIZE_USE_EXISTING);
    CurrentInputX = new wxTextCtrl(this,ID_MagXInput, _T(""),wxPoint(160,83),wxDefaultSize,wxTE_READONLY);
    ReadCurrentY = new wxStaticText(this,ID_MagZRead,_T("Current"));
    ReadCurrentY->Move(55, 250, wxSIZE_USE_EXISTING);
    CurrentInputY = new wxTextCtrl(this,ID_MagXInput, _T(""),wxPoint(160,243),wxDefaultSize,wxTE_READONLY);
    ReadCurrentZ = new wxStaticText(this,ID_MagZRead,_T("Current"));
    ReadCurrentZ->Move(55, 410, wxSIZE_USE_EXISTING);
    CurrentInputZ = new wxTextCtrl(this,ID_MagXInput, _T(""),wxPoint(160,403),wxDefaultSize,wxTE_READONLY);


    //EVT_BUTTON(BUTTON_Hello, &MyFrame::OnButton);
    Bind(wxEVT_BUTTON, &MyFrame::OnSetMagX, this, ID_SetMagX);
    Bind(wxEVT_BUTTON, &MyFrame::OnCSVButton, this, UseCSV);
    Bind(wxEVT_BUTTON, &MyFrame::OnSetMagY, this, ID_SetMagY);


    



    //frame resizing:
    // wxBoxSizer* sizer = new wxBoxSizer(wxHORIZONTAL);
    // sizer->Add(XAxisLabel);
    // sizer->Add(YAxisLabel);
    // sizer->Add(ZAxisLabel);
    
    // this->SetSizer(sizer);
    // Fit();
    // Centre();
    this->Fit(); //this works on its own, i don't understand how to use sizers lol
}
 
void MyFrame::OnExit(wxCommandEvent& event)
{
    Close(true);
}
 
void MyFrame::OnAbout(wxCommandEvent& event)
{
    wxMessageBox("This is a wxWidgets Hello World example",
                 "About Hello World", wxOK | wxICON_INFORMATION);
}
 
void MyFrame::OnImport(wxCommandEvent& event)
{
    //wxLogMessage("Hello world from wxWidgets!");
    wxFileDialog openFileDiaglogue(this, _("Import CSV File"), "", "",
                         "CSV files (*.csv)|*.csv", wxFD_OPEN|wxFD_FILE_MUST_EXIST);
    if(openFileDiaglogue.ShowModal() == wxID_CANCEL){
        return;
    }

    //use filestream functions directly from wxWidgets
    wxFileInputStream input_csv_file(openFileDiaglogue.GetPath());
    if(!input_csv_file.IsOk()){
        //error_handlung
    }


    //OPTION 1: Use FileStream funcs from wxWidgets first, just output messages to a debug console or something 
    //OPTION 2: Use GetPath to get path to file, then have logic similar to CSV button and only process data once we click a button...
    
    //Probably a 3rd option thats a mix, will decide later
    
    
}

void MyFrame::OnSetMagX(wxCommandEvent& event)
{
    wxLogMessage("do something here");
}

void MyFrame::OnCSVButton(wxCommandEvent& event)
{
    //wxLogMessage("do something else here");

    //On button press, we should read from the text box to get path
    wxString csv_path = this->CSVPathBox->GetValue();
    
    //wxLogMessage(csv_path); //for debugging
    
    std::string csv_path_str = csv_path.ToStdString();
    std::string error_status = "";
    std::vector<std::pair<double, double>> csv_data; //note will probably need to make this a global variable or something so its scope isnt limited to this func
    read_csv(csv_data,csv_path_str,error_status); 
    
    wxString error_wxString(error_status);
    this->DebugBox->SetValue(error_wxString);

   
}

void MyFrame::OnHowTo(wxCommandEvent& event)
{

}

void MyFrame::OnSetMagY(wxCommandEvent& event)
{
    wxLogMessage("do another thing here");
}