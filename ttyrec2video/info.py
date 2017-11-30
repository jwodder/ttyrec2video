from   datetime     import timezone
import json
from   textwrap     import indent
import click
from   .            import __version__
from   .read_ttyrec import read_ttyrec

def set_ibm_encoding(ctx, param, value):
    if value:
        ctx.params['encoding'] = 'cp437'

@click.command(context_settings={"help_option_names": ["-h", "--help"]})
@click.option('-E', '--encoding', default='utf-8', show_default=True,
              help='Character encoding of ttyrec files')
@click.option('--ibm', callback=set_ibm_encoding, expose_value=False,
              help='Synonym for "--encoding cp437"')
@click.option('-F', '--list-frames', is_flag=True)
@click.version_option(__version__, '-V', '--version',
                      message='ttyrec2video %(version)s')
@click.argument('ttyrec', type=click.File('rb'), nargs=-1)
@click.pass_context
def main(ctx, ttyrec, encoding, list_frames):
    first = True
    ok = True
    click.echo('[', nl=False)
    for fp in ttyrec:
        frames = read_ttyrec(fp, encoding=encoding)
        try:
            about = ttyrec_info(fp.name, frames, list_frames=list_frames)
        except UnicodeDecodeError as e:
            click.echo(
                '{}: {}: {}'.format(ctx.command_path, fp.name, e),
                err=True,
            )
            ok = False
        else:
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
    ctx.exit(0 if ok else 1)

def ttyrec_info(filename, frames, list_frames=False):
    framedata = []
    start_time = None
    last = None
    for fr in frames:
        if start_time is None:
            start_time = fr.timestamp
        last = fr
        if list_frames:
            framedata.append({
                "frameno": fr.index,
                "offset": fr.start,
                "timestamp_iso8601": fr.timestamp.isoformat(),
                "timestamp_unix": fr.timestamp.replace(tzinfo=timezone.utc)
                                              .timestamp(),
            })
    about = {"filename": filename}
    if last is not None:
        about["frame_qty"] = last.index + 1
        duration = last.timestamp - start_time
        about["duration"] = str(duration)
        about["duration_seconds"] = duration.total_seconds()
    else:
        about["frame_qty"] = 0
        about["duration"] = None
        about["duration_seconds"] = None
    if list_frames:
        about["frames"] = framedata
    return about

if __name__ == '__main__':
    main()
