#include <algorithm>

#include "cUNZIP.h"

// Define only when using for transfert
// For local computer use, undefine
// Do this for both cZIP and cUNZIP
#define __CODE_PAGE_UTF8_
#include "TString.h"

// TODO : Define more errors type
#define UNZIP_SUCCESS	0x0000;
#define UNZIP_ERROR		0x0001;

/**
 * @brief	Unzip source file to target folder
 *
 * @author	Maxime Lagadec
 * @date	4/14/2018
 *
 * @param	[in] wsSource : Path to zip to unzip
 * @param	[in] wsDestination : Path to folder where to unzip
 *
 * @return	SUCCESS : 0
 * @return	ERROR : 1
 *
 */

DWORD cUNZIP::UnzipToFolder(const std::wstring wsSource, const std::wstring wsDestination)
{
	HANDLE hZipFile;

	// Open file reading
	hZipFile = CreateFile(
		ToTString(wsSource).c_str(),
		GENERIC_READ,
		FILE_SHARE_READ | FILE_SHARE_WRITE,
		NULL,
		OPEN_EXISTING,
		FILE_ATTRIBUTE_NORMAL,
		NULL
	);

	if (hZipFile == INVALID_HANDLE_VALUE)
		return UNZIP_ERROR;

	return UnzipToFolder(wsDestination, hZipFile);
}

/**
 * @brief	Unzip source data to target folder
 *
 * @author	Maxime Lagadec
 * @date	4/14/2018
 *
 * @param	[in] wsDestination : Path to folder where to unzip
 * @param	[in] pbyData : Data to unzip
 * @param	[in] dwSize : Size of the data to unzip
 *
 * @return	SUCCESS : 0
 * @return	ERROR : 1
 *
 */

DWORD cUNZIP::UnzipToFolder(const std::wstring wsDestination, BYTE* pbyData, DWORD dwSize)
{
	DWORD dwNbEntries = 0;

	// Make sure directory has no double backslash ("\\\\") except for network drive
	if (wsDestination.find(L"\\\\") != std::wstring::npos)
	{
		if (wsDestination.rfind(L"\\\\") >= 1)
			return UNZIP_ERROR;
	}

	// Make sure directory is a folder (ends with "\\")
	if (wsDestination.substr(wsDestination.length() - 1) != L"\\")
		return UNZIP_ERROR;

	// Load zip's informations
	if (LoadZIPStructure(pbyData, dwSize))
		return UNZIP_ERROR;

	dwNbEntries = m_vCENTRAL_DIRECTORY_FILE_HEADER.size();

	// Create extraction paths
	for (DWORD dwLoop = 0; dwLoop < dwNbEntries; dwLoop++)
	{
		if (CreateExtractFile(wsDestination, dwLoop))
			return UNZIP_ERROR;
	}

	// Extract files
	for (DWORD dwLoop = dwNbEntries; dwLoop--;)
	{
		if (ExtractFile(wsDestination, dwLoop, pbyData))
			return UNZIP_ERROR;
	}

	// Update files' time and date
	for (DWORD dwLoop = dwNbEntries; dwLoop--;)
	{
		if (UpdateFileTimeDate(wsDestination, dwLoop))
			return UNZIP_ERROR;
	}

	return UNZIP_SUCCESS;
}

/**
 * @brief	Unzip source data to target folder
 *
 * @author	Maxime Lagadec
 * @date	4/14/2018
 *
 * @param	[in] wsDestination : Path to folder where to unzip
 * @param	[in] hZipFile : Handle referring to opened zip file to unzip
 *
 * @return	SUCCESS : 0
 * @return	ERROR : 1
 *
 */

DWORD cUNZIP::UnzipToFolder(const std::wstring wsDestination, HANDLE hZipFile)
{
	DWORD dwNbEntries = 0;

	// Make sure directory has no double backslash ("\\\\") except for network drive
	if (wsDestination.find(L"\\\\") != std::wstring::npos)
	{
		if (wsDestination.rfind(L"\\\\") >= 1)
			return UNZIP_ERROR;
	}

	// Make sure directory is a folder (ends with "\\")
	if (wsDestination.substr(wsDestination.length() - 1) != L"\\")
		return UNZIP_ERROR;

	// Load zip's informations
	if (LoadZIPStructure(hZipFile))
		return UNZIP_ERROR;

	dwNbEntries = m_vCENTRAL_DIRECTORY_FILE_HEADER.size();

	// Create extraction paths
	for (DWORD dwLoop = 0; dwLoop < dwNbEntries; dwLoop++)
	{
		if (CreateExtractFile(wsDestination, dwLoop))
			return UNZIP_ERROR;
	}

	// Extract files
	for (DWORD dwLoop = dwNbEntries; dwLoop--;)
	{
		if (ExtractFile(wsDestination, dwLoop, hZipFile))
			return UNZIP_ERROR;
	}

	// Update files' time and date
	for (DWORD dwLoop = dwNbEntries; dwLoop--;)
	{
		if (UpdateFileTimeDate(wsDestination, dwLoop))
			return UNZIP_ERROR;
	}

	return UNZIP_SUCCESS;
}

/**
 * @brief	Flush all internal memory
 *
 * @author	Maxime Lagadec
 * @date	4/14/2018
 *
 */

void cUNZIP::FlushMemory()
{
	m_vLOCAL_FILE_HEADER.clear();
	m_vLOCAL_FILE_HEADER.resize(0);
	m_vLOCAL_FILE_HEADER.shrink_to_fit();

	m_vCENTRAL_DIRECTORY_FILE_HEADER.clear();
	m_vCENTRAL_DIRECTORY_FILE_HEADER.resize(0);
	m_vCENTRAL_DIRECTORY_FILE_HEADER.shrink_to_fit();

	END_OF_CENTRAL_DIRECTORY_RECORD tEND_OF_CENTRAL_DIRECTORY_RECORD = { '\0' };

	m_tEND_OF_CENTRAL_DIRECTORY_RECORD = tEND_OF_CENTRAL_DIRECTORY_RECORD;
}

