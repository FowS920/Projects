#include <windef.h>

typedef union
{
	BYTE v[540];
	struct
	{
		BYTE LOCAL_FILE_HEADER_SIGNATURE[4];	/**< Local file header signature = 0x04034b50 (read as a little - endian number) */
		BYTE VERSION_NEEDED_TO_EXTRACT[2];		/**< Version needed to extract(minimum) */
		BYTE GENERAL_PURPOSE_BIT_FLAG[2];		/**< General purpose bit flag */
		BYTE COMPRESSION_METHOD[2];				/**< Compression method */
		BYTE FILE_LAST_MODIFICATION_TIME[2];	/**< File last modification time */
		BYTE FILE_LAST_MODICATION_DATE[2];		/**< File last modification date */
		BYTE CRC32[4];							/**< CRC - 32 */
		BYTE COMPRESSED_SIZE[4];				/**< Compressed size */
		BYTE UNCOMPRESSED_SIZE[4];				/**< Uncompressed size */
		BYTE FILE_NAME_LENGTH[2];				/**< File name length (n) */
		BYTE EXTRA_FIELD_LENGTH[2]; 			/**< Extra field length (m) */
		BYTE FILE_NAME[255];					/**< File name (length n) */
		BYTE EXTRA_FIELD[255];					/**< Extra field (length m) */
	} f;
} LOCAL_FILE_HEADER, *PLOCAL_FILE_HEADER;

typedef union
{
	BYTE v[16];
	struct
	{
		BYTE DATA_DESCRIPTOR_SIGNATURE[4];	/**< Optional data descriptor signature = 0x08074b50 */
		BYTE CRC32[4];						/**< CRC - 32 */
		BYTE COMPRESSED_SIZE[4];			/**< Compressed size */
		BYTE UNCOMPRESSED_SIZE[4];			/**< Uncompressed size */
	} f;
} DATA_DESCRIPTOR, *PDATA_DESCRIPTOR;

typedef union
{
	BYTE v[811];
	struct
	{
		BYTE CENTRAL_DIRECTORY_FILE_HEADER_SIGNATURE[4];	/**< Central directory file header signature = 0x02014b50 */
		BYTE VERSION_MADE_BY[2];							/**< Version made by */
		BYTE VERSION_NEEDED_TO_EXTRACT[2];					/**< Version needed to extract (minimum) */
		BYTE GENERAL_PURPOSE_BIT_FLAG[2];					/**< General purpose bit flag */
		BYTE COMPRESSION_METHOD[2];							/**< Compression method */
		BYTE FILE_LAST_MODIFICATION_TIME[2];				/**< File last modification time */
		BYTE FILE_LAST_MODIFICATION_DATE[2];				/**< File last modification date */
		BYTE CRC32[4];										/**< CRC - 32 */
		BYTE COMPRESSED_SIZE[4];							/**< Compressed size */
		BYTE UNCOMPRESSED_SIZE[4];							/**< Uncompressed size */
		BYTE FILE_NAME_LENGTH[2];							/**< File name length(n) */
		BYTE EXTRA_FIELD_LENGTH[2];							/**< Extra field length(m) */
		BYTE FILE_COMMENT_LENGTH[2];						/**< File comment length(k) */
		BYTE DISK_NUMBER_WHERE_FILE_STARTS[2];				/**< Disk number where file starts */
		BYTE INTERNAL_FILE_ATTRIBUTES[2];					/**< Internal file attributes */
		BYTE EXTERNAL_FILE_ATTRIBUTES[4];					/**< External file attributes */
		BYTE RELATIVE_OFFSET_LOCAL_FILE_HEADER[4];			/**< Relative offset of local file header. This is the number of bytes between the start of the first disk on which the file occurs, and the start of the local file header. This allows software reading the central directory to locate the position of the file inside the ZIP file. */
		BYTE FILE_NAME[255];								/**< File name (length n) */
		BYTE EXTRA_FIELD[255];								/**< Extra field (length m) */
		BYTE FILE_COMMENT[255];								/**< File comment (length k) */
	} f;
} CENTRAL_DIRECTORY_FILE_HEADER, *PCENTRAL_DIRECTORY_FILE_HEADER;

typedef union
{
	BYTE v[277];
	struct
	{
		BYTE END_OF_CENTRAL_DIRECTORY_SIGNATURE[4];					/**< End of central directory signature = 0x06054b50 */
		BYTE NUMBER_OF_THIS_DISK[2];								/**< Number of this disk */
		BYTE DISK_WHERE_CENTRAL_DIRECTORY_STARTS[2];				/**< Disk where central directory starts */
		BYTE NUMBER_OF_CENTRAL_DIRECTORY_RECORDS_ON_THIS_DISK[2];	/**< Number of central directory records on this disk */
		BYTE TOTAL_NUMBER_OF_CENTRAL_DIRECTORY_RECORDS[2];			/**< Total number of central directory records */
		BYTE SIZE_OF_CENTRAL_DIRECTORY[4];							/**< Size of central directory (bytes) */
		BYTE OFFSET_OF_START_OF_CENTRAL_DIRECTORY[4];				/**< Offset of start of central directory, relative to start of archive	*/
		BYTE COMMENT_LENGTH[2];										/**< Comment length(n) */
		BYTE COMMENT[255];											/**< Comment (length n) */
	} f;
} END_OF_CENTRAL_DIRECTORY_RECORD, *PEND_OF_CENTRAL_DIRECTORY_RECORD;