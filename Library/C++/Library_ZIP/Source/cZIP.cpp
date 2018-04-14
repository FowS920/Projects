#include <algorithm>

#include "cZIP.h"

// Define only when using for transfert
// For local computer use, undefine
// Do this for both cZIP and cUNZIP
#define __CODE_PAGE_UTF8_
#include "TString.h"

// TODO : Define more errors type
#define ZIP_SUCCESS	0x0000;
#define ZIP_ERROR	0x0001;

/**
 * @brief	Class constructor
 *
 * @author	Maxime Lagadec
 * @date	4/8/2018
 *
 */

cZIP::cZIP()
{

}

/**
 * @brief	Class constructor (Also zip directory to memory)
 *
 * @author	Maxime Lagadec
 * @date	4/8/2018
 *
 * @param	[in] wsDirectory : Path to directory or file to zip into memory
 *
 * @note	Use GetDidZipFail() to confirm zipping worked
 *
 */

cZIP::cZIP(std::wstring wsDirectory)
{
	m_bZippingFailed = ZipToMemory(wsDirectory);
}

/**
 * @brief	Class constructor (Also zip directory to file)
 *
 * @author	Maxime Lagadec
 * @date	4/8/2018
 *
 * @param	[in] wsDirectory : Path to directory or file to zip into memory
 * @param	[in] wsDestination : Path to directory with file name to zip into memory
 * @param	[in,opt] bFlush : TRUE -> Flush memory data after zipping / FALSE -> Do not flush memory data after zipping
 *
 * @note	Use GetDidZipFail() to confirm zipping worked
 *
 */

cZIP::cZIP(std::wstring wsDirectory, std::wstring wsDestination, const BOOL bFlush)
{
	m_bZippingFailed = ZipToFile(wsDirectory, wsDestination, bFlush);
}

/**
 * @brief	Class destructor
 *
 * @author	Maxime Lagadec
 * @date	4/8/2018
 *
 */

cZIP::~cZIP()
{
	FlushMemory();
}

/**
 * @brief	ZIP directory or file to memory
 *
 * @author	Maxime Lagadec
 * @date	4/8/2018
 *
 * @param	[in] wsDirectory : Path to directory or file to zip into memory
 *
 * @return	SUCCESS : 0
 * @return	ERROR : 1
 *
 * @note	m_vZippedData variable is where the ZIP is stored
 *
 */

DWORD cZIP::ZipToMemory(std::wstring wsDirectory)
{
	DWORD dwSizeOfCentralDirectory;
	DWORD dwOffsetStartCentralDirectory;

	// Reset memory
	FlushMemory();

	// Swap all / to \\ in case (we use \\ for coding and / for storing)
	std::replace(wsDirectory.begin(), wsDirectory.end(), L'/', L'\\');

	// Make sure directory has no double backslash ("\\\\") except for network drive
	if (wsDirectory.find(L"\\\\") != std::wstring::npos)
	{
		if (wsDirectory.rfind(L"\\\\") >= 1)
			return ZIP_ERROR;
	}

	// Make sure directory (or file) exists
	{
		HANDLE hFile;

		WIN32_FIND_DATA tWIN32_FIND_DATA;

		hFile = FindFirstFile(ToTString(wsDirectory).c_str(), &tWIN32_FIND_DATA);

		if (hFile == INVALID_HANDLE_VALUE)
			return ZIP_ERROR;

		m_bFile = !(FILE_ATTRIBUTE_DIRECTORY == (tWIN32_FIND_DATA.dwFileAttributes & FILE_ATTRIBUTE_DIRECTORY));
	}

	// Call ZIP function
	{
		std::vector<BYTE> vCentralHeaderData;
	
		// Try to catch bad_allocation (when resizing vectors)
		try
		{
			if (ZIP(m_vZippedData, vCentralHeaderData, wsDirectory, wsDirectory.rfind(L"\\") + 1, m_bFile))
			{
				// Reset memory
				FlushMemory();
				return ZIP_ERROR;
			}
		}
		// We did not have enough space to allocate correctly the data
		catch (std::bad_alloc)
		{
			// Reset memory
			FlushMemory();
			return ZIP_ERROR;
		}

		dwSizeOfCentralDirectory = vCentralHeaderData.size();
		dwOffsetStartCentralDirectory = m_vZippedData.size();

		// Copy to memory
		m_vZippedData.resize(m_vZippedData.size() + vCentralHeaderData.size());
		memcpy(m_vZippedData.data() + m_vZippedData.size() - vCentralHeaderData.size(), vCentralHeaderData.data(), vCentralHeaderData.size());
	}

	AllocateEndOfCentralDirectoryRecord(m_vZippedData, m_wNumberOfCentralDirectories, dwSizeOfCentralDirectory, dwOffsetStartCentralDirectory);

	m_wsStoredDirectoryZip = wsDirectory;
	m_bZippedDataInMemory = TRUE;

	return ZIP_SUCCESS;
}

/**
 * @brief	ZIP directory or file to a .zip file
 *
 * @author	Maxime Lagadec
 * @date	4/8/2018
 *
 * @param	[in] wsDirectory : Path to directory or file to zip into memory
 * @param	[in] wsDestination : Path to directory with file name to zip into memory
 * @param	[in,opt] bFlush : TRUE -> Flush memory data after zipping / FALSE -> Do not flush memory data after zipping
 *
 * @return	SUCCESS : 0
 * @return	ERROR : 1
 *
 * @note	m_vZippedData variable is where the ZIP is stored (not flushed!)
 * @note	sDestination file name must have no extention or .zip has an extension
 */

