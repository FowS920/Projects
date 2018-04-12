#include <vector>
#include <string>

#include "tZIP.h"

#define ZLIB_WINAPI
#include "zlib.h"
#include "zip.h"

/**
 * @class	cZIP
 *
 * @brief	Class used to perform zipping action
 *
 * @author	Maxime Lagadec
 * @date	4/8/2018
 *
 */
class cZIP
{
public:

	// Constructor
	cZIP();
	// Constructor and zip directory or file to memory
	cZIP(std::string sDirectory);
	// Constructor and zip directory or file to memory then to file
	cZIP(std::string sDirectory, std::string sDestination, const BOOL bFlush = TRUE);

	// Destructor (calls FlushMemory)
	virtual ~cZIP();

	// Zip directory or file to memory
	DWORD ZipToMemory(std::string sDirectory);

	// Zip directory or file to memory and then to file
	// bFlush : TRUE -> Will flush memory after creating zip file
	// bFlush : FALSE -> Will not flush memory after creating zip file
	DWORD ZipToFile(std::string sDirectory, std::string sDestination, const BOOL bFlush = TRUE);

	// Flush all memory
	void FlushMemory();

	// Get the zipped data
	void GetZippedData(BYTE* pbyZippedData, DWORD dwSizeOfData) { pbyZippedData = m_vZippedData.data(); dwSizeOfData = m_vZippedData.size(); }
	// Get wether there's data zipped in memory or not
	BOOL GetIsThereZippedData() { return m_bZippedDataInMemory; }
	// Get wether zip failed or not after using constructor
	BOOL GetDidZipFail() { return m_bZippingFailed; }

private:

	// Recursive function used to fill buffer with zipped data
	DWORD ZIP(std::vector<BYTE> &vZippedData, std::vector<BYTE> &vCentralHeaderData, const std::string sDirectory, const DWORD dwInitialDirectoryLength, const BOOL bFile);

	// Allocate buffer with the various headers of a zip file
	void AllocateLocalFileHeader(std::vector<BYTE> &vZippedData, const std::string sDirectory, const DWORD dwInitialDirectoryLength, const PWIN32_FIND_DATA tPWIN32_FIND_DATA, const WORD wCompressionMethod, const DWORD dwCRC32, const DWORD dwCompressedSize, const DWORD dwUncompressedSize);
	void AllocateDataDescriptor(std::vector<BYTE> &vZippedData, const DWORD dwCRC32, const DWORD dwCompressedSize, const DWORD dwUncompressedSize);
	void AllocateCentralDirectoryFileHeader(std::vector<BYTE> &vZippedData, const std::string sDirectory, const DWORD dwInitialDirectoryLength, const PWIN32_FIND_DATA tPWIN32_FIND_DATA, const WORD wCompressionMethod, const DWORD dwCRC32, const DWORD dwCompressedSize, const DWORD dwUncompressedSize, const DWORD dwOffsetLocalHeader);
	void AllocateEndOfCentralDirectoryRecord(std::vector<BYTE> &vZippedData, const WORD wNumberOfCentralDirectories, const DWORD dwSizeOfCentralDirectory, const DWORD dwOffsetStartCentralDirectory);

	// Same has zlib's compress but no zlib header
	int compressRAW(Bytef *dest, uLongf *destLen, const Bytef *source, uLong sourceLen, int level);

protected:

	BOOL m_bFile = FALSE;						/**< Set when the zipped data in memory is a file */
	BOOL m_bZippedDataInMemory = FALSE;			/**< Set when there's is zipped data in memory */
	BOOL m_bZippingFailed = FALSE;				/**< Set when zipping fail after using class constructor */

	std::string m_sStoredDirectoryZip = "";		/**< Represents the directory zipped in memory */

	std::vector<BYTE> m_vZippedData;			/**< Zipped data */

	WORD m_wNumberOfCentralDirectories = 0;		/**< Represents the number of central directories in the zipped data */
};