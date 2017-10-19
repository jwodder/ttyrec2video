from   collections import namedtuple
from   datetime    import datetime
from   functools   import partial
import struct

Frame = namedtuple('Frame', 'timestamp data index start end')

def read_ttyrec(fp, encoding=None, errors=None):
    prev_end = 0
    for i, header in enumerate(iter(partial(fp.read, 12), b'')):
        sec, usec, size = struct.unpack('<3I', header)
        dt = datetime.fromtimestamp(sec).replace(microsecond=usec)
        data = fp.read(size)
        if len(data) < size:
            raise ValueError  ###
        if encoding is not None:
            data = data.decode(encoding, errors or 'strict')
        here = prev_end + 12 + size
        yield Frame(timestamp=dt, data=data, index=i, start=prev_end, end=here)
        prev_end = here

def read_frame(fp, encoding=None, errors=None):
    start = fp.tell() if fp.seekable() else None
    sec, usec, size = struct.unpack('<3I', fp.read(12))
    dt = datetime.fromtimestamp(sec).replace(microsecond=usec)
    data = fp.read(size)
    if len(data) < size:
        raise ValueError  ###
    if encoding is not None:
        data = data.decode(encoding, errors or 'strict')
    end = fp.tell() if fp.seekable() else None
    return Frame(timestamp=dt, data=data, index=None, start=start, end=end)
