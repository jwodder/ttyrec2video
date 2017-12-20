from pathlib               import Path
from click.testing         import CliRunner
from ttyrec2video.__main__ import main

DATA_DIR = Path(__file__).with_name('data')

def test_cli_info():
    pth = str(DATA_DIR / 'hello.ttyrec')
    r = CliRunner().invoke(main, ['--info', pth])
    assert r.exit_code == 0, r.output
    assert r.output == '''\
Reading {} ...
{{
    "duration": "0:00:42.065535",
    "duration_seconds": 42.065535,
    "update_qty": 3
}}
'''.format(pth)
