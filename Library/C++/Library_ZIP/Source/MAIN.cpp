#include "cUNZIP.h"
#include "cZIP.h"

#include "TString.h"

int main()
{
	cZIP clZIP = cZIP();
	clZIP.ZipToMemory(L"C:\\Projects\\KEK420");

	BYTE* pbyData;
	DWORD dwSize;

	clZIP.GetZippedData(pbyData, dwSize);

	HANDLE hFile;
	hFile = CreateFile(
		L"C:\\Projects\\KEK420.zip",
		GENERIC_READ,
		FILE_SHARE_READ | FILE_SHARE_WRITE,
		NULL,
		OPEN_EXISTING,
		FILE_ATTRIBUTE_NORMAL,
		NULL
	);

	cUNZIP clUNZIP = cUNZIP();
	clUNZIP.UnzipToFolder(L"C:\\Projects\\WOW\\", hFile);

	return 0;
}

