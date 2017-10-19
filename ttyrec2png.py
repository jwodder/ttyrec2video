#!/usr/bin/python3
import click
from   PIL         import Image, ImageDraw, ImageFont
import pyte
from   read_ttyrec import read_ttyrec

DEFAULT_BG = (0,0,0)

FONT_SIZE = 16
LINES = 24
COLUMNS = 80

# PIL.ImageFont objects; assumed to be monospaced and the same size:
FONT = ImageFont.truetype('data/fonts/unifont.ttf', size=FONT_SIZE)
BOLD_FONT = ImageFont.truetype('data/fonts/unifont.ttf', size=FONT_SIZE)

CWIDTH  = FONT.getsize('X')[0]
CHEIGHT = FONT_SIZE * 6 // 5

FG = {}
FG.update({
    v: (int(v[:2], 16), int(v[2:4], 16), int(v[4:], 16))
    for v in pyte.graphics.FG_BG_256
})
FG.update({
    v: FG[pyte.graphics.FG_BG_256[k-30]]
    for k,v in pyte.graphics.FG.items()
})
FG["default"] = (0xF4, 0xF4, 0xF4)

BG = {}
BG.update({
    v: (int(v[:2], 16), int(v[2:4], 16), int(v[4:], 16))
    for v in pyte.graphics.FG_BG_256
})
BG.update({
    v: BG[pyte.graphics.FG_BG_256[k-40]]
    for k,v in pyte.graphics.FG.items()
})
BG["default"] = DEFAULT_BG

def screen2png(screen, filename):
    img = Image.new('RGB', (COLUMNS * CWIDTH, LINES * CHEIGHT), DEFAULT_BG)
    draw = ImageDraw.Draw(img)
    for y in range(LINES):
        for x in range(COLUMNS):
            c = screen.buffer[y][x]
            fg = FG[c.fg]
            bg = BG[c.bg]
            if c.reverse:
                fg, bg = bg, fg
            #if c.underline:  # pyte 0.7.0?
            #    ???
            draw.rectangle(
                [x*CWIDTH, y*CHEIGHT, (x+1)*CWIDTH, (y+1)*CHEIGHT],
                fill=bg,
            )
            draw.text(
                (x*CWIDTH, y*CHEIGHT),
                c.data,
                fill=fg,
                font=BOLD_FONT if c.bold else FONT,
            )
    img.save(filename)

@click.command()
@click.option('-E', '--encoding', default='utf-8')
@click.option('-o', '--outfile', default='ttyrec.png')
@click.argument('ttyrec', type=click.File('rb'))
@click.argument('frame', type=int)
def main(ttyrec, frame, encoding, outfile):
    screen = pyte.Screen(COLUMNS, LINES)
    stream = pyte.Stream(screen)
    frames = read_ttyrec(ttyrec, encoding=encoding)
    for _ in range(frame):
        stream.feed(next(frames).data)
    screen2png(screen, outfile)

if __name__ == '__main__':
    main()
