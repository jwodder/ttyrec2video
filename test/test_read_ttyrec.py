from datetime            import datetime, timedelta
from pathlib             import Path
from ttyrec2video.reader import TTYUpdate, read_ttyrec

DATA_DIR = Path(__file__).with_name('data')

HELLO = [
    TTYUpdate(
        timestamp = datetime(2017, 12, 10, 21, 49, 33),
        data      = b'Hello,',
        offset    = 0,
        duration  = timedelta(seconds=4, microseconds=256),
    ),
    TTYUpdate(
        timestamp = datetime(2017, 12, 10, 21, 49, 37, 256),
        data      = b'\xE2\x80\x9CWorld\xE2\x80\x9D!\r\n',
        offset    = 18,
        duration  = timedelta(seconds=38, microseconds=65279),
    ),
    TTYUpdate(
        timestamp = datetime(2017, 12, 10, 21, 50, 15, 65535),
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
