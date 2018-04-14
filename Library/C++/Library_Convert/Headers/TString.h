#include "windows.h"

#include <string>
#include <vector>

#ifdef __CODE_PAGE_UTF8_
#define CodePage	CP_UTF8
#else
//#define CodePage	CP_ACP       
#define CodePage	CP_OEMCP     
//#define CodePage	CP_MACCP     
//#define CodePage	CP_THREAD_ACP
//#define CodePage	CP_SYMBOL   
#endif   

#ifdef _UNICODE
#define	ToTString	ToWString
#else
#define ToTString	ToString
#endif

#ifndef __LIBRARY_CONVERT_TSTRING_

inline std::wstring ToWString(LPCSTR pstrString)
{
	std::vector<WCHAR> vwstrString;

	int iBuffSize = MultiByteToWideChar(CodePage, MB_PRECOMPOSED, pstrString, -1, NULL, 0);

	vwstrString.resize(iBuffSize);

	MultiByteToWideChar(CodePage, MB_PRECOMPOSED, pstrString, -1, vwstrString.data(), iBuffSize);

	return (std::wstring) vwstrString.data();
}

inline std::wstring ToWString(LPCWSTR pwstrString)
{
	return (std::wstring) pwstrString;
}

inline std::wstring ToWString(std::string sString)
{
	std::vector<WCHAR> vwstrString;

	int iBuffSize = MultiByteToWideChar(CodePage, MB_PRECOMPOSED, sString.c_str(), -1, NULL, 0);

	vwstrString.resize(iBuffSize);

	MultiByteToWideChar(CodePage, MB_PRECOMPOSED, sString.c_str(), -1, vwstrString.data(), iBuffSize);

	return (std::wstring) vwstrString.data();
}

inline std::wstring ToWString(std::wstring wsString)
{
	return wsString;
}

inline std::string ToString(LPCSTR pstrString)
{
	return (std::string) pstrString;
}

inline std::string ToString(LPCWSTR pwcString)
{
	std::vector<CHAR> vstrString;

	int iBuffSize = WideCharToMultiByte(CodePage, NULL, pwcString, -1, NULL, 0, NULL, NULL);

	vstrString.resize(iBuffSize);

	WideCharToMultiByte(CodePage, NULL, pwcString, -1, vstrString.data(), iBuffSize, NULL, NULL);

	return (std::string) vstrString.data();
}

inline std::string ToString(std::string sString)
{
	return sString;
}

inline std::string ToString(std::wstring wsString)
{
	std::vector<CHAR> vstrString;

	int iBuffSize = WideCharToMultiByte(CodePage, NULL, wsString.c_str(), -1, NULL, 0, NULL, NULL);

	vstrString.resize(iBuffSize);

	WideCharToMultiByte(CodePage, NULL, wsString.c_str(), -1, vstrString.data(), iBuffSize, NULL, NULL);

	return (std::string) vstrString.data();
}

#endif

#ifndef __LIBRARY_CONVERT_TSTRING_
#define __LIBRARY_CONVERT_TSTRING_
#endif