/**
 * @brief	Load zip file's information into internal memory
 *
 * @author	Maxime Lagadec
 * @date	4/14/2018
 *
 * @param	[in] pbyData : Data to unzip
 * @param	[in] dwSize : Size of the data to unzip
 *
 * @return	SUCCESS : 0
 * @return	ERROR : 1
 *
 */

DWORD cUNZIP::LoadZIPStructure(BYTE* pbyData, DWORD dwSize)
{
	if (dwSize == 0)
		return UNZIP_ERROR;

	FlushMemory();

	do
	{
		// LOCAL_FILE_HEADER (0x04034b50)
		if (pbyData[0] == '\x50' && pbyData[1] == '\x4b' && pbyData[2] == '\x03' && pbyData[3] == '\x04')
		{
			LOCAL_FILE_HEADER tLOCAL_FILE_HEADER = { '\0' };

			memcpy(tLOCAL_FILE_HEADER.v, pbyData, 30);

			{
				WORD wFileNameLength = tLOCAL_FILE_HEADER.f.FILE_NAME_LENGTH[0] + (tLOCAL_FILE_HEADER.f.FILE_NAME_LENGTH[1] << 8);
				WORD wExtraFieldLength = tLOCAL_FILE_HEADER.f.EXTRA_FIELD_LENGTH[0] + (tLOCAL_FILE_HEADER.f.EXTRA_FIELD_LENGTH[1] << 8);

				if (wFileNameLength == 0)
				{
					FlushMemory();
					return UNZIP_ERROR;
				}

				memcpy(tLOCAL_FILE_HEADER.f.FILE_NAME, pbyData + 30, wFileNameLength);
				memcpy(tLOCAL_FILE_HEADER.f.EXTRA_FIELD, pbyData + 30 + wExtraFieldLength, wExtraFieldLength);

				pbyData += 30 + wFileNameLength + wExtraFieldLength;
				dwSize -= 30 + wFileNameLength + wExtraFieldLength;
			}

			{
				DWORD dwCompressedSize = tLOCAL_FILE_HEADER.f.COMPRESSED_SIZE[0] + (tLOCAL_FILE_HEADER.f.COMPRESSED_SIZE[1] << 8) + (tLOCAL_FILE_HEADER.f.COMPRESSED_SIZE[2] << 16) + (tLOCAL_FILE_HEADER.f.COMPRESSED_SIZE[3] << 24);
				DWORD dwUncompressedSize = tLOCAL_FILE_HEADER.f.UNCOMPRESSED_SIZE[0] + (tLOCAL_FILE_HEADER.f.UNCOMPRESSED_SIZE[1] << 8) + (tLOCAL_FILE_HEADER.f.UNCOMPRESSED_SIZE[2] << 16) + (tLOCAL_FILE_HEADER.f.UNCOMPRESSED_SIZE[3] << 24);

				if (dwCompressedSize)
					if (!dwUncompressedSize)
						return UNZIP_ERROR;

				if (dwUncompressedSize)
					if (!dwCompressedSize)
						return UNZIP_ERROR;

				pbyData += dwCompressedSize;
				dwSize -= dwCompressedSize;
			}

			// DATA_DESCRIPTOR (0x08074b50)
			if (0x08 == (tLOCAL_FILE_HEADER.f.GENERAL_PURPOSE_BIT_FLAG[0] & 0x08))
			{
				// SIGNATURE DATA_DESCRIPTOR
				if (pbyData[0] == '\x50' && pbyData[1] == '\x4b' && pbyData[2] == '\x07' && pbyData[3] == '\x08')
				{
					memcpy(tLOCAL_FILE_HEADER.f.CRC32, pbyData + 4, 4);
					memcpy(tLOCAL_FILE_HEADER.f.COMPRESSED_SIZE, pbyData + 8, 4);
					memcpy(tLOCAL_FILE_HEADER.f.UNCOMPRESSED_SIZE, pbyData + 12, 4);

					pbyData += 16;
					dwSize -= 16;
				}
				// SIGNATURE LOCAL_FILE_HEADER
				else if (pbyData[12] == '\x50' && pbyData[13] == '\x4b' && pbyData[14] == '\x03' && pbyData[15] == '\x04')
				{
					memcpy(tLOCAL_FILE_HEADER.f.CRC32, pbyData, 4);
					memcpy(tLOCAL_FILE_HEADER.f.COMPRESSED_SIZE, pbyData + 4, 4);
					memcpy(tLOCAL_FILE_HEADER.f.UNCOMPRESSED_SIZE, pbyData + 8, 4);

					pbyData += 12;
					dwSize -= 12;
				}
				// SIGNATURE CENTRAL_DIRECTORY_FILE_HEADER
				else if (pbyData[12] == '\x50' && pbyData[13] == '\x4b' && pbyData[14] == '\x01' && pbyData[15] == '\x02')
				{
					memcpy(tLOCAL_FILE_HEADER.f.CRC32, pbyData, 4);
					memcpy(tLOCAL_FILE_HEADER.f.COMPRESSED_SIZE, pbyData + 4, 4);
					memcpy(tLOCAL_FILE_HEADER.f.UNCOMPRESSED_SIZE, pbyData + 8, 4);

					pbyData += 12;
					dwSize -= 12;
				}
			}

			m_vLOCAL_FILE_HEADER.push_back(tLOCAL_FILE_HEADER);
		}
		// CENTRAL_DIRECTORY_FILE_HEADER (0x02014b50)
		else if (pbyData[0] == '\x50' && pbyData[1] == '\x4b' && pbyData[2] == '\x01' && pbyData[3] == '\x02')
		{
			CENTRAL_DIRECTORY_FILE_HEADER tCENTRAL_DIRECTORY_FILE_HEADER = { '\0' };

			memcpy(tCENTRAL_DIRECTORY_FILE_HEADER.v, pbyData, 46);

			{
				WORD wFileNameLength = tCENTRAL_DIRECTORY_FILE_HEADER.f.FILE_NAME_LENGTH[0] + (tCENTRAL_DIRECTORY_FILE_HEADER.f.FILE_NAME_LENGTH[1] << 8);
				WORD wExtraFieldLength = tCENTRAL_DIRECTORY_FILE_HEADER.f.EXTRA_FIELD_LENGTH[0] + (tCENTRAL_DIRECTORY_FILE_HEADER.f.EXTRA_FIELD_LENGTH[1] << 8);
				WORD wFileCommentLength = tCENTRAL_DIRECTORY_FILE_HEADER.f.FILE_COMMENT_LENGTH[0] + (tCENTRAL_DIRECTORY_FILE_HEADER.f.FILE_COMMENT_LENGTH[1] << 8);

				if (wFileNameLength == 0)
				{
					FlushMemory();
					return UNZIP_ERROR;
				}

				memcpy(tCENTRAL_DIRECTORY_FILE_HEADER.f.FILE_NAME, pbyData + 46, wFileNameLength);
				memcpy(tCENTRAL_DIRECTORY_FILE_HEADER.f.EXTRA_FIELD, pbyData + 46 + wFileNameLength, wExtraFieldLength);
				memcpy(tCENTRAL_DIRECTORY_FILE_HEADER.f.FILE_COMMENT, pbyData + 46 + wFileNameLength + wExtraFieldLength, wFileCommentLength);

				pbyData += 46 + wFileNameLength + wExtraFieldLength + wFileCommentLength;
				dwSize -= 46 + wFileNameLength + wExtraFieldLength + wFileCommentLength;
			}

			m_vCENTRAL_DIRECTORY_FILE_HEADER.push_back(tCENTRAL_DIRECTORY_FILE_HEADER);
		}
		// END_OF_CENTRAL_DIRECTORY_RECORD (0x06054b50)
		else if (pbyData[0] == '\x50' && pbyData[1] == '\x4b' && pbyData[2] == '\x05' && pbyData[3] == '\x06')
		{
			END_OF_CENTRAL_DIRECTORY_RECORD tEND_OF_CENTRAL_DIRECTORY_RECORD = { '\0' };

			memcpy(tEND_OF_CENTRAL_DIRECTORY_RECORD.v, pbyData, 22);

			{
				WORD wCommentLength = tEND_OF_CENTRAL_DIRECTORY_RECORD.f.COMMENT_LENGTH[0] + (tEND_OF_CENTRAL_DIRECTORY_RECORD.f.COMMENT_LENGTH[1] << 8);

				memcpy(tEND_OF_CENTRAL_DIRECTORY_RECORD.f.COMMENT, pbyData + 22, wCommentLength);

				pbyData += 22 + wCommentLength;
				dwSize -= 22 + wCommentLength;
			}

			if (dwSize != 0)
			{
				FlushMemory();
				return UNZIP_ERROR;
			}

			m_tEND_OF_CENTRAL_DIRECTORY_RECORD = tEND_OF_CENTRAL_DIRECTORY_RECORD;
		}
		else
		{
			FlushMemory();
			return UNZIP_ERROR;
		}
	} while (dwSize);

	if (m_vLOCAL_FILE_HEADER.size() != m_vCENTRAL_DIRECTORY_FILE_HEADER.size())
	{
		FlushMemory();
		return UNZIP_ERROR;
	}

	return UNZIP_SUCCESS;
}

