// Start of wxWidgets "Hello World" Program
#include <wx/wx.h>
#include <MyFrame.h>
 
class MyApp : public wxApp
{
public:
    bool OnInit() override;
};
 
wxIMPLEMENT_APP(MyApp);
 

 
bool MyApp::OnInit()
{
    MyFrame *frame = new MyFrame();
    frame->Show(true);
    return true;
}
 
