#include <vector>
#include <string>

#include "tZIP.h"

#define ZLIB_WINAPI
#include "zlib.h"
#include "zip.h"

class cZIP
{
public:

	DWORD ZipToMemory(std::string sDirectory);
	DWORD ZipToFile(std::string sDirectory, std::string sDestination);

private:

	DWORD ZIP(std::vector<BYTE> &vZippedData, std::vector<BYTE> &vCentralHeaderData, std::string sDirectory, DWORD dwInitialDirectoryLength, BOOL bFile);

	void AllocateLocalFileHeader(std::vector<BYTE> &vZippedData, const std::string sDirectory, const DWORD dwInitialDirectoryLength, const PWIN32_FIND_DATA tPWIN32_FIND_DATA);
	void AllocateDataDescriptor(std::vector<BYTE> &vZippedData, const DWORD dwCRC32, const DWORD dwCompressedSize, const DWORD dwUncompressedSize);
	void AllocateCentralDirectoryFileHeader(std::vector<BYTE> &vZippedData, const std::string sDirectory, const DWORD dwInitialDirectoryLength, const PWIN32_FIND_DATA tPWIN32_FIND_DATA, const DWORD dwCRC32, const DWORD dwCompressedSize, const DWORD dwUncompressedSize, const DWORD dwOffsetLocalHeader);
	void AllocateEndOfCentralDirectoryRecord(std::vector<BYTE> &vZippedData, const WORD wNumberOfCentralDirectories, const DWORD dwSizeOfCentralDirectory, const DWORD dwOffsetStartCentralDirectory);

protected:

	BOOL m_bFile = FALSE;
	BOOL m_bZippedDataInMemory = FALSE;

	std::string m_sStoredDirectoryZip = "";

	std::vector<BYTE> m_vZippedData;

	WORD m_wNumberOfCentralDirectories = 0;
};