DWORD cZIP::ZipToFile(std::wstring wsDirectory, std::wstring wsDestination, const BOOL bFlush)
{
	HANDLE hOpenedFile;

	// Make sure destination exists
	hOpenedFile = CreateFile(
		ToTString(wsDestination).c_str(),
		GENERIC_WRITE,
		FILE_SHARE_READ,
		NULL,
		CREATE_NEW,
		FILE_ATTRIBUTE_NORMAL,
		NULL
	);

	if (hOpenedFile == INVALID_HANDLE_VALUE)
		return ZIP_ERROR;

	// If already zipped don't rezip
	if (!(m_bZippedDataInMemory && (m_wsStoredDirectoryZip == wsDirectory)))
		// Zip to memory
		if (ZipToMemory(wsDirectory))
		{
			CloseHandle(hOpenedFile);
			_wremove(wsDestination.c_str());
			return ZIP_ERROR;
		}

	// Write to file
	WriteFile(hOpenedFile, m_vZippedData.data(), m_vZippedData.size(), NULL, NULL);

	CloseHandle(hOpenedFile);

	if (bFlush)
		FlushMemory();

	return ZIP_SUCCESS;
}

/**
 * @brief	Flush internal memory allocated
 *
 * @author	Maxime Lagadec
 * @date	4/8/2018
 *
 */
void cZIP::FlushMemory()
{
	m_bFile = FALSE;
	m_bZippedDataInMemory = FALSE;
	m_wsStoredDirectoryZip = L"";

	m_vZippedData.clear();
	m_vZippedData.resize(0);
	m_vZippedData.shrink_to_fit();

	m_wNumberOfCentralDirectories = 0;
}

/**
 * @brief	Recursive function used to ZIP data into memory
 *
 * @author	Maxime Lagadec
 * @date	4/8/2018
 *
 * @param	[in,out] vZippedData : Buffer where headers and data is stored
 * @param	[in,out] vCentralHeaderData : Buffer where central header data is stored
 * @param	[in] wsDirectory : Path to directory or file to zip into memory
 * @param	[in] dwInitialDirectoryLength : Length of initial directory path that is not to be zipped
 * @param	[in] bFile : TRUE if we are zipping a file, FALSE if we are zipping a directory
 *
 * @return	SUCCESS : 0
 * @return	ERROR : 1
 *
 */

DWORD cZIP::ZIP(std::vector<BYTE> &vZippedData, std::vector<BYTE> &vCentralHeaderData, const std::wstring wsDirectory, const DWORD dwInitialDirectoryLength, const BOOL bFile)
{
	HANDLE hFile;
	HANDLE hOpenedFile;

	WIN32_FIND_DATA tWIN32_FIND_DATA;

	std::wstring wsFileName;
	std::wstring wsFile;

	std::wstring wsSearchDirectory;
	std::wstring wsNewDirectory;

	if (bFile)
		wsSearchDirectory = wsDirectory;
	else
		wsSearchDirectory = wsDirectory + L"\\*";

	hFile = FindFirstFile(ToTString(wsSearchDirectory).c_str(), &tWIN32_FIND_DATA);

	if (hFile == INVALID_HANDLE_VALUE)
		return ZIP_ERROR;

	do
	{
		wsFile = ToWString(tWIN32_FIND_DATA.cFileName);

		// We don't want to add DOS files (. and ..)
		if ((wsFile == L".") || (wsFile == L".."))
		{
			continue;
		}
		// We found a directory (go deeper)
		else if (FILE_ATTRIBUTE_DIRECTORY == (tWIN32_FIND_DATA.dwFileAttributes & FILE_ATTRIBUTE_DIRECTORY))
		{
			DWORD dwOffsetLocalHeader;

			wsNewDirectory = wsDirectory + L"\\" + ToWString(tWIN32_FIND_DATA.cFileName);

			// Add to header
			dwOffsetLocalHeader = vZippedData.size();

			AllocateLocalFileHeader(vZippedData, wsDirectory, dwInitialDirectoryLength, &tWIN32_FIND_DATA, 0x0000, 0x00000000, 0x00000000, 0x00000000);
		  //AllocateDataDescriptor(vZippedData, 0x00000000, 0x00000000, 0x00000000);
			AllocateCentralDirectoryFileHeader(vCentralHeaderData, wsDirectory, dwInitialDirectoryLength, &tWIN32_FIND_DATA, 0x0000, 0x00000000, 0x00000000, 0x00000000, dwOffsetLocalHeader);

			if (ZIP(vZippedData, vCentralHeaderData, wsNewDirectory, dwInitialDirectoryLength, FALSE))
			{
				FindClose(hFile);
				return ZIP_ERROR;
			}
		}
		// We found a file (zip it)
		else
		{
			DWORD dwCRC32;
			DWORD dwCompressedSize;
			DWORD dwUncompressedSize;
			DWORD dwOffsetLocalHeader;

			std::vector<BYTE> byCompressedBuffer;

			dwOffsetLocalHeader = vZippedData.size();

			// File can be up to DWORD file size
			if (tWIN32_FIND_DATA.nFileSizeHigh != 0)
				return ZIP_ERROR;

			dwUncompressedSize = tWIN32_FIND_DATA.nFileSizeLow;
			dwCompressedSize = compressBound(dwUncompressedSize);

			byCompressedBuffer.resize(dwCompressedSize);

			{
				std::vector<BYTE> byUncompressedBuffer;
				byUncompressedBuffer.resize(dwUncompressedSize);

				// Read file to buffer
				if (m_bFile)
					wsFile = wsDirectory;
				else
					wsFile = wsDirectory + L"\\" + ToWString(tWIN32_FIND_DATA.cFileName);

				hOpenedFile = CreateFile(
					ToTString(wsFile).c_str(),
					GENERIC_READ,
					FILE_SHARE_READ | FILE_SHARE_WRITE,
					NULL,
					OPEN_EXISTING,
					FILE_ATTRIBUTE_NORMAL,
					NULL
				);

				if (hOpenedFile == INVALID_HANDLE_VALUE)
					return ZIP_ERROR;

				ReadFile(hOpenedFile, byUncompressedBuffer.data(), dwUncompressedSize, NULL, NULL);

				CloseHandle(hOpenedFile);

				dwCRC32 = crc32(0L, Z_NULL, 0);
				dwCRC32 = crc32(dwCRC32, byUncompressedBuffer.data(), dwUncompressedSize);

				if (compressRAW(byCompressedBuffer.data(), &dwCompressedSize, byUncompressedBuffer.data(), dwUncompressedSize, 5))
					return ZIP_ERROR;
			}

			AllocateLocalFileHeader(vZippedData, wsDirectory, dwInitialDirectoryLength, &tWIN32_FIND_DATA, 0x0008, dwCRC32, dwCompressedSize, dwUncompressedSize);

			// Copy to memory
			vZippedData.resize(vZippedData.size() + dwCompressedSize);
			memcpy(vZippedData.data() + vZippedData.size() - dwCompressedSize, byCompressedBuffer.data(), dwCompressedSize);

		  //AllocateDataDescriptor(vZippedData, dwCRC32, dwCompressedSize, dwUncompressedSize);
			AllocateCentralDirectoryFileHeader(vCentralHeaderData, wsDirectory, dwInitialDirectoryLength, &tWIN32_FIND_DATA, 0x0008, dwCRC32, dwCompressedSize, dwUncompressedSize, dwOffsetLocalHeader);
		}
	} while (FindNextFile(hFile, &tWIN32_FIND_DATA));

	FindClose(hFile);

	if (GetLastError() != ERROR_NO_MORE_FILES)
		return ZIP_ERROR;

	return ZIP_SUCCESS;
}

