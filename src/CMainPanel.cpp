#include "CMainPanel.h"

#include <windows.h>
// base vgui interfaces
#include <vgui/vgui.h>
#include <vgui_controls/Panel.h>
#include <vgui/IVGui.h>
#include <vgui/ISurface.h>
#include <vgui/Cursor.h>
#include <vgui_controls/ProgressBox.h>

#include <vgui/IVGui.h>

#include "tier0/memdbgon.h"


CMainPanel::CMainPanel() : Panel(NULL, "CMainPanel")
{
	SetPaintBackgroundEnabled(false);
	SetFgColor(Color(0, 0, 0, 0));
}

CMainPanel::~CMainPanel()
{

}


void CMainPanel::Initialize()
{

	p_MainFrame = new CMainFrame(this, "CMainPanel");
	MoveToFront();

}

void CMainPanel::Open(void)
{
	p_MainFrame->SetVisible(true);
	p_MainFrame->Activate();
}

void CMainPanel::OnClose()
{
	vgui::ivgui()->Stop();
}