/**
 * @brief	Load zip file's information into internal memory
 *
 * @author	Maxime Lagadec
 * @date	4/14/2018
 *
 * @param	[in] pbyData : Data to unzip
 * @param	[in] hZipFile : Handle referring to opened zip file to unzip
 *
 * @return	SUCCESS : 0
 * @return	ERROR : 1
 *
 */

DWORD cUNZIP::LoadZIPStructure(HANDLE hZipFile)
{
	BYTE pbyData[4];
	DWORD dwSize = GetFileSize(hZipFile, NULL);

	if (INVALID_SET_FILE_POINTER == SetFilePointer(hZipFile, 0, 0, FILE_BEGIN))
		return UNZIP_ERROR;

	FlushMemory();

	do
	{
		ReadFile(hZipFile, pbyData, 4, NULL, NULL);
		SetFilePointer(hZipFile, -4, NULL, FILE_CURRENT);

		// LOCAL_FILE_HEADER (0x04034b50)
		if (pbyData[0] == '\x50' && pbyData[1] == '\x4b' && pbyData[2] == '\x03' && pbyData[3] == '\x04')
		{
			LOCAL_FILE_HEADER tLOCAL_FILE_HEADER = { '\0' };

			ReadFile(hZipFile, tLOCAL_FILE_HEADER.v, 30, NULL, NULL);

			{
				WORD wFileNameLength = tLOCAL_FILE_HEADER.f.FILE_NAME_LENGTH[0] + (tLOCAL_FILE_HEADER.f.FILE_NAME_LENGTH[1] << 8);
				WORD wExtraFieldLength = tLOCAL_FILE_HEADER.f.EXTRA_FIELD_LENGTH[0] + (tLOCAL_FILE_HEADER.f.EXTRA_FIELD_LENGTH[1] << 8);

				if (wFileNameLength == 0)
				{
					FlushMemory();
					return UNZIP_ERROR;
				}

				ReadFile(hZipFile, tLOCAL_FILE_HEADER.f.FILE_NAME, wFileNameLength, NULL, NULL);
				ReadFile(hZipFile, tLOCAL_FILE_HEADER.f.FILE_NAME, wExtraFieldLength, NULL, NULL);

				dwSize -= 30 + wFileNameLength + wExtraFieldLength;
			}

			{
				DWORD dwCompressedSize = tLOCAL_FILE_HEADER.f.COMPRESSED_SIZE[0] + (tLOCAL_FILE_HEADER.f.COMPRESSED_SIZE[1] << 8) + (tLOCAL_FILE_HEADER.f.COMPRESSED_SIZE[2] << 16) + (tLOCAL_FILE_HEADER.f.COMPRESSED_SIZE[3] << 24);
				DWORD dwUncompressedSize = tLOCAL_FILE_HEADER.f.UNCOMPRESSED_SIZE[0] + (tLOCAL_FILE_HEADER.f.UNCOMPRESSED_SIZE[1] << 8) + (tLOCAL_FILE_HEADER.f.UNCOMPRESSED_SIZE[2] << 16) + (tLOCAL_FILE_HEADER.f.UNCOMPRESSED_SIZE[3] << 24);

				if (dwCompressedSize)
					if (!dwUncompressedSize)
						return UNZIP_ERROR;

				if (dwUncompressedSize)
					if (!dwCompressedSize)
						return UNZIP_ERROR;

				SetFilePointer(hZipFile, dwCompressedSize, NULL, FILE_CURRENT);
				dwSize -= dwCompressedSize;
			}

			// DATA_DESCRIPTOR (0x08074b50)
			if (0x08 == (tLOCAL_FILE_HEADER.f.GENERAL_PURPOSE_BIT_FLAG[0] & 0x08))
			{
				// SIGNATURE DATA_DESCRIPTOR
				if (pbyData[0] == '\x50' && pbyData[1] == '\x4b' && pbyData[2] == '\x07' && pbyData[3] == '\x08')
				{
					SetFilePointer(hZipFile, 4, NULL, FILE_CURRENT);
					ReadFile(hZipFile, tLOCAL_FILE_HEADER.f.CRC32, 4, NULL, NULL);
					ReadFile(hZipFile, tLOCAL_FILE_HEADER.f.COMPRESSED_SIZE, 4, NULL, NULL);
					ReadFile(hZipFile, tLOCAL_FILE_HEADER.f.UNCOMPRESSED_SIZE, 4, NULL, NULL);

					dwSize -= 16;
				}
				// SIGNATURE LOCAL_FILE_HEADER
				else if (pbyData[12] == '\x50' && pbyData[13] == '\x4b' && pbyData[14] == '\x03' && pbyData[15] == '\x04')
				{
					ReadFile(hZipFile, tLOCAL_FILE_HEADER.f.CRC32, 4, NULL, NULL);
					ReadFile(hZipFile, tLOCAL_FILE_HEADER.f.COMPRESSED_SIZE, 4, NULL, NULL);
					ReadFile(hZipFile, tLOCAL_FILE_HEADER.f.UNCOMPRESSED_SIZE, 4, NULL, NULL);

					dwSize -= 12;
				}
				// SIGNATURE CENTRAL_DIRECTORY_FILE_HEADER
				else if (pbyData[12] == '\x50' && pbyData[13] == '\x4b' && pbyData[14] == '\x01' && pbyData[15] == '\x02')
				{
					ReadFile(hZipFile, tLOCAL_FILE_HEADER.f.CRC32, 4, NULL, NULL);
					ReadFile(hZipFile, tLOCAL_FILE_HEADER.f.COMPRESSED_SIZE, 4, NULL, NULL);
					ReadFile(hZipFile, tLOCAL_FILE_HEADER.f.UNCOMPRESSED_SIZE, 4, NULL, NULL);

					dwSize -= 12;
				}
			}

			m_vLOCAL_FILE_HEADER.push_back(tLOCAL_FILE_HEADER);
		}
		// CENTRAL_DIRECTORY_FILE_HEADER (0x02014b50)
		else if (pbyData[0] == '\x50' && pbyData[1] == '\x4b' && pbyData[2] == '\x01' && pbyData[3] == '\x02')
		{
			CENTRAL_DIRECTORY_FILE_HEADER tCENTRAL_DIRECTORY_FILE_HEADER = { '\0' };

			ReadFile(hZipFile, tCENTRAL_DIRECTORY_FILE_HEADER.v, 46, NULL, NULL);

			{
				WORD wFileNameLength = tCENTRAL_DIRECTORY_FILE_HEADER.f.FILE_NAME_LENGTH[0] + (tCENTRAL_DIRECTORY_FILE_HEADER.f.FILE_NAME_LENGTH[1] << 8);
				WORD wExtraFieldLength = tCENTRAL_DIRECTORY_FILE_HEADER.f.EXTRA_FIELD_LENGTH[0] + (tCENTRAL_DIRECTORY_FILE_HEADER.f.EXTRA_FIELD_LENGTH[1] << 8);
				WORD wFileCommentLength = tCENTRAL_DIRECTORY_FILE_HEADER.f.FILE_COMMENT_LENGTH[0] + (tCENTRAL_DIRECTORY_FILE_HEADER.f.FILE_COMMENT_LENGTH[1] << 8);

				if (wFileNameLength == 0)
				{
					FlushMemory();
					return UNZIP_ERROR;
				}

				ReadFile(hZipFile, tCENTRAL_DIRECTORY_FILE_HEADER.f.FILE_NAME, wFileNameLength, NULL, NULL);
				ReadFile(hZipFile, tCENTRAL_DIRECTORY_FILE_HEADER.f.EXTRA_FIELD, wExtraFieldLength, NULL, NULL);
				ReadFile(hZipFile, tCENTRAL_DIRECTORY_FILE_HEADER.f.FILE_COMMENT, wFileCommentLength, NULL, NULL);

				dwSize -= 46 + wFileNameLength + wExtraFieldLength + wFileCommentLength;
			}

			m_vCENTRAL_DIRECTORY_FILE_HEADER.push_back(tCENTRAL_DIRECTORY_FILE_HEADER);
		}
		// END_OF_CENTRAL_DIRECTORY_RECORD (0x06054b50)
		else if (pbyData[0] == '\x50' && pbyData[1] == '\x4b' && pbyData[2] == '\x05' && pbyData[3] == '\x06')
		{
			END_OF_CENTRAL_DIRECTORY_RECORD tEND_OF_CENTRAL_DIRECTORY_RECORD = { '\0' };

			ReadFile(hZipFile, tEND_OF_CENTRAL_DIRECTORY_RECORD.v, 22, NULL, NULL);

			{
				WORD wCommentLength = tEND_OF_CENTRAL_DIRECTORY_RECORD.f.COMMENT_LENGTH[0] + (tEND_OF_CENTRAL_DIRECTORY_RECORD.f.COMMENT_LENGTH[1] << 8);

				ReadFile(hZipFile, tEND_OF_CENTRAL_DIRECTORY_RECORD.f.COMMENT, wCommentLength, NULL, NULL);

				dwSize -= 22 + wCommentLength;
			}

			if (dwSize != 0)
			{
				FlushMemory();
				return UNZIP_ERROR;
			}

			m_tEND_OF_CENTRAL_DIRECTORY_RECORD = tEND_OF_CENTRAL_DIRECTORY_RECORD;
		}
		else
		{
			FlushMemory();
			return UNZIP_ERROR;
		}
	} while (dwSize);

	if (m_vLOCAL_FILE_HEADER.size() != m_vCENTRAL_DIRECTORY_FILE_HEADER.size())
	{
		FlushMemory();
		return UNZIP_ERROR;
	}

	return UNZIP_SUCCESS;
}