/**
 * @brief	Allocate local file header to buffer
 *
 * @author	Maxime Lagadec
 * @date	4/8/2018
 *
 * @param	[in,out] vZippedData : Buffer where local file header is stored
 * @param	[in] wsDirectory : Path to directory or file to zip into memory
 * @param	[in] dwInitialDirectoryLength : Length of initial directory path that is not to be zipped
 * @param	[in] tPWIN32_FIND_DATA : File's information structure
 * @param	[in] wCompressionMethod : Compression method used
 * @param	[in] dwCRC32 : CRC-32 of the uncompressed buffer
 * @param	[in] dwCompressedSize : Size of the compressed buffer
 * @param	[in] dwUncompressedSize : Size of the uncompressed buffer
 *
 */

void cZIP::AllocateLocalFileHeader(std::vector<BYTE> &vZippedData, const std::wstring wsDirectory, const DWORD dwInitialDirectoryLength, const PWIN32_FIND_DATA tPWIN32_FIND_DATA, const WORD wCompressionMethod, const DWORD dwCRC32, const DWORD dwCompressedSize, const DWORD dwUncompressedSize)
{
	// Initialize to '\0'
	LOCAL_FILE_HEADER tLOCAL_FILE_HEADER = { '\0' };

	std::wstring wsFile;
	std::string sFile;

	SYSTEMTIME tSYSTEMTIME;
	SYSTEMTIME tLOCALSYSTEMTIME;
	WORD wLastModificationDate;
	WORD wLastModificationTime;

	if (FILE_ATTRIBUTE_DIRECTORY == (tPWIN32_FIND_DATA->dwFileAttributes & FILE_ATTRIBUTE_DIRECTORY))
		wsFile = wsDirectory.substr(dwInitialDirectoryLength) + L"\\" + ToWString(tPWIN32_FIND_DATA->cFileName) + L"\\";
	else
		if (!m_bFile)
			wsFile = wsDirectory.substr(dwInitialDirectoryLength) + L"\\" + ToWString(tPWIN32_FIND_DATA->cFileName);
		else
			wsFile = wsDirectory.substr(dwInitialDirectoryLength);

	std::replace(wsFile.begin(), wsFile.end(), L'\\', L'/');
	sFile = ToString(wsFile);

	FileTimeToSystemTime(&tPWIN32_FIND_DATA->ftLastWriteTime, &tSYSTEMTIME);

	// Get file's LOCAL time
	SystemTimeToTzSpecificLocalTime(NULL, &tSYSTEMTIME, &tLOCALSYSTEMTIME);

	wLastModificationTime = (WORD) (((tLOCALSYSTEMTIME.wHour & 0x1F) << 11) + ((tSYSTEMTIME.wMinute & 0x3F) << 5) + ((tSYSTEMTIME.wSecond & 0x1F) >> 1));
	wLastModificationDate = (WORD) ((((tLOCALSYSTEMTIME.wYear - 1980) & 0x7F) << 9) + ((tLOCALSYSTEMTIME.wMonth & 0x0F) << 5) + (tLOCALSYSTEMTIME.wDay & 0x1F));

	memcpy(tLOCAL_FILE_HEADER.f.LOCAL_FILE_HEADER_SIGNATURE, "\x50\x4b\x03\x04", 4);			/* SIGNATURE - LITTLE_ENDIAN */
	memcpy(tLOCAL_FILE_HEADER.f.VERSION_NEEDED_TO_EXTRACT, "\x14\x00", 2);						/* VERSION 20 */
  //memcpy(tLOCAL_FILE_HEADER.f.GENERAL_PURPOSE_BIT_FLAG, "\x00\x00", 2);						/* UNUSED */

	tLOCAL_FILE_HEADER.f.COMPRESSION_METHOD[0] = (BYTE) wCompressionMethod;						/* COMPRESSION METHOD LOW */
	tLOCAL_FILE_HEADER.f.COMPRESSION_METHOD[1] = (BYTE) (wCompressionMethod >> 8);				/* COMPRESSION METHOD HIGH */

	tLOCAL_FILE_HEADER.f.FILE_LAST_MODIFICATION_TIME[0] = (BYTE) wLastModificationTime;			/* LAST MODIFICATION TIME LOW */
	tLOCAL_FILE_HEADER.f.FILE_LAST_MODIFICATION_TIME[1] = (BYTE) (wLastModificationTime >> 8);	/* LAST MODIFICATION TIME HIGH */

	tLOCAL_FILE_HEADER.f.FILE_LAST_MODIFICATION_DATE[0] = (BYTE) wLastModificationDate;			/* LAST MODIFICATION DATE LOW */
	tLOCAL_FILE_HEADER.f.FILE_LAST_MODIFICATION_DATE[1] = (BYTE) (wLastModificationDate >> 8);	/* LAST MODIFICATION DATE HIGH */

	tLOCAL_FILE_HEADER.f.CRC32[0] = (BYTE) dwCRC32;												/* CRC32 LOW-LOW */
	tLOCAL_FILE_HEADER.f.CRC32[1] = (BYTE) (dwCRC32 >> 8);										/* CRC32 LOW */
	tLOCAL_FILE_HEADER.f.CRC32[2] = (BYTE) (dwCRC32 >> 16);										/* CRC32 HIGH */
	tLOCAL_FILE_HEADER.f.CRC32[3] = (BYTE) (dwCRC32 >> 24);										/* CRC32 HIGH-HIGH */

	tLOCAL_FILE_HEADER.f.COMPRESSED_SIZE[0] = (BYTE) dwCompressedSize;							/* COMPRESSED SIZE LOW-LOW */
	tLOCAL_FILE_HEADER.f.COMPRESSED_SIZE[1] = (BYTE) (dwCompressedSize >> 8);					/* COMPRESSED SIZE LOW */
	tLOCAL_FILE_HEADER.f.COMPRESSED_SIZE[2] = (BYTE) (dwCompressedSize >> 16);					/* COMPRESSED SIZE HIGH */
	tLOCAL_FILE_HEADER.f.COMPRESSED_SIZE[3] = (BYTE) (dwCompressedSize >> 24);					/* COMPRESSED SIZE HIGH-HIGH */

	tLOCAL_FILE_HEADER.f.UNCOMPRESSED_SIZE[0] = (BYTE) dwUncompressedSize;						/* UNCOMPRESSED SIZE LOW-LOW */
	tLOCAL_FILE_HEADER.f.UNCOMPRESSED_SIZE[1] = (BYTE) (dwUncompressedSize >> 8);				/* UNCOMPRESSED SIZE LOW */
	tLOCAL_FILE_HEADER.f.UNCOMPRESSED_SIZE[2] = (BYTE) (dwUncompressedSize >> 16);				/* UNCOMPRESSED SIZE HIGH */
	tLOCAL_FILE_HEADER.f.UNCOMPRESSED_SIZE[3] = (BYTE) (dwUncompressedSize >> 24);				/* UNCOMPRESSED SIZE HIGH-HIGH */

	tLOCAL_FILE_HEADER.f.FILE_NAME_LENGTH[0] = (BYTE) sFile.size();								/* FILE SIZE LOW */
	tLOCAL_FILE_HEADER.f.FILE_NAME_LENGTH[1] = (BYTE) (sFile.size() >> 8);						/* FILE SIZE HIGH */

  //memcpy(tLOCAL_FILE_HEADER.f.EXTRA_FIELD_LENGTH, "\x00\x00", 2);								/* UNUSED */
	memcpy(tLOCAL_FILE_HEADER.f.FILE_NAME, sFile.c_str(), sFile.size());						/* FILE NAME */

  //BYTE pbyEFBuffer[255] = { '\0' };

  //memcpy(tLOCAL_FILE_HEADER.f.EXTRA_FIELD, pbyEFBuffer, 255);									/* UNUSED */

	// Copy to memory
	vZippedData.resize(vZippedData.size() + 30 + sFile.size());
	memcpy(vZippedData.data() + vZippedData.size() - 30 - sFile.size(), tLOCAL_FILE_HEADER.v, 30 + sFile.size());
}

