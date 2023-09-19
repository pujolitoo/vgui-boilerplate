#include "CMainFrame.h"

#include <vgui/IVGui.h>
#include <KeyValues.h>

CMainFrame::CMainFrame(vgui::Panel* parent, const char* name)
	: vgui::Frame(parent, name)
{
	m_MainPanel = parent;


	SetMinimumSize(310, 350);
	SetSize(310, 350);
	MoveToCenterOfScreen();
	SetSizeable(false);
	SetTitle("Hello World!", true);

	SetMinimizeButtonVisible(true);

	LoadComponents();

}

void CMainFrame::LoadComponents()
{
	button1 = new vgui::Button(this, "OKBUTTON", "OK");
	button1->SetCommand("OK");
	button1->DrawFocusBox(true);
	button1->SetPos(160, 310);

	m_cancelButton = new vgui::Button(this, "CANCELBUTTON", "Cancel");
	m_cancelButton->SetPos(230, 310);
	m_cancelButton->SetCommand("CANCEL");

}

void CMainFrame::OnCommand(const char* command)
{
	if (!stricmp("CANCEL", command) ||
		!stricmp("Close", command))
	{
		vgui::ivgui()->PostMessage(m_MainPanel->GetVPanel(), new KeyValues("Quit"), NULL);
		Close();
		vgui::ivgui()->Stop();
	}
	else if (!stricmp("OK", command))
	{
		FlashWindow();
	}
}


CMainFrame::~CMainFrame()
{

}