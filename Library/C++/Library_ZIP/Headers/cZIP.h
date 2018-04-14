#include <vector>
#include <string>

#include "tZIP.h"

#define ZLIB_WINAPI
#include "zlib.h"

/**
 * @class	cZIP
 *
 * @brief	Class used to perform zipping action
 *
 * @author	Maxime Lagadec
 * @date	4/8/2018
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

class cZIP
{
public:

	// Constructor
	cZIP();
	// Constructor and zip directory or file to memory
	cZIP(std::wstring wsDirectory);
	// Constructor and zip directory or file to memory then to file
	cZIP(std::wstring wsDirectory, std::wstring wsDestination, const BOOL bFlush = TRUE);

	// Destructor (calls FlushMemory)
	virtual ~cZIP();

	// Zip directory or file to memory
	DWORD ZipToMemory(std::wstring wsDirectory);

	// Zip directory or file to memory and then to file
	// bFlush : TRUE -> Will flush memory after creating zip file
	// bFlush : FALSE -> Will not flush memory after creating zip file
	DWORD ZipToFile(std::wstring wsDirectory, std::wstring wsDestination, const BOOL bFlush = TRUE);

	// Flush all memory
	void FlushMemory();

	// Get the zipped data
	void GetZippedData(BYTE* &pbyZippedData, DWORD &dwSizeOfData) { pbyZippedData = m_vZippedData.data(); dwSizeOfData = (DWORD) m_vZippedData.size(); }
	// Get wether there's data zipped in memory or not
	BOOL GetIsThereZippedData() { return m_bZippedDataInMemory; }
	// Get wether zip failed or not after using constructor
	BOOL GetDidZipFail() { return m_bZippingFailed; }

private:

	// Recursive function used to fill buffer with zipped data
	DWORD ZIP(std::vector<BYTE> &vZippedData, std::vector<BYTE> &vCentralHeaderData, const std::wstring wsDirectory, const DWORD dwInitialDirectoryLength, const BOOL bFile);

	// Allocate buffer with the various headers of a zip file
	void AllocateLocalFileHeader(std::vector<BYTE> &vZippedData, const std::wstring wsDirectory, const DWORD dwInitialDirectoryLength, const PWIN32_FIND_DATA tPWIN32_FIND_DATA, const WORD wCompressionMethod, const DWORD dwCRC32, const DWORD dwCompressedSize, const DWORD dwUncompressedSize);
	void AllocateDataDescriptor(std::vector<BYTE> &vZippedData, const DWORD dwCRC32, const DWORD dwCompressedSize, const DWORD dwUncompressedSize);
	void AllocateCentralDirectoryFileHeader(std::vector<BYTE> &vZippedData, const std::wstring wsDirectory, const DWORD dwInitialDirectoryLength, const PWIN32_FIND_DATA tPWIN32_FIND_DATA, const WORD wCompressionMethod, const DWORD dwCRC32, const DWORD dwCompressedSize, const DWORD dwUncompressedSize, const DWORD dwOffsetLocalHeader);
	void AllocateEndOfCentralDirectoryRecord(std::vector<BYTE> &vZippedData, const WORD wNumberOfCentralDirectories, const DWORD dwSizeOfCentralDirectory, const DWORD dwOffsetStartCentralDirectory);

	// Same has zlib's compress but no zlib header
	int compressRAW(Bytef *dest, uLongf *destLen, const Bytef *source, uLong sourceLen, int level);

protected:

	BOOL m_bFile = FALSE;						/**< Set when the zipped data in memory is a file */
	BOOL m_bZippedDataInMemory = FALSE;			/**< Set when there's is zipped data in memory */
	BOOL m_bZippingFailed = FALSE;				/**< Set when zipping fail after using class constructor */

	std::wstring m_wsStoredDirectoryZip = L"";		/**< Represents the directory zipped in memory */

	std::vector<BYTE> m_vZippedData;			/**< Zipped data */

	WORD m_wNumberOfCentralDirectories = 0;		/**< Represents the number of central directories in the zipped data */
};