#pragma once

#include <vgui_controls/Frame.h>
#include <vgui_controls/Panel.h>
#include <vgui_controls/ListPanel.h>
#include <vgui_controls/PHandle.h>
#include "CMainFrame.h"

class CMainPanel : public vgui::Panel
{
public:
	CMainPanel();
	virtual				~CMainPanel();

	virtual void		Initialize();


	// displays the dialog, moves it into focus, updates if it has to
	virtual void		Open(void);


private:

	virtual void OnClose();

	vgui::DHANDLE<vgui::ProgressBox> m_pProgressBox;
	CMainFrame* p_MainFrame;
};

