from   datetime            import datetime, timedelta, timezone
from   pathlib             import Path
import pytest
from   ttyrec2video.reader import ShortTTYRecError, TTYUpdate, read_ttyrec

DATA_DIR = Path(__file__).with_name('data')

HELLO = [
    TTYUpdate(
        timestamp = datetime(2017, 12, 10, 21, 49, 33, tzinfo=timezone.utc),
        data      = b'Hello,',
        offset    = 0,
        duration  = timedelta(seconds=4, microseconds=256),
    ),
    TTYUpdate(
        timestamp = datetime(2017, 12, 10, 21, 49, 37, 256, tzinfo=timezone.utc),
        data      = b'\xE2\x80\x9CWorld\xE2\x80\x9D!\r\n',
        offset    = 18,
        duration  = timedelta(seconds=38, microseconds=65279),
    ),
    TTYUpdate(
        timestamp = datetime(2017, 12, 10, 21, 50, 15, 65535, tzinfo=timezone.utc),
        data      = b"How's it going?\r\n",
        offset    = 44,
        duration  = None,
    ),
]

def test_read_ttyrec_bytes():
    with (DATA_DIR / 'hello.ttyrec').open('rb') as fp:
        assert list(read_ttyrec(fp)) == HELLO

def test_read_ttyrec_utf8():
    with (DATA_DIR / 'hello.ttyrec').open('rb') as fp:
        assert list(read_ttyrec(fp, encoding='utf-8')) == [
            u._replace(data=u.data.decode('utf-8')) for u in HELLO
        ]

@pytest.mark.parametrize('encoding', [None, 'utf-8'])
def test_read_ttyrec_short(encoding):
    with (DATA_DIR / 'short.ttyrec').open('rb') as fp:
        with pytest.raises(
            ShortTTYRecError,
            match='ttyrec update at offset 18 ended prematurely;'
                  ' expected 14 bytes, got 6',
        ): list(read_ttyrec(fp, encoding=encoding))

@pytest.mark.parametrize('encoding', [None, 'utf-8'])
def test_read_ttyrec_empty(encoding):
    with (DATA_DIR / 'empty.ttyrec').open('rb') as fp:
        assert list(read_ttyrec(fp, encoding=encoding)) == []
