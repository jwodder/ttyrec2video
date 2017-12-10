from   collections import namedtuple
from   datetime    import datetime
from   functools   import partial
import struct
import attr

TTYUpdate = namedtuple('TTYUpdate', 'timestamp data offset duration')

def read_ttyrec(fp, encoding=None, errors=None):
    prev = None
    offset = 0
    for header in iter(partial(fp.read, 12), b''):
        sec, usec, size = struct.unpack('<3I', header)
        dt = datetime.fromtimestamp(sec).replace(microsecond=usec)
        data = fp.read(size)
        if len(data) < size:
            raise ShortTTYRecError(
                offset   = offset,
                expected = size,
                received = len(data),
            )
        if encoding is not None:
            data = data.decode(encoding, errors or 'strict')
        if prev is not None:
            yield prev._replace(duration=dt-prev.timestamp)
        prev = TTYUpdate(timestamp=dt, data=data, offset=offset, duration=None)
        offset += 12 + size
    if prev is not None:
        yield prev


@attr.s(repr=False)
class ShortTTYRecError(ValueError):
    offset   = attr.ib()
    expected = attr.ib()
    received = attr.ib()

    def __str__(self):
        return (
            'ttyrec update at offset {0.offset} ended prematurely;'
            ' expected {0.expected} byte{1}, got {0.received}'.format(
                self,
                's' if self.expected != 1 else '',
            )
        )
