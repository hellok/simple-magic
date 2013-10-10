###  simple a wrapper around the libmagic file identification library

http://swoolley.org/man.cgi/3/libmagic

Usage:
    
    >>> import simple_magic
    >>> filename="/opt/local/lib/libmagic.1.dylib"
    >>> cookie=simple_magic.open()
    >>> simple_magic.load(cookie)
    0
    >>> simple_magic.file(cookie,filename)
    'application/octet-stream'
    
    also:
    
    mime = subprocess.Popen("/usr/bin/file --mime PATH", shell=True,stdout=subprocess.PIPE).communicate()[0]            