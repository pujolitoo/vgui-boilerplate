// teesst.cpp : This file contains the 'main' function. Program execution begins and ends there.
//

#include <iostream>
#include <Windows.h>
#include<direct.h>

#include <vgui_controls/Panel.h>
#include <vgui_controls/Controls.h>
#include <vgui/ISystem.h>
#include <vgui/IVGui.h>
#include <vgui/IPanel.h>
#include <interface.h>
#include "tier0/dbg.h"
#include "filesystem.h"
#include <vgui/ILocalize.h>
#include <vgui/IScheme.h>
#include <vgui/ISurface.h>
#include <appframework/AppFramework.h>
#include "appframework/tier3app.h"
#include <memory>

#include "CMainPanel.h"

#include <tier0/memdbgoff.h>

#define FILESYSTEM_MODULE_NAME "FileSystem_Stdio.dll"

CSysModule* g_pFileSystemModule = NULL;
CMainPanel* g_pMainPanel = NULL;

class CTestAppSystemGroup : public CVguiSteamApp
{
public:
	virtual bool Create()
	{
		AppSystemInfo_t modules[] =
		{
			{"vgui2.dll", VGUI_IVGUI_INTERFACE_VERSION},
			{"", ""}
		};
		return this->AddSystems(modules);
	}
	virtual bool PreInit()
	{
		if (!CVguiSteamApp::PreInit())
		{
			return false;
		}
	}
	virtual int Main()
	{
		g_pFullFileSystem->AddSearchPath(".", "MAIN");
		g_pFullFileSystem->AddSearchPath("platform", "PLATFORM", PATH_ADD_TO_HEAD);

		vgui::ivgui()->SetSleep(false);

		g_pMainPanel = new CMainPanel();

		g_pMainPanel->SetVisible(true);

		vgui::surface()->SetEmbeddedPanel(g_pMainPanel->GetVPanel());

		g_pVGuiLocalize->AddFile("Resource/platform_spanish.txt");
		g_pVGuiLocalize->AddFile("Resource/vgui_spanish.txt");

		vgui::scheme()->LoadSchemeFromFile("Resource/SourceScheme.res", "SourceScheme");

		vgui::ivgui()->Start();

		g_pMainPanel->Initialize();
		g_pMainPanel->Open();

		vgui::ivgui()->RunFrame();
		while (vgui::ivgui()->IsRunning())
		{
			vgui::ivgui()->RunFrame();
		}

		return 0;
	}
	virtual void PostShutdown()
	{
		delete g_pMainPanel;
		g_pMainPanel = NULL;
		CVguiSteamApp::PostShutdown();
	}
	virtual void Destroy()
	{

	}

	// Used to chain to base class
	AppModule_t LoadModule(CreateInterfaceFn factory)
	{
		return CSteamAppSystemGroup::LoadModule(factory);
	}

	// Method to add various global singleton systems 
	bool AddSystems(AppSystemInfo_t* pSystems)
	{
		return CSteamAppSystemGroup::AddSystems(pSystems);
	}

	void* FindSystem(const char* pInterfaceName)
	{
		return CSteamAppSystemGroup::FindSystem(pInterfaceName);
	}
};

class CTestApplication : public CSteamApplication
{
public:
	CTestApplication(CTestAppSystemGroup* appsystemGroup) : CSteamApplication(appsystemGroup)
	{
	}
	virtual bool Create()
	{
		AppModule_t filesystemModule = LoadModule(FILESYSTEM_MODULE_NAME);
		m_pFileSystem = (IFileSystem*)AddSystem(filesystemModule, FILESYSTEM_INTERFACE_VERSION);
		if (!m_pFileSystem)
		{
			Warning("Unable to load the file system!\n");
			return false;
		}
		return true;
	}
};

int WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, LPSTR lpCmdLine, int nCmdShow)
{
	CTestAppSystemGroup testSystems;
	CTestApplication testApplication(&testSystems);
	return 	testApplication.Run();
}

