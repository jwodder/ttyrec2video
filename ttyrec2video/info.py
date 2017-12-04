from   datetime import timezone
import json
from   textwrap import indent
import click
from   .        import __version__
from   .reader  import read_ttyrec

@click.command(context_settings={"help_option_names": ["-h", "--help"]})
@click.option('-A', '--all', 'show_all', is_flag=True)
@click.version_option(__version__, '-V', '--version',
                      message='ttyrec2video %(version)s')
@click.argument('ttyrec', type=click.File('rb'), nargs=-1)
def main(ttyrec, show_all):
    first = True
    click.echo('[', nl=False)
    for fp in ttyrec:
        about = ttyrec_info(fp.name, read_ttyrec(fp), show_all=show_all)
        if first:
            click.echo()
            first = False
        else:
            click.echo(',')
        click.echo(
            indent(json.dumps(about, sort_keys=True, indent=4), ' '*4),
            nl=False,
        )
    if not first:
        click.echo()
    click.echo(']')

def ttyrec_info(filename, updates, show_all=False):
    update_data = []
    start_time = None
    last = None
    for fr in updates:
        if start_time is None:
            start_time = fr.timestamp
        last = fr
        if show_all:
            update_data.append({
                "index": fr.index,
                "offset": fr.start,
                "timestamp_iso8601": fr.timestamp.isoformat(),
                "timestamp_unix": fr.timestamp.replace(tzinfo=timezone.utc)
                                              .timestamp(),
            })
    about = {"filename": filename}
    if last is not None:
        about["update_qty"] = last.index + 1
        duration = last.timestamp - start_time
        about["duration"] = str(duration)
        about["duration_seconds"] = duration.total_seconds()
    else:
        about["update_qty"] = 0
        about["duration"] = None
        about["duration_seconds"] = None
    if show_all:
        about["updates"] = update_data
    return about

if __name__ == '__main__':
    main()
