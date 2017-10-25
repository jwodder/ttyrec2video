#!/usr/bin/python3
from   bisect            import bisect_left
import click
import imageio
import numpy as np
from   PIL               import ImageFont
import pyte
from   lib.read_ttyrec   import read_ttyrec
from   lib.screen_imager import ScreenImager

@click.command()
@click.option('-E', '--encoding', default='utf-8')
@click.option('-o', '--outfile', default='ttyrec.mp4')
@click.option('--size', type=(int, int), default=(80, 24))
@click.argument('ttyrec', type=click.File('rb'))
def main(ttyrec, encoding, outfile, size):
    screen = pyte.Screen(*size)
    stream = pyte.Stream(screen)
    imgr = ScreenImager(
        font      = ImageFont.truetype('data/fonts/unifont.ttf', size=16),
        bold_font = ImageFont.truetype('data/fonts/unifont.ttf', size=16),
        font_size = 16,
        columns   = size[0],
        lines     = size[1],
    )
    frames = []
    frame_times = []
    start_time = None
    for ts, data, *_ in read_ttyrec(ttyrec, encoding=encoding):
        if start_time is None:
            start_time = ts
        stream.feed(data)
        # <https://stackoverflow.com/a/1095878/744178>:
        frames.append(np.asarray(imgr.render(screen)))
        frame_times.append((ts - start_time).total_seconds())
    assert len(frames) > 0  ###
    # Must be called before importing VideoClip:
    imageio.plugins.ffmpeg.download()
    from moviepy.editor import VideoClip
    vid = VideoClip(
        make_frame=lambda t: frames[bisect_left(frame_times, t)],
        duration=frame_times[-1],
    )
    vid.fps = 24
    vid.write_videofile(outfile, progress_bar=True)

if __name__ == '__main__':
    main()
