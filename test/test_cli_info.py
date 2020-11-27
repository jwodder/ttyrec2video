from   pathlib               import Path
import click
from   click.testing         import CliRunner
from   ttyrec2video.__main__ import main

DATA_DIR = Path(__file__).with_name('data')

def test_cli_info():
    pth = str(DATA_DIR / 'hello.ttyrec')
    r = CliRunner().invoke(main, ['--info', pth])
    assert r.exit_code == 0, r.output
    assert r.output == f'''\
Reading {pth} ...
{{
    "duration": "0:00:42.065535",
    "duration_seconds": 42.065535,
    "update_qty": 3
}}
'''

def test_cli_info_empty():
    pth = str(DATA_DIR / 'empty.ttyrec')
    r = CliRunner().invoke(main, ['--info', pth])
    assert r.exit_code == 0, r.output
    assert r.output == f'''\
Reading {pth} ...
{{
    "duration": null,
    "duration_seconds": null,
    "update_qty": 0
}}
'''

def test_cli_info_short():
    pth = str(DATA_DIR / 'short.ttyrec')
    r = CliRunner().invoke(main, ['--info', pth], standalone_mode=False)
    assert r.exit_code != 0
    assert r.output == f'Reading {pth} ...\n'
    assert isinstance(r.exception, click.UsageError)
    assert str(r.exception) \
        == 'ttyrec update at offset 18 ended prematurely;'\
           ' expected 14 bytes, got 6'