/**
 * @brief	Allocate data descriptor to buffer
 *
 * @author	Maxime Lagadec
 * @date	4/8/2018
 *
 * @param	[in,out] vZippedData : Buffer where data descriptor is stored
 * @param	[in] dwCRC32 : CRC-32 of the uncompressed buffer
 * @param	[in] dwCompressedSize : Size of the compressed buffer
 * @param	[in] dwUncompressedSize : Size of the uncompressed buffer
 *
 */

void cZIP::AllocateDataDescriptor(std::vector<BYTE> &vZippedData, const DWORD dwCRC32, const DWORD dwCompressedSize, const DWORD dwUncompressedSize)
{
	// Initialize to '\0'
	DATA_DESCRIPTOR tDATA_DESCRIPTOR = { '\0' };

	memcpy(tDATA_DESCRIPTOR.f.DATA_DESCRIPTOR_SIGNATURE, "\x50\x4b\x07\x08", 4);	/* SIGNATURE - LITTLE_ENDIAN */

	tDATA_DESCRIPTOR.f.CRC32[0] = (BYTE) dwCRC32;									/* CRC32 LOW-LOW */
	tDATA_DESCRIPTOR.f.CRC32[1] = (BYTE) (dwCRC32 >> 8);							/* CRC32 LOW */
	tDATA_DESCRIPTOR.f.CRC32[2] = (BYTE) (dwCRC32 >> 16);							/* CRC32 HIGH */
	tDATA_DESCRIPTOR.f.CRC32[3] = (BYTE) (dwCRC32 >> 24);							/* CRC32 HIGH-HIGH */

	tDATA_DESCRIPTOR.f.COMPRESSED_SIZE[0] = (BYTE) dwCompressedSize;				/* COMPRESSED SIZE LOW-LOW */
	tDATA_DESCRIPTOR.f.COMPRESSED_SIZE[1] = (BYTE) (dwCompressedSize >> 8);			/* COMPRESSED SIZE LOW */
	tDATA_DESCRIPTOR.f.COMPRESSED_SIZE[2] = (BYTE) (dwCompressedSize >> 16);		/* COMPRESSED SIZE HIGH */
	tDATA_DESCRIPTOR.f.COMPRESSED_SIZE[3] = (BYTE) (dwCompressedSize >> 24);		/* COMPRESSED SIZE HIGH-HIGH */

	tDATA_DESCRIPTOR.f.UNCOMPRESSED_SIZE[0] = (BYTE) dwUncompressedSize;			/* UNCOMPRESSED SIZE LOW-LOW */
	tDATA_DESCRIPTOR.f.UNCOMPRESSED_SIZE[1] = (BYTE) (dwUncompressedSize >> 8);		/* UNCOMPRESSED SIZE LOW */
	tDATA_DESCRIPTOR.f.UNCOMPRESSED_SIZE[2] = (BYTE) (dwUncompressedSize >> 16);	/* UNCOMPRESSED SIZE HIGH */
	tDATA_DESCRIPTOR.f.UNCOMPRESSED_SIZE[3] = (BYTE) (dwUncompressedSize >> 24);	/* UNCOMPRESSED SIZE HIGH-HIGH */

	// Copy to memory
	vZippedData.resize(vZippedData.size() + 16);
	memcpy(vZippedData.data() + vZippedData.size() - 16, tDATA_DESCRIPTOR.v, 16);
}