/**
 * @brief	Create the file where data will be extracted to
 *
 * @author	Maxime Lagadec
 * @date	4/14/2018
 *
 * @param	[in] wsDirectory : Path to folder where to unzip
 * @param	[in] dwFileNumber : Number of the affected file stored in internal memory
 *
 * @return	SUCCESS : 0
 * @return	ERROR : 1
 *
 */

DWORD cUNZIP::CreateExtractFile(const std::wstring wsDirectory, const DWORD dwFileNumber)
{
	HANDLE hFile;

	std::wstring wsFile = ToWString((char *)m_vCENTRAL_DIRECTORY_FILE_HEADER[dwFileNumber].f.FILE_NAME);
	std::replace(wsFile.begin(), wsFile.end(), L'/', L'\\');

	wsFile.insert(0, wsDirectory);

	// Gather file's information
	DWORD dwExternalFileAttributes = m_vCENTRAL_DIRECTORY_FILE_HEADER[dwFileNumber].f.EXTERNAL_FILE_ATTRIBUTES[0] + (m_vCENTRAL_DIRECTORY_FILE_HEADER[dwFileNumber].f.EXTERNAL_FILE_ATTRIBUTES[1] << 8) + (m_vCENTRAL_DIRECTORY_FILE_HEADER[dwFileNumber].f.EXTERNAL_FILE_ATTRIBUTES[2] << 16) + (m_vCENTRAL_DIRECTORY_FILE_HEADER[dwFileNumber].f.EXTERNAL_FILE_ATTRIBUTES[3] << 24);

	// Create path to directory
	if (CreateRootPath(wsFile))
		return UNZIP_ERROR;

	// Make sure we are not working with a directory
	if (wsFile.substr(wsFile.length() - 1) != L"\\")
	{
		hFile = CreateFile(
			ToTString(wsFile).c_str(),
			GENERIC_READ | GENERIC_WRITE,
			FILE_SHARE_READ | FILE_SHARE_WRITE,
			NULL,
			CREATE_NEW,
			FILE_ATTRIBUTE_NORMAL,
			NULL
		);

		if (hFile == INVALID_HANDLE_VALUE)
			return UNZIP_ERROR;

		CloseHandle(hFile);
	}

	// Update file's attributes
	if (dwExternalFileAttributes != 0)
		if (!SetFileAttributes(ToTString(wsFile).c_str(), dwExternalFileAttributes))
			return UNZIP_ERROR;

	return UNZIP_SUCCESS;
}

