from   collections import namedtuple
from   datetime    import datetime
from   functools   import partial
import struct
import attr

Frame = namedtuple('Frame', 'timestamp data index start end duration')

def read_ttyrec(fp, encoding=None, errors=None):
    prev = None
    for i, header in enumerate(iter(partial(fp.read, 12), b'')):
        sec, usec, size = struct.unpack('<3I', header)
        dt = datetime.fromtimestamp(sec).replace(microsecond=usec)
        data = fp.read(size)
        if len(data) < size:
            raise ShortTTYRecError(
                offset   = prev.end if prev is not None else 0,
                expected = size,
                received = len(data),
            )
        if encoding is not None:
            data = data.decode(encoding, errors or 'strict')
        if prev is not None:
            yield prev._replace(duration=dt-prev.timestamp)
            prev_end = prev.end
        else:
            prev_end = 0
        prev = Frame(
            timestamp = dt,
            data      = data,
            index     = i,
            start     = prev_end,
            end       = prev_end + 12 + size,
            duration  = None,
        )
    if prev is not None:
        yield prev


@attr.s(repr=False)
class ShortTTYRecError(ValueError):
    offset   = attr.ib()
    expected = attr.ib()
    received = attr.ib()

    def __str__(self):
        return (
            'ttyrec frame at offset {0.offset} ended prematurely;'
            ' expected {0.expected} byte{1}, got {0.received}'.format(
                self,
                's' if self.expected != 1 else '',
            )
        )
