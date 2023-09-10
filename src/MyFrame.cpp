#include <wx/wx.h>
#include "MyFrame.h"

MyFrame::MyFrame()
    : wxFrame(nullptr, wxID_ANY, "Hello World")
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
    SetStatusText("Welcome to wxWidgets!");
 
    Bind(wxEVT_MENU, &MyFrame::OnHello, this, ID_Hello);
    Bind(wxEVT_MENU, &MyFrame::OnAbout, this, wxID_ABOUT);
    Bind(wxEVT_MENU, &MyFrame::OnExit, this, wxID_EXIT);

    TestButton1 = new wxButton(this, BUTTON1_Hello, _T("Test1"));
    TestButton2 = new wxButton(this, BUTTON2_Hello, _T("Test2"));
    TestButton3 = new wxButton(this, BUTTON3_Hello, _T("Test3"));

    TestButton2->Move(0, 40, wxSIZE_USE_EXISTING );
    TestButton3->Move(0, 80, wxSIZE_USE_EXISTING );

    //EVT_BUTTON(BUTTON_Hello, &MyFrame::OnButton);
    Bind(wxEVT_BUTTON, &MyFrame::OnButton1, this, BUTTON1_Hello);
    Bind(wxEVT_BUTTON, &MyFrame::OnButton2, this, BUTTON2_Hello);
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

void MyFrame::OnButton2(wxCommandEvent& event)
{
    wxLogMessage("do something else here");
}

void MyFrame::OnButton3(wxCommandEvent& event)
{
    wxLogMessage("do another thing here");
}