/**
 * @brief	Allocate central directory file header to buffer
 *
 * @author	Maxime Lagadec
 * @date	4/8/2018
 *
 * @param	[in,out] vZippedData : Buffer where data descriptor is stored
 * @param	[in] wsDirectory : Path to directory or file to zip into memory
 * @param	[in] dwInitialDirectoryLength : Length of initial directory path that is not to be zipped
 * @param	[in] tPWIN32_FIND_DATA : File's information structure
 * @param	[in] wCompressionMethod : Compression method used
 * @param	[in] dwCRC32 : CRC-32 of the uncompressed buffer
 * @param	[in] dwCompressedSize : Size of the compressed buffer
 * @param	[in] dwUncompressedSize : Size of the uncompressed buffer
 * @param	[in] dwOffsetLocalHeader : Offset to the matching local header (from start of the file)
 *
 */

void cZIP::AllocateCentralDirectoryFileHeader(std::vector<BYTE> &vZippedData, const std::wstring wsDirectory, const DWORD dwInitialDirectoryLength, const PWIN32_FIND_DATA tPWIN32_FIND_DATA, const WORD wCompressionMethod, const DWORD dwCRC32, const DWORD dwCompressedSize, const DWORD dwUncompressedSize, const DWORD dwOffsetLocalHeader)
{
	CENTRAL_DIRECTORY_FILE_HEADER tCENTRAL_DIRECTORY_FILE_HEADER = { '\0' };

	std::wstring wsFile;
	std::string sFile;

	SYSTEMTIME tSYSTEMTIME;
	SYSTEMTIME tLOCALSYSTEMTIME;
	WORD wLastModificationDate;
	WORD wLastModificationTime;

	if (FILE_ATTRIBUTE_DIRECTORY == (tPWIN32_FIND_DATA->dwFileAttributes & FILE_ATTRIBUTE_DIRECTORY))
		wsFile = wsDirectory.substr(dwInitialDirectoryLength) + L"\\" + ToWString(tPWIN32_FIND_DATA->cFileName) + L"\\";
	else
		if (!m_bFile)
			wsFile = wsDirectory.substr(dwInitialDirectoryLength) + L"\\" + ToWString(tPWIN32_FIND_DATA->cFileName);
		else
			wsFile = wsDirectory.substr(dwInitialDirectoryLength);

	std::replace(wsFile.begin(), wsFile.end(), L'\\', L'/');
	sFile = ToString(wsFile);

	FileTimeToSystemTime(&tPWIN32_FIND_DATA->ftLastWriteTime, &tSYSTEMTIME);

	// Get file's LOCAL time
	SystemTimeToTzSpecificLocalTime(NULL, &tSYSTEMTIME, &tLOCALSYSTEMTIME);

	wLastModificationTime = (WORD) (((tLOCALSYSTEMTIME.wHour & 0x1F) << 11) + ((tSYSTEMTIME.wMinute & 0x3F) << 5) + ((tSYSTEMTIME.wSecond & 0x1F) >> 1));
	wLastModificationDate = (WORD) ((((tLOCALSYSTEMTIME.wYear - 1980) & 0x7F) << 9) + ((tLOCALSYSTEMTIME.wMonth & 0x0F) << 5) + (tLOCALSYSTEMTIME.wDay & 0x1F));

	memcpy(tCENTRAL_DIRECTORY_FILE_HEADER.f.CENTRAL_DIRECTORY_FILE_HEADER_SIGNATURE, "\x50\x4b\x01\x02", 4);			/* SIGNATURE - LITTLE_ENDIAN */
	memcpy(tCENTRAL_DIRECTORY_FILE_HEADER.f.VERSION_MADE_BY, "\x14\x00", 2);											/* VERSION 20 */
	memcpy(tCENTRAL_DIRECTORY_FILE_HEADER.f.VERSION_NEEDED_TO_EXTRACT, "\x14\x00", 2);									/* VERSION 20 */
  //memcpy(tCENTRAL_DIRECTORY_FILE_HEADER.f.GENERAL_PURPOSE_BIT_FLAG, "\x00\x00", 2);									/* UNUSED */

	tCENTRAL_DIRECTORY_FILE_HEADER.f.COMPRESSION_METHOD[0] = (BYTE) wCompressionMethod;									/* COMPRESSION METHOD LOW */
	tCENTRAL_DIRECTORY_FILE_HEADER.f.COMPRESSION_METHOD[1] = (BYTE) (wCompressionMethod >> 8);							/* COMPRESSION METHOD HIGH */

	tCENTRAL_DIRECTORY_FILE_HEADER.f.FILE_LAST_MODIFICATION_TIME[0] = (BYTE) wLastModificationTime;						/* LAST MODIFICATION TIME LOW */
	tCENTRAL_DIRECTORY_FILE_HEADER.f.FILE_LAST_MODIFICATION_TIME[1] = (BYTE) (wLastModificationTime >> 8);				/* LAST MODIFICATION TIME HIGH */

	tCENTRAL_DIRECTORY_FILE_HEADER.f.FILE_LAST_MODIFICATION_DATE[0] = (BYTE) wLastModificationDate;						/* LAST MODIFICATION DATE LOW */
	tCENTRAL_DIRECTORY_FILE_HEADER.f.FILE_LAST_MODIFICATION_DATE[1] = (BYTE) (wLastModificationDate >> 8);				/* LAST MODIFICATION DATE HIGH */

	tCENTRAL_DIRECTORY_FILE_HEADER.f.CRC32[0] = (BYTE) dwCRC32;															/* CRC32 LOW-LOW */
	tCENTRAL_DIRECTORY_FILE_HEADER.f.CRC32[1] = (BYTE) (dwCRC32 >> 8);													/* CRC32 LOW */
	tCENTRAL_DIRECTORY_FILE_HEADER.f.CRC32[2] = (BYTE) (dwCRC32 >> 16);													/* CRC32 HIGH */
	tCENTRAL_DIRECTORY_FILE_HEADER.f.CRC32[3] = (BYTE) (dwCRC32 >> 24);													/* CRC32 HIGH-HIGH */

	tCENTRAL_DIRECTORY_FILE_HEADER.f.COMPRESSED_SIZE[0] = (BYTE) dwCompressedSize;										/* COMPRESSED SIZE LOW-LOW */
	tCENTRAL_DIRECTORY_FILE_HEADER.f.COMPRESSED_SIZE[1] = (BYTE) (dwCompressedSize >> 8);								/* COMPRESSED SIZE LOW */
	tCENTRAL_DIRECTORY_FILE_HEADER.f.COMPRESSED_SIZE[2] = (BYTE) (dwCompressedSize >> 16);								/* COMPRESSED SIZE HIGH */
	tCENTRAL_DIRECTORY_FILE_HEADER.f.COMPRESSED_SIZE[3] = (BYTE) (dwCompressedSize >> 24);								/* COMPRESSED SIZE HIGH-HIGH */

	tCENTRAL_DIRECTORY_FILE_HEADER.f.UNCOMPRESSED_SIZE[0] = (BYTE) dwUncompressedSize;									/* UNCOMPRESSED SIZE LOW-LOW */
	tCENTRAL_DIRECTORY_FILE_HEADER.f.UNCOMPRESSED_SIZE[1] = (BYTE) (dwUncompressedSize >> 8);							/* UNCOMPRESSED SIZE LOW */
	tCENTRAL_DIRECTORY_FILE_HEADER.f.UNCOMPRESSED_SIZE[2] = (BYTE) (dwUncompressedSize >> 16);							/* UNCOMPRESSED SIZE HIGH */
	tCENTRAL_DIRECTORY_FILE_HEADER.f.UNCOMPRESSED_SIZE[3] = (BYTE) (dwUncompressedSize >> 24);							/* UNCOMPRESSED SIZE HIGH-HIGH */

	tCENTRAL_DIRECTORY_FILE_HEADER.f.FILE_NAME_LENGTH[0] = (BYTE) sFile.size();											/* FILE SIZE LOW */
	tCENTRAL_DIRECTORY_FILE_HEADER.f.FILE_NAME_LENGTH[1] = (BYTE) (sFile.size() >> 8);									/* FILE SIZE HIGH */

  //memcpy(tCENTRAL_DIRECTORY_FILE_HEADER.f.EXTRA_FIELD_LENGTH, "\x00\x00", 2);											/* UNUSED */
  //memcpy(tCENTRAL_DIRECTORY_FILE_HEADER.f.FILE_COMMENT_LENGTH, "\x00\x00", 2);										/* UNUSED */
  //memcpy(tCENTRAL_DIRECTORY_FILE_HEADER.f.DISK_NUMBER_WHERE_FILE_STARTS, "\x00\x00", 2);								/* UNUSED */
  //memcpy(tCENTRAL_DIRECTORY_FILE_HEADER.f.INTERNAL_FILE_ATTRIBUTES, "\x00\x00", 2);									/* UNUSED */

	tCENTRAL_DIRECTORY_FILE_HEADER.f.EXTERNAL_FILE_ATTRIBUTES[0] = (BYTE) tPWIN32_FIND_DATA->dwFileAttributes;			/* FILE ATTRIBUTE LOW-LOW */
	tCENTRAL_DIRECTORY_FILE_HEADER.f.EXTERNAL_FILE_ATTRIBUTES[1] = (BYTE) (tPWIN32_FIND_DATA->dwFileAttributes >> 8);	/* FILE ATTRIBUTE LOW */
	tCENTRAL_DIRECTORY_FILE_HEADER.f.EXTERNAL_FILE_ATTRIBUTES[2] = (BYTE) (tPWIN32_FIND_DATA->dwFileAttributes >> 16);	/* FILE ATTRIBUTE HIGH */
	tCENTRAL_DIRECTORY_FILE_HEADER.f.EXTERNAL_FILE_ATTRIBUTES[3] = (BYTE) (tPWIN32_FIND_DATA->dwFileAttributes >> 24);	/* FILE ATTRIBUTE HIGH-HIGH */

	tCENTRAL_DIRECTORY_FILE_HEADER.f.RELATIVE_OFFSET_LOCAL_FILE_HEADER[0] = (BYTE) dwOffsetLocalHeader;					/* OFFSET LOCAL FILE HEADER LOW-LOW */
	tCENTRAL_DIRECTORY_FILE_HEADER.f.RELATIVE_OFFSET_LOCAL_FILE_HEADER[1] = (BYTE) (dwOffsetLocalHeader >> 8);			/* OFFSET LOCAL FILE HEADER LOW */
	tCENTRAL_DIRECTORY_FILE_HEADER.f.RELATIVE_OFFSET_LOCAL_FILE_HEADER[2] = (BYTE) (dwOffsetLocalHeader >> 16);			/* OFFSET LOCAL FILE HEADER HIGH */
	tCENTRAL_DIRECTORY_FILE_HEADER.f.RELATIVE_OFFSET_LOCAL_FILE_HEADER[3] = (BYTE) (dwOffsetLocalHeader >> 24);			/* OFFSET LOCAL FILE HEADER HIGH-HIGH */

	memcpy(tCENTRAL_DIRECTORY_FILE_HEADER.f.FILE_NAME, sFile.c_str(), sFile.size());									/* FILE NAME */

  //BYTE byEFBuffer[255] = { '\0' };

  //memcpy(tCENTRAL_DIRECTORY_FILE_HEADER.f.EXTRA_FIELD, byEFBuffer, 255);												/* UNUSED */

  //BYTE byFCBuffer[255] = { '\0' };

  //memcpy(tCENTRAL_DIRECTORY_FILE_HEADER.f.FILE_COMMENT, byFCBuffer, 255);												/* UNUSED */

	// Copy to memory
	vZippedData.resize(vZippedData.size() + 46 + sFile.size());
	memcpy(vZippedData.data() + vZippedData.size() - 46 - sFile.size(), tCENTRAL_DIRECTORY_FILE_HEADER.v, 46 + sFile.size());

	m_wNumberOfCentralDirectories++;
}

