'''
AssertWT
~~~~~~~~

Assert that a Python script is run in the Windows Terminal 'wt.exe' instead
of the standard 'conhost.exe' console.

    >>> import assertwt
    >>> assertwt.restart()

'''

import sys
import subprocess
import os
import platform


__version__ = '1.0.0'
__author__ = 'cuzi'
__email__ = 'cuzi@openmail.cc'
__source__ = 'https://github.com/cvzi/AssertWt/'
__license__ = '''
This is free and unencumbered software released into the public domain.

Anyone is free to copy, modify, publish, use, compile, sell, or
distribute this software, either in source code form or as a compiled
binary, for any purpose, commercial or non-commercial, and by any
means.

In jurisdictions that recognize copyright laws, the author or authors
of this software dedicate any and all copyright interest in the
software to the public domain. We make this dedication for the benefit
of the public at large and to the detriment of our heirs and
successors. We intend this dedication to be an overt act of
relinquishment in perpetuity of all present and future rights to this
software under copyright law.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.

For more information, please refer to <http://unlicense.org/>
'''


def ARGV(argv):
    '''
    Placeholder in args list that represents the original command line arguments
    '''
    return subprocess.list2cmdline(argv)


def CD(argv):
    '''
    Placeholder in args list that represents the current working directory
    '''
    return os.getcwd()


def restart(args=["wt", "-d", CD, "cmd", "/C", ARGV]):
    '''
    Restarts the script in the 'Windows Terminal' if it is available

    :param args: Choose how to run the script:

        CMD: ``["wt", "-d", assertwt.CD, "cmd", "/C", assertwt.ARGV]``

        CMD (no exit): ``["wt", "-d", assertwt.CD, "cmd", "/K", assertwt.ARGV]``

        Powershell: ``["wt", "-d", assertwt.CD, "powershell", "-NoExit", "-Command", assertwt.ARGV]``

        Powershell (no exit): ``["wt", "-d", assertwt.CD, "powershell", "-Command", assertwt.ARGV]``

    '''
    if platform.system() != 'Windows' or 'WT_SESSION' in os.environ or 'idlelib' in sys.modules:
        return

    import ctypes
    import ctypes.wintypes

    GetCommandLineW = ctypes.windll.kernel32.GetCommandLineW
    GetCommandLineW.restype = ctypes.wintypes.LPWSTR
    GetCommandLineW.argtypes = []

    CommandLineToArgvW = ctypes.windll.shell32.CommandLineToArgvW
    CommandLineToArgvW.restype = ctypes.POINTER(ctypes.wintypes.LPWSTR)
    CommandLineToArgvW.argtypes = [
        ctypes.wintypes.LPCWSTR, ctypes.POINTER(ctypes.c_int)]

    argn = ctypes.c_int()
    argv = CommandLineToArgvW(GetCommandLineW(), ctypes.byref(argn))[
        :argn.value]

    args = [arg(argv) if callable(arg) else arg for arg in args]

    try:
        subprocess.run(args, shell=True, check=True)
        exit(0)
    except subprocess.CalledProcessError as e:
        print("Failed to start Windows Terminal:")
        print(e)
        print("############################################")
        return


if __name__ == '__main__':
    restart()
