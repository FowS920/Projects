#include <vector>
#include <string>

#include "tZIP.h"

#define ZLIB_WINAPI
#include "zlib.h"

/**
 * @class	cUNZIP
 *
 * @brief	Class used to perform unzipping actions
 *
 * @author	Maxime Lagadec
 * @date	4/14/2018
 *
 * @note	Intended usage is for relatively small to medium files (ideally under 500 MB, maximum is up to 1 GB)
 * @note	Large files can take more memory and this could lead to bad_allocation exceptions
 *
 * @note	When using files with UNICODE characters, be careful when exporting to different OS...!
 * @note	If they don't use the same Code Page, the files' names can be messed up
 *
 * @todo	Implement BOOST for file creation and read/write (compatible with other OS then windows)
 *
 */

class cUNZIP
{
public:

	// Unzip target data into target destination
	DWORD UnzipToFolder(const std::wstring wsSource, const std::wstring wsDestination);
	DWORD UnzipToFolder(const std::wstring wsDestination, BYTE* pbyData, DWORD dwSize);
	DWORD UnzipToFolder(const std::wstring wsDestination, HANDLE hZipFile);

	// Flush all internal memory
	void FlushMemory();

private:

	// Load a zip file's informations
	DWORD LoadZIPStructure(BYTE* pbyData, DWORD dwSize);
	DWORD LoadZIPStructure(HANDLE hZipFile);

	// Create a zipped file location
	DWORD CreateExtractFile(const std::wstring wsDirectory, const DWORD dwFileNumber);

	// Extract compressed data to previously created zip file
	DWORD ExtractFile(const std::wstring wsDirectory, const DWORD dwFileNumber, BYTE* pbyData);
	DWORD ExtractFile(const std::wstring wsDirectory, const DWORD dwFileNumber, HANDLE hZipFile);

	// Update existing zipped file's time and date
	DWORD UpdateFileTimeDate(const std::wstring wsDirectory, const DWORD dwFileNumber);

	// Create a file's / folder's root path
	DWORD CreateRootPath(const std::wstring wsFile);

	// Uncompress RAW compressed data
	int uncompressRAW(Bytef *dest, uLongf *destLen, const Bytef *source, uLong sourceLen);

protected:

	std::vector<LOCAL_FILE_HEADER> m_vLOCAL_FILE_HEADER;							/**< Vector with all local file headers */
	std::vector<CENTRAL_DIRECTORY_FILE_HEADER> m_vCENTRAL_DIRECTORY_FILE_HEADER;	/**< Vector with all central directory headers */

	END_OF_CENTRAL_DIRECTORY_RECORD m_tEND_OF_CENTRAL_DIRECTORY_RECORD;				/**< End of central directory header */
};