/**
 * @brief	Extract the file
 *
 * @author	Maxime Lagadec
 * @date	4/14/2018
 *
 * @param	[in] wsDirectory : Path to folder where to unzip
 * @param	[in] dwFileNumber : Number of the affected file stored in internal memory
 * @param	[in] pbyData : Data to unzip
 *
 * @return	SUCCESS : 0
 * @return	ERROR : 1
 *
 * @note	File's location must have been created previously (See CreateExtractFile)
 *
 */

DWORD cUNZIP::ExtractFile(const std::wstring wsDirectory, const DWORD dwFileNumber, BYTE* pbyData)
{
	HANDLE hFile;

	DWORD dwCRC32Compare;
	DWORD dwBytesWritten;

	std::wstring wsFile = ToWString((char *)m_vCENTRAL_DIRECTORY_FILE_HEADER[dwFileNumber].f.FILE_NAME);
	std::replace(wsFile.begin(), wsFile.end(), L'/', L'\\');

	// Make sure we are not working with a directory
	if (wsFile.substr(wsFile.length() - 1) == L"\\")
		return UNZIP_SUCCESS;

	wsFile.insert(0, wsDirectory);

	// Gather file's information
	WORD wCompressionMethod = m_vCENTRAL_DIRECTORY_FILE_HEADER[dwFileNumber].f.COMPRESSION_METHOD[0] + (m_vCENTRAL_DIRECTORY_FILE_HEADER[dwFileNumber].f.COMPRESSION_METHOD[1] << 8);

	DWORD dwCRC32 = m_vCENTRAL_DIRECTORY_FILE_HEADER[dwFileNumber].f.CRC32[0] + (m_vCENTRAL_DIRECTORY_FILE_HEADER[dwFileNumber].f.CRC32[1] << 8) + (m_vCENTRAL_DIRECTORY_FILE_HEADER[dwFileNumber].f.CRC32[2] << 16) + (m_vCENTRAL_DIRECTORY_FILE_HEADER[dwFileNumber].f.CRC32[3] << 24);
	DWORD dwCompressedSize = m_vCENTRAL_DIRECTORY_FILE_HEADER[dwFileNumber].f.COMPRESSED_SIZE[0] + (m_vCENTRAL_DIRECTORY_FILE_HEADER[dwFileNumber].f.COMPRESSED_SIZE[1] << 8) + (m_vCENTRAL_DIRECTORY_FILE_HEADER[dwFileNumber].f.COMPRESSED_SIZE[2] << 16) + (m_vCENTRAL_DIRECTORY_FILE_HEADER[dwFileNumber].f.COMPRESSED_SIZE[3] << 24);
	DWORD dwUncompressedSize = m_vCENTRAL_DIRECTORY_FILE_HEADER[dwFileNumber].f.UNCOMPRESSED_SIZE[0] + (m_vCENTRAL_DIRECTORY_FILE_HEADER[dwFileNumber].f.UNCOMPRESSED_SIZE[1] << 8) + (m_vCENTRAL_DIRECTORY_FILE_HEADER[dwFileNumber].f.UNCOMPRESSED_SIZE[2] << 16) + (m_vCENTRAL_DIRECTORY_FILE_HEADER[dwFileNumber].f.UNCOMPRESSED_SIZE[3] << 24);
	DWORD dwRelativeOffsetLocalFileHeader = m_vCENTRAL_DIRECTORY_FILE_HEADER[dwFileNumber].f.RELATIVE_OFFSET_LOCAL_FILE_HEADER[0] + (m_vCENTRAL_DIRECTORY_FILE_HEADER[dwFileNumber].f.RELATIVE_OFFSET_LOCAL_FILE_HEADER[1] << 8) + (m_vCENTRAL_DIRECTORY_FILE_HEADER[dwFileNumber].f.RELATIVE_OFFSET_LOCAL_FILE_HEADER[2] << 16) + (m_vCENTRAL_DIRECTORY_FILE_HEADER[dwFileNumber].f.RELATIVE_OFFSET_LOCAL_FILE_HEADER[3] << 24);

	// Reposition data pointer
	pbyData += dwRelativeOffsetLocalFileHeader;

	// Open file for writing
	hFile = CreateFile(
		ToTString(wsFile).c_str(),
		GENERIC_WRITE,
		FILE_SHARE_READ,
		NULL,
		OPEN_EXISTING,
		FILE_ATTRIBUTE_NORMAL,
		NULL
	);

	if (hFile == INVALID_HANDLE_VALUE)
		return UNZIP_ERROR;

	// Compression method store
	if (wCompressionMethod == 0x00)
	{
		std::vector<BYTE> vData;

		if (dwCompressedSize != dwUncompressedSize)
		{
			CloseHandle(hFile);
			return UNZIP_ERROR;
		}

		// Copy file's data to vector
		vData.resize(dwCompressedSize);
		memcpy(vData.data(), pbyData + 30 + pbyData[26] + (pbyData[27] << 8) + pbyData[28] + (pbyData[29] << 8), dwCompressedSize);

		// Calculate and compare CRC32
		dwCRC32Compare = crc32(0L, Z_NULL, 0);
		dwCRC32Compare = crc32(dwCRC32Compare, vData.data(), dwUncompressedSize);

		if (dwCRC32Compare != dwCRC32)
		{
			CloseHandle(hFile);
			return UNZIP_ERROR;
		}

		WriteFile(hFile, vData.data(), dwUncompressedSize, &dwBytesWritten, NULL);
		CloseHandle(hFile);

		if (dwBytesWritten != dwUncompressedSize)
			return UNZIP_ERROR;
	}
	// Compression method deflate
	else if (wCompressionMethod == 0x08)
	{
		std::vector<BYTE> vCompressed;
		std::vector<BYTE> vUncompressed;

		// Copy file's data to vector
		vCompressed.resize(dwCompressedSize);
		memcpy(vCompressed.data(), pbyData + 30 + pbyData[26] + (pbyData[27] << 8) + pbyData[28] + (pbyData[29] << 8), dwCompressedSize);

		// Uncompress using inflate (RAW, -15)
		vUncompressed.resize(dwUncompressedSize);
		if (uncompressRAW(vUncompressed.data(), &dwUncompressedSize, vCompressed.data(), dwCompressedSize))
			return UNZIP_ERROR;

		// Calculate and compare CRC32
		dwCRC32Compare = crc32(0L, Z_NULL, 0);
		dwCRC32Compare = crc32(dwCRC32Compare, vUncompressed.data(), dwUncompressedSize);

		if (dwCRC32Compare != dwCRC32)
		{
			CloseHandle(hFile);
			return UNZIP_ERROR;
		}

		WriteFile(hFile, vUncompressed.data(), dwUncompressedSize, &dwBytesWritten, NULL);
		CloseHandle(hFile);

		if (dwBytesWritten != dwUncompressedSize)
			return UNZIP_ERROR;
	}
	// Compression method unhandled
	else
	{
		CloseHandle(hFile);
		return UNZIP_ERROR;
	}

	return UNZIP_SUCCESS;
}

