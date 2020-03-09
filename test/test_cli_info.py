from   pathlib               import Path
import re
from   click.testing         import CliRunner
from   ttyrec2video.__main__ import main

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

def test_cli_info_empty():
    pth = str(DATA_DIR / 'empty.ttyrec')
    r = CliRunner().invoke(main, ['--info', pth])
    assert r.exit_code == 0, r.output
    assert r.output == '''\
Reading {} ...
{{
    "duration": null,
    "duration_seconds": null,
    "update_qty": 0
}}
'''.format(pth)

def test_cli_info_short():
    pth = str(DATA_DIR / 'short.ttyrec')
    r = CliRunner().invoke(main, ['--info', pth])
    assert r.exit_code != 0
    stdout_lines = r.output.splitlines()
    assert len(stdout_lines) == 5, r.output
    assert stdout_lines[0] == 'Reading {} ...'.format(pth)
    assert stdout_lines[1] == 'Usage: ttyrec2video [OPTIONS] TTYREC [OUTFILE]'
    assert re.match(
        r'^Try [\'"]ttyrec2video -h[\'"] for help\.$',
        stdout_lines[2],
    )
    assert stdout_lines[3] == ''
    assert stdout_lines[4] \
        == 'Error: ttyrec update at offset 18 ended prematurely;'\
           ' expected 14 bytes, got 6'
