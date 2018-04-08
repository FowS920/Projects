#include <algorithm>

#include "cZIP.h"

#define SUCCESS	0x0000;
#define ERROR	0x0001;

DWORD cZIP::ZipToMemory(std::string sDirectory)
{
	DWORD dwSizeOfCentralDirectory;
	DWORD dwOffsetStartCentralDirectory;

	// Reset memory
	m_bZippedDataInMemory = FALSE;
	m_sStoredDirectoryZip = "";
	m_vZippedData.clear();
	m_wNumberOfCentralDirectories = 0;

	// Swap all / to \\ in case (we use \\ for coding and / for storing)
	std::replace(sDirectory.begin(), sDirectory.end(), "/", "\\");

	// Make sure directory has no double backslash ("\\\\") except for drive
	if (sDirectory.find(":\\\\") != std::string::npos)
	{
		if (sDirectory.substr(sDirectory.find(":\\\\") + 2).find("\\\\") != std::string::npos)
			return ERROR;
	}
	else
	{
		if (sDirectory.find("\\\\") != std::string::npos)
			return ERROR;
	}

	// Make sure directory (or file) exists
	{
		HANDLE hFile;

		PWIN32_FIND_DATA tPWIN32_FIND_DATA;

		hFile = FindFirstFile(sDirectory.c_str(), tPWIN32_FIND_DATA);

		if (hFile == INVALID_HANDLE_VALUE)
			return ERROR;

		m_bFile = !(FILE_ATTRIBUTE_DIRECTORY == tPWIN32_FIND_DATA->dwFileAttributes & FILE_ATTRIBUTE_DIRECTORY);
	}

	// Call ZIP function
	{
		std::vector<BYTE> vCentralHeaderData;
	
		if (ZIP(m_vZippedData, vCentralHeaderData, sDirectory, sDirectory.rfind("\\") + 2, m_bFile))
		{
			// Reset memory
			m_bZippedDataInMemory = FALSE;
			m_sStoredDirectoryZip = "";
			m_vZippedData.clear();
			m_wNumberOfCentralDirectories = 0;
			return ERROR;
		}

		dwSizeOfCentralDirectory = vCentralHeaderData.size();
		dwOffsetStartCentralDirectory = m_vZippedData.size();

		// Copy to memory
		m_vZippedData.resize(m_vZippedData.size() + vCentralHeaderData.size());
		memcpy(m_vZippedData.data() + m_vZippedData.size() - vCentralHeaderData.size(), vCentralHeaderData.data(), vCentralHeaderData.size());
	}

	AllocateEndOfCentralDirectoryRecord(m_vZippedData, m_wNumberOfCentralDirectories, dwSizeOfCentralDirectory, dwOffsetStartCentralDirectory);

	m_sStoredDirectoryZip = sDirectory;
	m_bZippedDataInMemory = TRUE;
}

DWORD cZIP::ZipToFile(std::string sDirectory, std::string sDestination)
{
	// TODO : Check if destination is valid
	{
	
	}

	if (!(m_bZippedDataInMemory && (m_sStoredDirectoryZip == sDirectory)))
		if (ZipToMemory(sDestination))
			return ERROR;

	// TODO : Write to file
	{
	
	}
}