/**
 * @brief	Extract the file
 *
 * @author	Maxime Lagadec
 * @date	4/14/2018
 *
 * @param	[in] wsDirectory : Path to folder where to unzip
 * @param	[in] dwFileNumber : Number of the affected file stored in internal memory
 * @param	[in] hZipFile : Handle referring to opened zip file to unzip
 *
 * @return	SUCCESS : 0
 * @return	ERROR : 1
 *
 * @note	File's location must have been created previously (See CreateExtractFile)
 *
 */

DWORD cUNZIP::ExtractFile(const std::wstring wsDirectory, const DWORD dwFileNumber, HANDLE hZipFile)
{
	HANDLE hFile;

	BYTE pbyData[34];

	DWORD dwCRC32Compare;
	DWORD dwBytesWritten;

	std::wstring wsFile = ToWString((char *)m_vCENTRAL_DIRECTORY_FILE_HEADER[dwFileNumber].f.FILE_NAME);
	std::replace(wsFile.begin(), wsFile.end(), L'/', L'\\');

	// Make sure we are not working with a directory
	if (wsFile.substr(wsFile.length() - 1) == L"\\")
		return UNZIP_SUCCESS;

	wsFile.insert(0, wsDirectory);

	// Gather file's information
	WORD wCompressionMethod = m_vCENTRAL_DIRECTORY_FILE_HEADER[dwFileNumber].f.COMPRESSION_METHOD[0] + (m_vCENTRAL_DIRECTORY_FILE_HEADER[dwFileNumber].f.COMPRESSION_METHOD[1] << 8);

	DWORD dwCRC32 = m_vCENTRAL_DIRECTORY_FILE_HEADER[dwFileNumber].f.CRC32[0] + (m_vCENTRAL_DIRECTORY_FILE_HEADER[dwFileNumber].f.CRC32[1] << 8) + (m_vCENTRAL_DIRECTORY_FILE_HEADER[dwFileNumber].f.CRC32[2] << 16) + (m_vCENTRAL_DIRECTORY_FILE_HEADER[dwFileNumber].f.CRC32[3] << 24);
	DWORD dwCompressedSize = m_vCENTRAL_DIRECTORY_FILE_HEADER[dwFileNumber].f.COMPRESSED_SIZE[0] + (m_vCENTRAL_DIRECTORY_FILE_HEADER[dwFileNumber].f.COMPRESSED_SIZE[1] << 8) + (m_vCENTRAL_DIRECTORY_FILE_HEADER[dwFileNumber].f.COMPRESSED_SIZE[2] << 16) + (m_vCENTRAL_DIRECTORY_FILE_HEADER[dwFileNumber].f.COMPRESSED_SIZE[3] << 24);
	DWORD dwUncompressedSize = m_vCENTRAL_DIRECTORY_FILE_HEADER[dwFileNumber].f.UNCOMPRESSED_SIZE[0] + (m_vCENTRAL_DIRECTORY_FILE_HEADER[dwFileNumber].f.UNCOMPRESSED_SIZE[1] << 8) + (m_vCENTRAL_DIRECTORY_FILE_HEADER[dwFileNumber].f.UNCOMPRESSED_SIZE[2] << 16) + (m_vCENTRAL_DIRECTORY_FILE_HEADER[dwFileNumber].f.UNCOMPRESSED_SIZE[3] << 24);
	DWORD dwRelativeOffsetLocalFileHeader = m_vCENTRAL_DIRECTORY_FILE_HEADER[dwFileNumber].f.RELATIVE_OFFSET_LOCAL_FILE_HEADER[0] + (m_vCENTRAL_DIRECTORY_FILE_HEADER[dwFileNumber].f.RELATIVE_OFFSET_LOCAL_FILE_HEADER[1] << 8) + (m_vCENTRAL_DIRECTORY_FILE_HEADER[dwFileNumber].f.RELATIVE_OFFSET_LOCAL_FILE_HEADER[2] << 16) + (m_vCENTRAL_DIRECTORY_FILE_HEADER[dwFileNumber].f.RELATIVE_OFFSET_LOCAL_FILE_HEADER[3] << 24);

	// Reposition data pointer
	SetFilePointer(hZipFile, dwRelativeOffsetLocalFileHeader, NULL, FILE_BEGIN);

	// Open file for writing
	hFile = CreateFile(
		ToTString(wsFile).c_str(),
		GENERIC_WRITE,
		FILE_SHARE_READ,
		NULL,
		OPEN_EXISTING,
		FILE_ATTRIBUTE_NORMAL,
		NULL
	);

	if (hFile == INVALID_HANDLE_VALUE)
		return UNZIP_ERROR;

	// Compression method store
	if (wCompressionMethod == 0x00)
	{
		std::vector<BYTE> vData;

		if (dwCompressedSize != dwUncompressedSize)
		{
			CloseHandle(hFile);
			return UNZIP_ERROR;
		}

		// Copy file's data to vector
		vData.resize(dwCompressedSize);
		ReadFile(hZipFile, pbyData, 30, NULL, NULL);
		SetFilePointer(hZipFile, pbyData[26] + (pbyData[27] << 8) + pbyData[28] + (pbyData[29] << 8), NULL, FILE_CURRENT);
		ReadFile(hZipFile, vData.data(), dwCompressedSize, NULL, NULL);

		// Calculate and compare CRC32
		dwCRC32Compare = crc32(0L, Z_NULL, 0);
		dwCRC32Compare = crc32(dwCRC32Compare, vData.data(), dwUncompressedSize);

		if (dwCRC32Compare != dwCRC32)
		{
			CloseHandle(hFile);
			return UNZIP_ERROR;
		}

		WriteFile(hFile, vData.data(), dwUncompressedSize, &dwBytesWritten, NULL);
		CloseHandle(hFile);

		if (dwBytesWritten != dwUncompressedSize)
			return UNZIP_ERROR;
	}
	// Compression method deflate
	else if (wCompressionMethod == 0x08)
	{
		std::vector<BYTE> vCompressed;
		std::vector<BYTE> vUncompressed;

		// Copy file's data to vector
		vCompressed.resize(dwCompressedSize);
		ReadFile(hZipFile, pbyData, 30, NULL, NULL);
		SetFilePointer(hZipFile, pbyData[26] + (pbyData[27] << 8) + pbyData[28] + (pbyData[29] << 8), NULL, FILE_CURRENT);
		ReadFile(hZipFile, vCompressed.data(), dwCompressedSize, NULL, NULL);

		// Uncompress using inflate (RAW, -15)
		vUncompressed.resize(dwUncompressedSize);
		if (uncompressRAW(vUncompressed.data(), &dwUncompressedSize, vCompressed.data(), dwCompressedSize))
			return UNZIP_ERROR;

		// Calculate and compare CRC32
		dwCRC32Compare = crc32(0L, Z_NULL, 0);
		dwCRC32Compare = crc32(dwCRC32Compare, vUncompressed.data(), dwUncompressedSize);

		if (dwCRC32Compare != dwCRC32)
		{
			CloseHandle(hFile);
			return UNZIP_ERROR;
		}

		WriteFile(hFile, vUncompressed.data(), dwUncompressedSize, &dwBytesWritten, NULL);
		CloseHandle(hFile);

		if (dwBytesWritten != dwUncompressedSize)
			return UNZIP_ERROR;
	}
	// Compression method unhandled
	else
	{
		CloseHandle(hFile);
		return UNZIP_ERROR;
	}

	return UNZIP_SUCCESS;
}

