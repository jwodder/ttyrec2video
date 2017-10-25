from   collections import namedtuple
from   datetime    import datetime
from   functools   import partial
import struct

Frame = namedtuple('Frame', 'timestamp data index start end duration')

def read_ttyrec(fp, encoding=None, errors=None):
    prev = None
    for i, header in enumerate(iter(partial(fp.read, 12), b'')):
        sec, usec, size = struct.unpack('<3I', header)
        dt = datetime.fromtimestamp(sec).replace(microsecond=usec)
        data = fp.read(size)
        if len(data) < size:
            raise ValueError  ###
        if encoding is not None:
            data = data.decode(encoding, errors or 'strict')
        if prev is not None:
            yield prev._replace(duration=dt-prev.timestamp)
            prev_end = prev.end
        else:
            prev_end = 0
        prev = Frame(
            timestamp=dt,
            data=data,
            index=i,
            start=prev_end,
            end=prev_end + 12 + size,
            duration=None,
        )
    if prev is not None:
        yield prev

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
    return Frame(timestamp=dt, data=data, index=None, start=start, end=end,
                 duration=None)