DWORD cZIP::ZIP(std::vector<BYTE> &vZippedData, std::vector<BYTE> &vCentralHeaderData, std::string sDirectory, DWORD dwInitialDirectoryLength, BOOL bFile)
{
	HANDLE hFile;
	HANDLE hOpenedFile;

	PWIN32_FIND_DATA tPWIN32_FIND_DATA;

	std::string sFileName;
	std::string sFile;

	std::string sSearchDirectory;
	std::string sNewDirectory;

	if (bFile)
		sSearchDirectory = sDirectory;
	else
		sSearchDirectory = sDirectory + "\\*";

	hFile = FindFirstFile(sSearchDirectory.c_str(), tPWIN32_FIND_DATA);

	if (hFile == INVALID_HANDLE_VALUE)
		return ERROR;

	do
	{
		sFileName = tPWIN32_FIND_DATA->cFileName;

		// We don't want to add DOS files (. and ..)
		if ((sFileName.find(".") != std::string::npos) || (sFileName.find("..") != std::string::npos))
		{
			continue;
		}
		// We found a directory (go deeper)
		else if (FILE_ATTRIBUTE_DIRECTORY == (tPWIN32_FIND_DATA->dwFileAttributes & FILE_ATTRIBUTE_DIRECTORY))
		{
			DWORD dwOffsetLocalHeader;

			sNewDirectory = sDirectory + "\\" + tPWIN32_FIND_DATA->cFileName;

			// Add to header
			dwOffsetLocalHeader = vZippedData.size();

			AllocateLocalFileHeader(vZippedData, sNewDirectory + "\\", dwInitialDirectoryLength, tPWIN32_FIND_DATA);
		  //AllocateDataDescriptor(vZippedData, 0x00000000, 0x00000000, 0x00000000);
			AllocateCentralDirectoryFileHeader(vCentralHeaderData, sNewDirectory + "\\", dwInitialDirectoryLength, tPWIN32_FIND_DATA, 0x00000000, 0x00000000, 0x00000000, dwOffsetLocalHeader);

			if (ZIP(vZippedData, vCentralHeaderData, sNewDirectory, dwInitialDirectoryLength, FALSE))
				return ERROR;
		}
		// We found a file (zip it)
		else
		{
			DWORD dwCRC32;
			DWORD dwCompressedSize;
			DWORD dwUncompressedSize;
			DWORD dwOffsetLocalHeader;

			DWORD dwNumberOfBytesRead;

			std::vector<BYTE> byCompressedBuffer;

			dwOffsetLocalHeader = vZippedData.size();

			AllocateLocalFileHeader(vZippedData, sDirectory, dwInitialDirectoryLength, tPWIN32_FIND_DATA);

			dwUncompressedSize = tPWIN32_FIND_DATA->nFileSizeHigh * (MAXDWORD + 1) + tPWIN32_FIND_DATA->nFileSizeLow;
			dwCompressedSize = compressBound(dwUncompressedSize);

			byCompressedBuffer.resize(dwCompressedSize);

			{
				std::vector<BYTE> byUncompressedBuffer;
				byUncompressedBuffer.resize(dwUncompressedSize);

				// Read file to buffer
				sFile = sDirectory + "\\" + tPWIN32_FIND_DATA->cFileName;

				hOpenedFile = CreateFile(
					sFile.c_str(),
					GENERIC_READ | GENERIC_WRITE,
					FILE_SHARE_READ,
					NULL,
					OPEN_EXISTING,
					FILE_ATTRIBUTE_NORMAL,
					NULL
				);

				if (hOpenedFile == INVALID_HANDLE_VALUE)
					return ERROR;

				BYTE* pbyData;
				pbyData = byUncompressedBuffer.data();

				do
				{
					ReadFile(hOpenedFile, pbyData, 1024, &dwNumberOfBytesRead, NULL);
					pbyData += dwNumberOfBytesRead;
				} while (dwNumberOfBytesRead == 1024);

				dwCRC32 = crc32(0L, Z_NULL, 0);
				dwCRC32 = crc32(dwCRC32, byUncompressedBuffer.data(), dwUncompressedSize);

				compress(byCompressedBuffer.data(), &dwCompressedSize, byUncompressedBuffer.data(), dwUncompressedSize);
			}

			// Copy to memory
			vZippedData.resize(vZippedData.size() + dwCompressedSize);
			memcpy(vZippedData.data() + vZippedData.size() - dwCompressedSize, byCompressedBuffer.data(), dwCompressedSize);

		  //AllocateDataDescriptor(vZippedData, dwCRC32, dwCompressedSize, dwUncompressedSize);
			AllocateCentralDirectoryFileHeader(vCentralHeaderData, sDirectory, dwInitialDirectoryLength, tPWIN32_FIND_DATA, dwCRC32, dwCompressedSize, dwUncompressedSize, dwOffsetLocalHeader);
		}
	} while (FindNextFile(hFile, tPWIN32_FIND_DATA));

	if (GetLastError() != ERROR_NO_MORE_FILES)
		return ERROR;

	return SUCCESS;
}