/**
 * @brief	Update the file's time and date
 *
 * @author	Maxime Lagadec
 * @date	4/14/2018
 *
 * @param	[in] wsDirectory : Path to folder where to unzip
 * @param	[in] dwFileNumber : Number of the affected file stored in internal memory
 *
 * @return	SUCCESS : 0
 * @return	ERROR : 1
 *
 * @note	File's location must have been created previously (See CreateExtractFile)
 * @note	Ideally the file must already have been extracted (See ExtractFile)
 *
 */

DWORD cUNZIP::UpdateFileTimeDate(const std::wstring wsDirectory, const DWORD dwFileNumber)
{
	HANDLE hFile;

	FILETIME tFILETIME;
	SYSTEMTIME tSYSTEMTIME;

	std::wstring wsFile = ToWString((char *)m_vCENTRAL_DIRECTORY_FILE_HEADER[dwFileNumber].f.FILE_NAME);
	std::replace(wsFile.begin(), wsFile.end(), L'/', L'\\');

	wsFile.insert(0, wsDirectory);

	// Open file for writing
	hFile = CreateFile(
		ToTString(wsFile).c_str(),
		GENERIC_WRITE,
		FILE_SHARE_READ | FILE_SHARE_WRITE,
		NULL,
		OPEN_EXISTING,
		FILE_FLAG_BACKUP_SEMANTICS,
		NULL
	);

	if (hFile == INVALID_HANDLE_VALUE)
		return UNZIP_ERROR;

	// Gather file's information
	WORD wFileLastModificationTime = m_vCENTRAL_DIRECTORY_FILE_HEADER[dwFileNumber].f.FILE_LAST_MODIFICATION_TIME[0] + (m_vCENTRAL_DIRECTORY_FILE_HEADER[dwFileNumber].f.FILE_LAST_MODIFICATION_TIME[1] << 8);
	WORD wFileLastModificationDate = m_vCENTRAL_DIRECTORY_FILE_HEADER[dwFileNumber].f.FILE_LAST_MODIFICATION_DATE[0] + (m_vCENTRAL_DIRECTORY_FILE_HEADER[dwFileNumber].f.FILE_LAST_MODIFICATION_DATE[1] << 8);

	// Update tSYSTEMTIME
	tSYSTEMTIME.wYear = ((wFileLastModificationDate >> 9) & 0x7F) + 1980;
	tSYSTEMTIME.wMonth = (wFileLastModificationDate >> 5) & 0x0F;
	tSYSTEMTIME.wDay = wFileLastModificationDate & 0x1F;
	tSYSTEMTIME.wDayOfWeek = 0;
	tSYSTEMTIME.wHour = (wFileLastModificationTime >> 11) & 0x1F;
	tSYSTEMTIME.wMinute = (wFileLastModificationTime >> 5) & 0x3F;
	tSYSTEMTIME.wSecond = (wFileLastModificationTime & 0x1F) << 1;
	tSYSTEMTIME.wMilliseconds = 0;

	// Update file time
	SystemTimeToFileTime(&tSYSTEMTIME, &tFILETIME);
	SetFileTime(hFile, &tFILETIME, &tFILETIME, &tFILETIME);

	CloseHandle(hFile);

	return UNZIP_SUCCESS;
}

