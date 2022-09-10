#pragma once
#include <vgui_controls/Frame.h>
#include <vgui_controls/Button.h>
#include <vgui_controls/TextEntry.h>

class CMainFrame : public vgui::Frame
{
	DECLARE_CLASS_SIMPLE(CMainFrame, vgui::Frame);

public:
	CMainFrame(vgui::Panel* parent, const char* name);
	~CMainFrame();

	virtual void OnCommand(const char* command);


private:

	void LoadComponents();

	vgui::Button* button1;
	vgui::Button* m_cancelButton;

	vgui::Panel* m_MainPanel = nullptr;
};