void cZIP::AllocateLocalFileHeader(std::vector<BYTE> &vZippedData, const std::string sDirectory, const DWORD dwInitialDirectoryLength, const PWIN32_FIND_DATA tPWIN32_FIND_DATA)
{
	// Initialize to '\0'
	LOCAL_FILE_HEADER tLOCAL_FILE_HEADER = { '\0' };

	std::string sFile = sDirectory.substr(dwInitialDirectoryLength) + "\\" + tPWIN32_FIND_DATA->cFileName;
	std::replace(sFile.begin(), sFile.end(), "\\", "/");

	memcpy(tLOCAL_FILE_HEADER.f.LOCAL_FILE_HEADER_SIGNATURE, "\x50\x4b\x03\x04", 4);	/**< SIGNATURE - LITTLE_ENDIAN */
	memcpy(tLOCAL_FILE_HEADER.f.VERSION_NEEDED_TO_EXTRACT, "\x00\x14", 2);				/**< VERSION 20 */
  //memcpy(tLOCAL_FILE_HEADER.f.GENERAL_PURPOSE_BIT_FLAG, "\x00\x00", 2);				/**< UNUSED */
	memcpy(tLOCAL_FILE_HEADER.f.COMPRESSION_METHOD, "\x00\x08", 2);						/**< DEFLATE */
	memcpy(tLOCAL_FILE_HEADER.f.FILE_LAST_MODIFICATION_TIME, "\x00\x00", 2);			/**< TODO - IMPORTANT! */
	memcpy(tLOCAL_FILE_HEADER.f.FILE_LAST_MODICATION_DATE, "\x00\x00", 2);				/**< TODO - IMPORTANT! */
  //memcpy(tLOCAL_FILE_HEADER.f.CRC32, "\x00\x00", 4);									/**< UNUSED */
  //memcpy(tLOCAL_FILE_HEADER.f.COMPRESSED_SIZE, "\x00\x00\x00\x00", 4);				/**< UNUSED */
  //memcpy(tLOCAL_FILE_HEADER.f.UNCOMPRESSED_SIZE, "\x00\x00\x00", 4);					/**< UNUSED */

	tLOCAL_FILE_HEADER.f.FILE_NAME_LENGTH[0] = (BYTE) sFile.size() >> 8;				/**< FILE SIZE (HIGH) */
	tLOCAL_FILE_HEADER.f.FILE_NAME_LENGTH[1] = (BYTE) sFile.size();						/**< FILE SIZE (LOW) */

  //memcpy(tLOCAL_FILE_HEADER.f.EXTRA_FIELD_LENGTH, "\x00\x00", 2);						/**< UNUSED */
	memcpy(tLOCAL_FILE_HEADER.f.FILE_NAME, sFile.c_str(), sFile.size());				/**< FILE NAME */

  //BYTE pbyEFBuffer[255] = { '\0' };

  //memcpy(tLOCAL_FILE_HEADER.f.EXTRA_FIELD, pbyEFBuffer, 255);							/**< UNUSED */

	// Copy to memory
	vZippedData.resize(vZippedData.size() + 30 + sFile.size());
	memcpy(vZippedData.data() + vZippedData.size() - 30 - sFile.size(), tLOCAL_FILE_HEADER.v, 30 + sFile.size());
}