/**
 * @brief	Create a file's root path
 *
 * @author	Maxime Lagadec
 * @date	4/14/2018
 *
 * @param	[in] wsFile : Path to the file which root path will be created
 *
 * @return	SUCCESS : 0
 * @return	ERROR : 1
 *
 */

DWORD cUNZIP::CreateRootPath(const std::wstring wsFile)
{
	// Try to create the path
	if (!CreateDirectory(ToTString(wsFile).substr(0, wsFile.rfind(L'\\')).c_str(), NULL))
	{
		DWORD dwLastError = GetLastError();

		// Path missing previous directories
		if (ERROR_PATH_NOT_FOUND == dwLastError)
		{
			// Create the missing directories
			for (std::wstring wsCopyFile = wsFile; !CreateDirectory(ToTString(wsFile).substr(0, wsFile.rfind(L'\\')).c_str(), NULL);)
			{
				// Directory should always have at least one backslash
				if ((wsCopyFile = wsCopyFile.substr(0, wsCopyFile.rfind(L'\\'))).rfind(L'\\') == std::wstring::npos)
					return UNZIP_ERROR;

				// If directory created reset path
				if (CreateDirectory(ToTString(wsCopyFile).c_str(), NULL))
					wsCopyFile = wsFile;
			}
		}
		// Unexpected error
		else if (ERROR_ALREADY_EXISTS != dwLastError)
			return UNZIP_ERROR;
	}

	return UNZIP_SUCCESS;
}

/**
 * @brief	Uncompress source buffer to destination buffer
 *
 * @author	Maxime Lagadec
 * @date	4/14/2018
 *
 * @param	[in,out] dest : Buffer that receives compressed data
 * @param	[in,out] destLen : Length of the destination buffer
 * @param	[in] source : Buffer to be compressed
 * @param	[in] sourceLen : Length of the source buffer
 *
 * @note	destLen gets updated with the actual size of the uncompression
 * @note	Uncompress is RAW (no zlib header) and uses inflate method
 *
 * @return	SUCCESS : 0
 * @return	ERROR : zlib's defined errors
 *
 */

int cUNZIP::uncompressRAW(Bytef *dest, uLongf *destLen, const Bytef *source, uLong sourceLen)
{
    z_stream stream;
    int err;

    stream.next_in = (Bytef*)source;
    stream.avail_in = (uInt)sourceLen;
    /* Check for source > 64K on 16-bit machine: */
    if ((uLong)stream.avail_in != sourceLen) return Z_BUF_ERROR;

    stream.next_out = dest;
    stream.avail_out = (uInt)*destLen;
    if ((uLong)stream.avail_out != *destLen) return Z_BUF_ERROR;

    stream.zalloc = (alloc_func)0;
    stream.zfree = (free_func)0;

    err = inflateInit2(&stream, -15);
    if (err != Z_OK) return err;

    err = inflate(&stream, Z_FINISH);
    if (err != Z_STREAM_END) {
        inflateEnd(&stream);
        if (err == Z_NEED_DICT || (err == Z_BUF_ERROR && stream.avail_in == 0))
            return Z_DATA_ERROR;
        return err;
    }
    *destLen = stream.total_out;

    err = inflateEnd(&stream);
    return err;
}