/**
 * @brief	Allocate end of central directory record to buffer
 *
 * @author	Maxime Lagadec
 * @date	4/8/2018
 *
 * @param	[in,out] vZippedData : Buffer where data descriptor is stored
 * @param	[in] wNumberOfCentralDirectories : Total number of central directories allocated
 * @param	[in] dwSizeOfCentralDirectory : Size of the central directory buffer
 * @param	[in] dwOffsetStartCentralDirectory : Offset to the start of the central directory from the start of the buffer
 *
 */

void cZIP::AllocateEndOfCentralDirectoryRecord(std::vector<BYTE> &vZippedData, const WORD wNumberOfCentralDirectories, const DWORD dwSizeOfCentralDirectory, const DWORD dwOffsetStartCentralDirectory)
{
	END_OF_CENTRAL_DIRECTORY_RECORD tEND_OF_CENTRAL_DIRECTORY_RECORD = { '\0' };

	memcpy(tEND_OF_CENTRAL_DIRECTORY_RECORD.f.END_OF_CENTRAL_DIRECTORY_SIGNATURE, "\x50\x4b\x05\x06", 4);								/* SIGNATURE - LITTLE_ENDIAN */
  //memcpy(tEND_OF_CENTRAL_DIRECTORY_RECORD.f.NUMBER_OF_THIS_DISK, "\x00\x00", 2);														/* UNUSED */
  //memcpy(tEND_OF_CENTRAL_DIRECTORY_RECORD.f.DISK_WHERE_CENTRAL_DIRECTORY_STARTS, "\x00\x00", 2);										/* UNUSED */

	tEND_OF_CENTRAL_DIRECTORY_RECORD.f.NUMBER_OF_CENTRAL_DIRECTORY_RECORDS_ON_THIS_DISK[0] = (BYTE) wNumberOfCentralDirectories;		/* NUMBER OF CENTRAL DIRECTORIES LOW */
	tEND_OF_CENTRAL_DIRECTORY_RECORD.f.NUMBER_OF_CENTRAL_DIRECTORY_RECORDS_ON_THIS_DISK[1] = (BYTE) (wNumberOfCentralDirectories >> 8);	/* NUMBER OF CETRANL DIRECTORIES HIGH */

	tEND_OF_CENTRAL_DIRECTORY_RECORD.f.TOTAL_NUMBER_OF_CENTRAL_DIRECTORY_RECORDS[0] = (BYTE) wNumberOfCentralDirectories;				/* NUMBER OF CENTRAL DIRECTORIES LOW */
	tEND_OF_CENTRAL_DIRECTORY_RECORD.f.TOTAL_NUMBER_OF_CENTRAL_DIRECTORY_RECORDS[1] = (BYTE) (wNumberOfCentralDirectories >> 8);		/* NUMBER OF CETRANL DIRECTORIES HIGH */

	tEND_OF_CENTRAL_DIRECTORY_RECORD.f.SIZE_OF_CENTRAL_DIRECTORY[0] = (BYTE) dwSizeOfCentralDirectory;									/* SIZE OF CENTRAL DIRECTORY LOW-LOW */
	tEND_OF_CENTRAL_DIRECTORY_RECORD.f.SIZE_OF_CENTRAL_DIRECTORY[1] = (BYTE) (dwSizeOfCentralDirectory >> 8);							/* SIZE OF CENTRAL DIRECTORY LOW */
	tEND_OF_CENTRAL_DIRECTORY_RECORD.f.SIZE_OF_CENTRAL_DIRECTORY[2] = (BYTE) (dwSizeOfCentralDirectory >> 16);							/* SIZE OF CENTRAL DIRECTORY HIGH */
	tEND_OF_CENTRAL_DIRECTORY_RECORD.f.SIZE_OF_CENTRAL_DIRECTORY[3] = (BYTE) (dwSizeOfCentralDirectory >> 24);							/* SIZE OF CENTRAL DIRECTORY HIGH-HIGH */

	tEND_OF_CENTRAL_DIRECTORY_RECORD.f.OFFSET_OF_START_OF_CENTRAL_DIRECTORY[0] = (BYTE) dwOffsetStartCentralDirectory;					/* OFFSET START OF CENTRAL DIRECTORY LOW-LOW */
	tEND_OF_CENTRAL_DIRECTORY_RECORD.f.OFFSET_OF_START_OF_CENTRAL_DIRECTORY[1] = (BYTE) (dwOffsetStartCentralDirectory >> 8);			/* OFFSET START OF CENTRAL DIRECTORY LOW */
	tEND_OF_CENTRAL_DIRECTORY_RECORD.f.OFFSET_OF_START_OF_CENTRAL_DIRECTORY[2] = (BYTE) (dwOffsetStartCentralDirectory >> 16);			/* OFFSET START OF CENTRAL DIRECTORY HIGH */
	tEND_OF_CENTRAL_DIRECTORY_RECORD.f.OFFSET_OF_START_OF_CENTRAL_DIRECTORY[3] = (BYTE) (dwOffsetStartCentralDirectory >> 24);			/* OFFSET START OF CENTRAL DIRECTORY HIGH-HIGH */

  //memcpy(tEND_OF_CENTRAL_DIRECTORY_RECORD.f.COMMENT_LENGTH, "\x00\x00", 2);															/* UNUSED */

  //BYTE byCBuffer[255] = { '\0' };

  //memcpy(tEND_OF_CENTRAL_DIRECTORY_RECORD.f.COMMENT, byCBuffer, 255);																	/* UNUSED */

	// Copy to memory
	vZippedData.resize(vZippedData.size() + 22);
	memcpy(vZippedData.data() + vZippedData.size() - 22, tEND_OF_CENTRAL_DIRECTORY_RECORD.v, 22);
}