void cZIP::AllocateDataDescriptor(std::vector<BYTE> &vZippedData, const DWORD dwCRC32, const DWORD dwCompressedSize, const DWORD dwUncompressedSize)
{
	// Initialize to '\0'
	DATA_DESCRIPTOR tDATA_DESCRIPTOR = { '\0' };

	memcpy(tDATA_DESCRIPTOR.f.DATA_DESCRIPTOR_SIGNATURE, "\x50\x4b\x07\x08", 4);	/**< SIGNATURE - LITTLE_ENDIAN */

	tDATA_DESCRIPTOR.f.CRC32[0] = (BYTE) dwCRC32 >> 24;								/**< CRC32 HIGH-HIGH */
	tDATA_DESCRIPTOR.f.CRC32[1] = (BYTE) dwCRC32 >> 16;								/**< CRC32 HIGH */
	tDATA_DESCRIPTOR.f.CRC32[2] = (BYTE) dwCRC32 >> 8;								/**< CRC32 LOW */
	tDATA_DESCRIPTOR.f.CRC32[3] = (BYTE) dwCRC32;									/**< CRC32 LOW-LOW */

	tDATA_DESCRIPTOR.f.COMPRESSED_SIZE[0] = (BYTE) dwCompressedSize >> 24;			/**< COMPRESSED SIZE HIGH-HIGH */
	tDATA_DESCRIPTOR.f.COMPRESSED_SIZE[1] = (BYTE) dwCompressedSize >> 16;			/**< COMPRESSED SIZE HIGH */
	tDATA_DESCRIPTOR.f.COMPRESSED_SIZE[2] = (BYTE) dwCompressedSize >> 8;			/**< COMPRESSED SIZE LOW */
	tDATA_DESCRIPTOR.f.COMPRESSED_SIZE[3] = (BYTE) dwCompressedSize;				/**< COMPRESSED SIZE LOW-LOW */

	tDATA_DESCRIPTOR.f.UNCOMPRESSED_SIZE[0] = (BYTE) dwUncompressedSize >> 24;		/**< UNCOMPRESSED SIZE HIGH-HIGH */
	tDATA_DESCRIPTOR.f.UNCOMPRESSED_SIZE[1] = (BYTE) dwUncompressedSize >> 16;		/**< UNCOMPRESSED SIZE HIGH */
	tDATA_DESCRIPTOR.f.UNCOMPRESSED_SIZE[2] = (BYTE) dwUncompressedSize >> 8;		/**< UNCOMPRESSED SIZE LOW */
	tDATA_DESCRIPTOR.f.UNCOMPRESSED_SIZE[3] = (BYTE) dwUncompressedSize;			/**< UNCOMPRESSED SIZE LOW-LOW */

	// Copy to memory
	vZippedData.resize(vZippedData.size() + 16);
	memcpy(vZippedData.data() + vZippedData.size() - 16, tDATA_DESCRIPTOR.v, 16);
}

