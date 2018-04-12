#include "cUNZIP.h"
#include "cZIP.h"

int main()
{
	cZIP clZIP = cZIP();
	clZIP.ZipToFile("C:\\Projects\\KEK420", "C:\\Projects\\KEK420.zip");

	return 0;
}

