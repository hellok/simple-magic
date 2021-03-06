"""
    simple a wrapper around the libmagic file identification library.
    
    See README for more information.
    
    Usage:
    
    >>> import simple_magic
    >>> filename="/opt/local/lib/libmagic.1.dylib"
    >>> cookie=simple_magic.open()
    >>> simple_magic.load(cookie)
    0
    >>> simple_magic.file(cookie,filename)
    'application/octet-stream'
    >>>
    
    """

import os.path
import ctypes
import ctypes.util

from ctypes import c_char_p, c_int, c_size_t, c_void_p

libmagic = ctypes.CDLL(ctypes.util.find_library('magic'))
if not libmagic._name:
    import sys
    if sys.platform == "darwin":
        # try mac ports location
        libmagic = ctypes.CDLL('/opt/local/lib/libmagic.dylib')
if not libmagic._name:
    raise Exception('failed to find libmagic.  Check your installation')

magic_t = ctypes.c_void_p

def errorcheck(result, func, args):
    err = magic_error(args[0])
    if err is not None:
        raise MagicException(err)
    else:
        return result

magic_open = libmagic.magic_open
magic_open.restype = magic_t
magic_open.argtypes = [c_int]

magic_close = libmagic.magic_close
magic_close.restype = None
magic_close.argtypes = [magic_t]

magic_error = libmagic.magic_error
magic_error.restype = c_char_p
magic_error.argtypes = [magic_t]

magic_errno = libmagic.magic_errno
magic_errno.restype = c_int
magic_errno.argtypes = [magic_t]

magic_file = libmagic.magic_file
magic_file.restype = c_char_p
magic_file.argtypes = [magic_t, c_char_p]
magic_file.errcheck = errorcheck


_magic_buffer = libmagic.magic_buffer
_magic_buffer.restype = c_char_p
_magic_buffer.argtypes = [magic_t, c_void_p, c_size_t]
_magic_buffer.errcheck = errorcheck


def magic_buffer(cookie, buf):
    return _magic_buffer(cookie, buf, len(buf))


magic_load = libmagic.magic_load
magic_load.restype = c_int
magic_load.argtypes = [magic_t, c_char_p]
magic_load.errcheck = errorcheck

magic_setflags = libmagic.magic_setflags
magic_setflags.restype = c_int
magic_setflags.argtypes = [magic_t, c_int]

magic_check = libmagic.magic_check
magic_check.restype = c_int
magic_check.argtypes = [magic_t, c_char_p]

magic_compile = libmagic.magic_compile
magic_compile.restype = c_int
magic_compile.argtypes = [magic_t, c_char_p]



MAGIC_NONE = 0x000000 # No flags

MAGIC_DEBUG = 0x000001 # Turn on debugging

MAGIC_SYMLINK = 0x000002 # Follow symlinks

MAGIC_COMPRESS = 0x000004 # Check inside compressed files

MAGIC_DEVICES = 0x000008 # Look at the contents of devices

MAGIC_MIME = 0x000010 # Return a mime string

MAGIC_CONTINUE = 0x000020 # Return all matches

MAGIC_CHECK = 0x000040 # Print warnings to stderr

MAGIC_PRESERVE_ATIME = 0x000080 # Restore access time on exit

MAGIC_RAW = 0x000100 # Don't translate unprintable chars

MAGIC_ERROR = 0x000200 # Handle ENOENT etc as real errors

MAGIC_NO_CHECK_COMPRESS = 0x001000 # Don't check for compressed files

MAGIC_NO_CHECK_TAR = 0x002000 # Don't check for tar files

MAGIC_NO_CHECK_SOFT = 0x004000 # Don't check magic entries

MAGIC_NO_CHECK_APPTYPE = 0x008000 # Don't check application type

MAGIC_NO_CHECK_ELF = 0x010000 # Don't check for elf details

MAGIC_NO_CHECK_ASCII = 0x020000 # Don't check for ascii files

MAGIC_NO_CHECK_TROFF = 0x040000 # Don't check ascii/troff

MAGIC_NO_CHECK_FORTRAN = 0x080000 # Don't check ascii/fortran

MAGIC_NO_CHECK_TOKENS = 0x100000 # Don't check ascii/tokens

def open(type=MAGIC_MIME):
    return magic_open(type)
def load(magic):
    return magic_load(magic,None)
def file(cookie,filename):
    if not os.path.exists(filename):
        raise IOError("File does not exist: " + filename)
    return magic_file(cookie, filename)

