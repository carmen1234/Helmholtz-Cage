#include <wx/wx.h>
#include <wx/textctrl.h>
#include "MyFrame.h"
#include "utils.h"
#include <string>

MyFrame::MyFrame()
    : wxFrame(nullptr, wxID_ANY, "HCageGui")
{
    wxMenu *menuFile = new wxMenu;
    menuFile->Append(ID_Hello, "&Hello...\tCtrl-H",
                     "Help string shown in status bar for this menu item");
    menuFile->AppendSeparator();
    menuFile->Append(wxID_EXIT);
 
    wxMenu *menuHelp = new wxMenu;
    menuHelp->Append(wxID_ABOUT);
 
    wxMenuBar *menuBar = new wxMenuBar;
    menuBar->Append(menuFile, "&File");
    menuBar->Append(menuHelp, "&Help");
 
    SetMenuBar( menuBar );
 
    CreateStatusBar();
    SetStatusText("Designed for UTAT");


    //for CSV file functionality
    CSVPathBox = new wxTextCtrl(this,CSVPathBoxE, _T("Type Path to CSV File Here"));
 
    Bind(wxEVT_MENU, &MyFrame::OnHello, this, ID_Hello);
    Bind(wxEVT_MENU, &MyFrame::OnAbout, this, wxID_ABOUT);
    Bind(wxEVT_MENU, &MyFrame::OnExit, this, wxID_EXIT);

    TestButton1 = new wxButton(this, BUTTON1_Hello, _T("Test1"));
    ReadCSVButton = new wxButton(this, UseCSV, _T("Import CSV"));
    TestButton3 = new wxButton(this, BUTTON3_Hello, _T("Test3"));

    ReadCSVButton->Move(0, 40, wxSIZE_USE_EXISTING);
    CSVPathBox->Move(120,40, wxSIZE_USE_EXISTING);
    TestButton3->Move(0, 80, wxSIZE_USE_EXISTING );

    //EVT_BUTTON(BUTTON_Hello, &MyFrame::OnButton);
    Bind(wxEVT_BUTTON, &MyFrame::OnButton1, this, BUTTON1_Hello);
    Bind(wxEVT_BUTTON, &MyFrame::OnCSVButton, this, UseCSV);
    Bind(wxEVT_BUTTON, &MyFrame::OnButton3, this, BUTTON3_Hello);
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
 
void MyFrame::OnHello(wxCommandEvent& event)
{
    wxLogMessage("Hello world from wxWidgets!");
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

    std::vector<std::pair<double, double>> csv_data; //note will probably need to make this a global variable or something so its scope isnt limited to this func
    read_csv(csv_data,csv_path_str); 


}

void MyFrame::OnButton3(wxCommandEvent& event)
{
    wxLogMessage("do another thing here");
}