/**
 * @brief	Compress source buffer to destination buffer
 *
 * @author	Maxime Lagadec
 * @date	4/11/2018
 *
 * @param	[in,out] dest : Buffer that receives compressed data
 * @param	[in,out] destLen : Length of the destination buffer
 * @param	[in] source : Buffer to be compressed
 * @param	[in] sourceLen : Length of the source buffer
 * @param	[in] level : 0 for store, 1 is fastest and 9 is best compress ratio
 *
 * @note	destLen gets updated with the actual size of the compression
 * @note	Compress is RAW (no zlib header) and uses deflate method
 *
 * @return	SUCCESS : 0
 * @return	ERROR : zlib's defined errors
 *
 */

int cZIP::compressRAW(Bytef *dest, uLongf *destLen, const Bytef *source, uLong sourceLen, int level)
{
	z_stream stream;
	int err;

	stream.next_in = (Bytef*)source;
	stream.avail_in = (uInt)sourceLen;
#ifdef MAXSEG_64K
	/* Check for source > 64K on 16-bit machine: */
	if ((uLong)stream.avail_in != sourceLen) return Z_BUF_ERROR;
#endif
	stream.next_out = dest;
	stream.avail_out = (uInt)*destLen;
	if ((uLong)stream.avail_out != *destLen) return Z_BUF_ERROR;

	stream.zalloc = (alloc_func)0;
	stream.zfree = (free_func)0;
	stream.opaque = (voidpf)0;

	err = deflateInit2(&stream, level, Z_DEFLATED, -15, 8, Z_DEFAULT_STRATEGY);
	if (err != Z_OK) return err;

	err = deflate(&stream, Z_FINISH);
	if (err != Z_STREAM_END) {
		deflateEnd(&stream);
		return err == Z_OK ? Z_BUF_ERROR : err;
	}
	*destLen = stream.total_out;

	err = deflateEnd(&stream);
	return err;
}