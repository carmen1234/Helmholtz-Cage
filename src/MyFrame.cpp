#include <wx/wx.h>
#include <wx/textctrl.h>
#include <wx/wfstream.h>
#include "MyFrame.h"
#include "utils.h"
#include <string>

MyFrame::MyFrame()
    : wxFrame(nullptr, wxID_ANY, "HCageGui",wxDefaultPosition)
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

    


   /*Panels*/
    XAxisPanel = new wxPanel(this,wxID_ANY,wxDefaultPosition, wxDefaultSize,wxTAB_TRAVERSAL);
    YAxisPanel = new wxPanel(this,wxID_ANY,wxDefaultPosition, wxDefaultSize,wxTAB_TRAVERSAL);
    ZAxisPanel = new wxPanel(this,wxID_ANY,wxDefaultPosition, wxDefaultSize,wxTAB_TRAVERSAL);
    /*I have no idea how to use them, they somehow work with sizers which I also dont get */
    
    

    //for CSV file functionality
    CSVPathBox = new wxTextCtrl(this,CSVPathBoxE, _T("Type Path to CSV File Here"));
    DebugBox = new wxTextCtrl(this, DebugBoxID);

    Bind(wxEVT_MENU, &MyFrame::OnImport, this, ID_IMPORT);
    Bind(wxEVT_MENU, &MyFrame::OnHowTo, this, ID_Documentation);
    Bind(wxEVT_MENU, &MyFrame::OnAbout, this, wxID_ABOUT);
    Bind(wxEVT_MENU, &MyFrame::OnExit, this, wxID_EXIT);

    TestButton1 = new wxButton(this, BUTTON1_Hello, _T("Test1"));
    
    TestButton3 = new wxButton(this, BUTTON3_Hello, _T("Test3"));
    TestButton3->Move(0, 40, wxSIZE_USE_EXISTING );

    ReadCSVButton = new wxButton(this, UseCSV, _T("Import CSV"));
    ReadCSVButton->Move(0, 80, wxSIZE_USE_EXISTING);
    CSVPathBox->Move(120,80, wxEXPAND | wxALL | wxHORIZONTAL | wxTE_CHARWRAP | wxGROW);
    
    DebugBox->SetSize(0,500,600,200, wxVERTICAL | wxGROW);
    CSVPathBox->SetSize(120,80, 250,40, wxHORIZONTAL | wxGROW);

    /*TEXT BOXES FOR READING INCOMING MAGENTIC FIELD DATA*/
    ReadMagX = new wxStaticText(this,ID_MagXRead,_T("M. Field Strength X"));
    ReadMagY = new wxStaticText(this,ID_MagYRead,_T("M. Field Strength Y"));
    ReadMagZ = new wxStaticText(this,ID_MagZRead,_T("M. Field Strength Z"));
    
    ReadMagX->Move(5, 147, wxSIZE_USE_EXISTING);
    ReadMagY->Move(5, 187, wxSIZE_USE_EXISTING);
    ReadMagZ->Move(5, 227, wxSIZE_USE_EXISTING);

    /*TODO: add functions to write to the textbox (will basically be copying the debug box)*/
    MagXInput = new wxTextCtrl(this,ID_MagXInput, _T(""),wxPoint(140,140),wxDefaultSize,wxTE_READONLY);
    MagYInput = new wxTextCtrl(this,ID_MagYInput, _T(""),wxPoint(140,180),wxDefaultSize,wxTE_READONLY);
    MagZInput = new wxTextCtrl(this,ID_MagXInput, _T(""),wxPoint(140,220),wxDefaultSize,wxTE_READONLY);

    ReadCurrent = new wxStaticText(this,ID_MagZRead,_T("Current"));
    ReadCurrent->Move(5, 267, wxSIZE_USE_EXISTING);
    CurrentInput = new wxTextCtrl(this,ID_MagXInput, _T(""),wxPoint(140,260),wxDefaultSize,wxTE_READONLY);

    //EVT_BUTTON(BUTTON_Hello, &MyFrame::OnButton);
    Bind(wxEVT_BUTTON, &MyFrame::OnButton1, this, BUTTON1_Hello);
    Bind(wxEVT_BUTTON, &MyFrame::OnCSVButton, this, UseCSV);
    Bind(wxEVT_BUTTON, &MyFrame::OnButton3, this, BUTTON3_Hello);


    //frame resizing:
    // wxBoxSizer* sizer = new wxBoxSizer(wxHORIZONTAL);
    // sizer->Add(DebugBox);
    // sizer->Add(CSVPathBox);
    // sizer->Add(ReadCSVButton);
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

void MyFrame::OnButton1(wxCommandEvent& event)
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

void MyFrame::OnButton3(wxCommandEvent& event)
{
    wxLogMessage("do another thing here");
}