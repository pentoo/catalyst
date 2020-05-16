import ctypes
import ctypes.util
import enum
import os

libc = ctypes.CDLL(ctypes.util.find_library('c'), use_errno=True)
libc.mount.argtypes = (ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_ulong, ctypes.c_char_p)
libc.umount.argtypes = (ctypes.c_char_p,)

class MS(enum.IntFlag):
    NONE = 0x0
    RDONLY = 0x1
    NOSUID = 0x2
    NODEV = 0x4
    NOEXEC = 0x8
    BIND = 0x1000

def mount(source: str, target: str, fs: str, flags: MS = MS.NONE, options: str = '') -> None:
    ret = libc.mount(source.encode(), target.encode(), fs.encode(), flags,
                     options.encode())
    if ret < 0:
        errno = ctypes.get_errno()
        raise OSError(errno,
                      f"Error mounting {source} ({fs}) on {target} with options"
                      f" {options}': {os.strerror(errno)}")

def umount(target: str) -> None:
    ret = libc.umount(target.encode())
    if ret < 0:
        errno = ctypes.get_errno()
        raise OSError(errno,
                      f"Error unmounting {target}': {os.strerror(errno)}")