void cZIP::AllocateCentralDirectoryFileHeader(std::vector<BYTE> &vZippedData, const std::string sDirectory, const DWORD dwInitialDirectoryLength, const PWIN32_FIND_DATA tPWIN32_FIND_DATA, const DWORD dwCRC32, const DWORD dwCompressedSize, const DWORD dwUncompressedSize, const DWORD dwOffsetLocalHeader)
{
	CENTRAL_DIRECTORY_FILE_HEADER tCENTRAL_DIRECTORY_FILE_HEADER = { '\0' };

	std::string sFile = sDirectory.substr(dwInitialDirectoryLength) + "\\" + tPWIN32_FIND_DATA->cFileName;
	std::replace(sFile.begin(), sFile.end(), "\\", "/");

	memcpy(tCENTRAL_DIRECTORY_FILE_HEADER.f.CENTRAL_DIRECTORY_FILE_HEADER_SIGNATURE, "\x50\x4b\x01\x02", 4);			/**< SIGNATURE - LITTLE_ENDIAN */
	memcpy(tCENTRAL_DIRECTORY_FILE_HEADER.f.VERSION_MADE_BY, "\x00\x14", 2);											/**< VERSION 20 */
	memcpy(tCENTRAL_DIRECTORY_FILE_HEADER.f.VERSION_NEEDED_TO_EXTRACT, "\x00\x14", 2);									/**< VERSION 20 */
  //memcpy(tCENTRAL_DIRECTORY_FILE_HEADER.f.GENERAL_PURPOSE_BIT_FLAG, "\x00\x00", 2);									/**< UNUSED */
	memcpy(tCENTRAL_DIRECTORY_FILE_HEADER.f.COMPRESSION_METHOD, "\x00\x08", 2);											/**< DEFLATE */
	memcpy(tCENTRAL_DIRECTORY_FILE_HEADER.f.FILE_LAST_MODIFICATION_TIME, "\x00\x00", 2);								/**< TODO - IMPORTANT! */
	memcpy(tCENTRAL_DIRECTORY_FILE_HEADER.f.FILE_LAST_MODIFICATION_DATE, "\x00\x00", 2);								/**< TODO - IMPORTANT! */

	tCENTRAL_DIRECTORY_FILE_HEADER.f.CRC32[0] = (BYTE) dwCRC32 >> 24;													/**< CRC32 HIGH-HIGH */
	tCENTRAL_DIRECTORY_FILE_HEADER.f.CRC32[1] = (BYTE) dwCRC32 >> 16;													/**< CRC32 HIGH */
	tCENTRAL_DIRECTORY_FILE_HEADER.f.CRC32[2] = (BYTE) dwCRC32 >> 8;													/**< CRC32 LOW */
	tCENTRAL_DIRECTORY_FILE_HEADER.f.CRC32[3] = (BYTE) dwCRC32;															/**< CRC32 LOW-LOW */

	tCENTRAL_DIRECTORY_FILE_HEADER.f.COMPRESSED_SIZE[0] = (BYTE) dwCompressedSize >> 24;								/**< COMPRESSED SIZE HIGH-HIGH */
	tCENTRAL_DIRECTORY_FILE_HEADER.f.COMPRESSED_SIZE[1] = (BYTE) dwCompressedSize >> 16;								/**< COMPRESSED SIZE HIGH */
	tCENTRAL_DIRECTORY_FILE_HEADER.f.COMPRESSED_SIZE[2] = (BYTE) dwCompressedSize >> 8;									/**< COMPRESSED SIZE LOW */
	tCENTRAL_DIRECTORY_FILE_HEADER.f.COMPRESSED_SIZE[3] = (BYTE) dwCompressedSize;										/**< COMPRESSED SIZE LOW-LOW */

	tCENTRAL_DIRECTORY_FILE_HEADER.f.UNCOMPRESSED_SIZE[0] = (BYTE) dwUncompressedSize >> 24;							/**< UNCOMPRESSED SIZE HIGH-HIGH */
	tCENTRAL_DIRECTORY_FILE_HEADER.f.UNCOMPRESSED_SIZE[1] = (BYTE) dwUncompressedSize >> 16;							/**< UNCOMPRESSED SIZE HIGH */
	tCENTRAL_DIRECTORY_FILE_HEADER.f.UNCOMPRESSED_SIZE[2] = (BYTE) dwUncompressedSize >> 8;								/**< UNCOMPRESSED SIZE LOW */
	tCENTRAL_DIRECTORY_FILE_HEADER.f.UNCOMPRESSED_SIZE[3] = (BYTE) dwUncompressedSize;									/**< UNCOMPRESSED SIZE LOW-LOW */

	tCENTRAL_DIRECTORY_FILE_HEADER.f.FILE_NAME_LENGTH[0] = (BYTE) sFile.size() >> 8;									/**< FILE SIZE (HIGH) */
	tCENTRAL_DIRECTORY_FILE_HEADER.f.FILE_NAME_LENGTH[1] = (BYTE) sFile.size();											/**< FILE SIZE (LOW) */

  //memcpy(tCENTRAL_DIRECTORY_FILE_HEADER.f.EXTRA_FIELD_LENGTH, "\x00\x00", 2);											/**< UNUSED */
  //memcpy(tCENTRAL_DIRECTORY_FILE_HEADER.f.FILE_COMMENT_LENGTH, "\x00\x00", 2);										/**< UNUSED */
  //memcpy(tCENTRAL_DIRECTORY_FILE_HEADER.f.DISK_NUMBER_WHERE_FILE_STARTS, "\x00\x00", 2);								/**< UNUSED */
  //memcpy(tCENTRAL_DIRECTORY_FILE_HEADER.f.INTERNAL_FILE_ATTRIBUTES, "\x00\x00", 2);									/**< UNUSED */

	tCENTRAL_DIRECTORY_FILE_HEADER.f.EXTERNAL_FILE_ATTRIBUTES[0] = (BYTE) tPWIN32_FIND_DATA->dwFileAttributes >> 24;	/**< FILE ATTRIBUTE HIGH-HIGH */
	tCENTRAL_DIRECTORY_FILE_HEADER.f.EXTERNAL_FILE_ATTRIBUTES[1] = (BYTE) tPWIN32_FIND_DATA->dwFileAttributes >> 16;	/**< FILE ATTRIBUTE HIGH */
	tCENTRAL_DIRECTORY_FILE_HEADER.f.EXTERNAL_FILE_ATTRIBUTES[2] = (BYTE) tPWIN32_FIND_DATA->dwFileAttributes >> 8;		/**< FILE ATTRIBUTE LOW */
	tCENTRAL_DIRECTORY_FILE_HEADER.f.EXTERNAL_FILE_ATTRIBUTES[3] = (BYTE) tPWIN32_FIND_DATA->dwFileAttributes;			/**< FILE ATTRIBUTE LOW-LOW */

	tCENTRAL_DIRECTORY_FILE_HEADER.f.RELATIVE_OFFSET_LOCAL_FILE_HEADER[0] = (BYTE) dwOffsetLocalHeader >> 24;			/**< OFFSET LOCAL FILE HEADER HIGH-HIGH */
	tCENTRAL_DIRECTORY_FILE_HEADER.f.RELATIVE_OFFSET_LOCAL_FILE_HEADER[1] = (BYTE) dwOffsetLocalHeader >> 16;			/**< OFFSET LOCAL FILE HEADER HIGH */
	tCENTRAL_DIRECTORY_FILE_HEADER.f.RELATIVE_OFFSET_LOCAL_FILE_HEADER[2] = (BYTE) dwOffsetLocalHeader >> 8;			/**< OFFSET LOCAL FILE HEADER LOW */
	tCENTRAL_DIRECTORY_FILE_HEADER.f.RELATIVE_OFFSET_LOCAL_FILE_HEADER[3] = (BYTE) dwOffsetLocalHeader;					/**< OFFSET LOCAL FILE HEADER LOW-LOW */

	memcpy(tCENTRAL_DIRECTORY_FILE_HEADER.f.FILE_NAME, sFile.c_str(), sFile.size());									/**< FILE NAME */

  //BYTE byEFBuffer[255] = { '\0' };

  //memcpy(tCENTRAL_DIRECTORY_FILE_HEADER.f.EXTRA_FIELD, byEFBuffer, 255);												/**< UNUSED */

  //BYTE byFCBuffer[255] = { '\0' };

  //memcpy(tCENTRAL_DIRECTORY_FILE_HEADER.f.FILE_COMMENT, byFCBuffer, 255);												/**< UNUSED */

	// Copy to memory
	vZippedData.resize(vZippedData.size() + 46 + sFile.size());
	memcpy(vZippedData.data() + vZippedData.size() - 46 - sFile.size(), tCENTRAL_DIRECTORY_FILE_HEADER.v, 46 + sFile.size());

	m_wNumberOfCentralDirectories++;
}

void cZIP::AllocateEndOfCentralDirectoryRecord(std::vector<BYTE> &vZippedData, const WORD wNumberOfCentralDirectories, const DWORD dwSizeOfCentralDirectory, const DWORD dwOffsetStartCentralDirectory)
{
	END_OF_CENTRAL_DIRECTORY_RECORD tEND_OF_CENTRAL_DIRECTORY_RECORD = { '\0' };

	memcpy(tEND_OF_CENTRAL_DIRECTORY_RECORD.f.END_OF_CENTRAL_DIRECTORY_SIGNATURE, "\x50\x4b\x05\x06", 4);								/**< SIGNATURE - LITTLE_ENDIAN */
  //memcpy(tEND_OF_CENTRAL_DIRECTORY_RECORD.f.NUMBER_OF_THIS_DISK, "\x00\x00", 2);														/**< UNUSED */
  //memcpy(tEND_OF_CENTRAL_DIRECTORY_RECORD.f.DISK_WHERE_CENTRAL_DIRECTORY_STARTS, "\x00\x00", 2);										/**< UNUSED */

	tEND_OF_CENTRAL_DIRECTORY_RECORD.f.NUMBER_OF_CENTRAL_DIRECTORY_RECORDS_ON_THIS_DISK[0] = (BYTE) wNumberOfCentralDirectories >> 8;	/**< NUMBER OF CENTRAL DIRECTORIES HIGH */
	tEND_OF_CENTRAL_DIRECTORY_RECORD.f.NUMBER_OF_CENTRAL_DIRECTORY_RECORDS_ON_THIS_DISK[1] = (BYTE) wNumberOfCentralDirectories;		/**< NUMBER OF CETRANL DIRECTORIES LOW */

	tEND_OF_CENTRAL_DIRECTORY_RECORD.f.TOTAL_NUMBER_OF_CENTRAL_DIRECTORY_RECORDS[0] = (BYTE) wNumberOfCentralDirectories >> 8;			/**< NUMBER OF CENTRAL DIRECTORIES HIGH */
	tEND_OF_CENTRAL_DIRECTORY_RECORD.f.TOTAL_NUMBER_OF_CENTRAL_DIRECTORY_RECORDS[1] = (BYTE) wNumberOfCentralDirectories;				/**< NUMBER OF CETRANL DIRECTORIES LOW */

	tEND_OF_CENTRAL_DIRECTORY_RECORD.f.SIZE_OF_CENTRAL_DIRECTORY[0] = (BYTE) dwSizeOfCentralDirectory >> 24;							/**< SIZE OF CENTRAL DIRECTORY HIGH-HIGH */
	tEND_OF_CENTRAL_DIRECTORY_RECORD.f.SIZE_OF_CENTRAL_DIRECTORY[1] = (BYTE) dwSizeOfCentralDirectory >> 16;							/**< SIZE OF CENTRAL DIRECTORY HIGH */
	tEND_OF_CENTRAL_DIRECTORY_RECORD.f.SIZE_OF_CENTRAL_DIRECTORY[2] = (BYTE) dwSizeOfCentralDirectory >> 8;								/**< SIZE OF CENTRAL DIRECTORY LOW */
	tEND_OF_CENTRAL_DIRECTORY_RECORD.f.SIZE_OF_CENTRAL_DIRECTORY[3] = (BYTE) dwSizeOfCentralDirectory;									/**< SIZE OF CENTRAL DIRECTORY LOW-LOW */

	tEND_OF_CENTRAL_DIRECTORY_RECORD.f.OFFSET_OF_START_OF_CENTRAL_DIRECTORY[0] = (BYTE) dwOffsetStartCentralDirectory >> 24;			/**< OFFSET START OF CENTRAL DIRECTORY HIGH-HIGH */
	tEND_OF_CENTRAL_DIRECTORY_RECORD.f.OFFSET_OF_START_OF_CENTRAL_DIRECTORY[1] = (BYTE) dwOffsetStartCentralDirectory >> 16;			/**< OFFSET START OF CENTRAL DIRECTORY HIGH */
	tEND_OF_CENTRAL_DIRECTORY_RECORD.f.OFFSET_OF_START_OF_CENTRAL_DIRECTORY[2] = (BYTE) dwOffsetStartCentralDirectory >> 8;				/**< OFFSET START OF CENTRAL DIRECTORY LOW */
	tEND_OF_CENTRAL_DIRECTORY_RECORD.f.OFFSET_OF_START_OF_CENTRAL_DIRECTORY[3] = (BYTE) dwOffsetStartCentralDirectory;					/**< OFFSET START OF CENTRAL DIRECTORY LOW-LOW */

  //memcpy(tEND_OF_CENTRAL_DIRECTORY_RECORD.f.COMMENT_LENGTH, "\x00\x00", 2);															/**< UNUSED */

  //BYTE byCBuffer[255] = { '\0' };

  //memcpy(tEND_OF_CENTRAL_DIRECTORY_RECORD.f.COMMENT, byCBuffer, 255);																	/**< UNUSED */

	// Copy to memory
	vZippedData.resize(vZippedData.size() + 22);
	memcpy(vZippedData.data() + vZippedData.size() - 22, tEND_OF_CENTRAL_DIRECTORY_RECORD.v, 22);
}