import attr
from   PIL import Image, ImageDraw
import pyte

DEFAULT_BG = (0,0,0)
CURSOR_BG  = (0x9A, 0x9A, 0x9A)

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


@attr.s
class ScreenRenderer:
    font_size = attr.ib()
    # Fonts must be PIL.ImageFont instances.  (No, `attrs` validators can't be
    # used to enforce this.)  They are also assumed to be monospaced and of
    # size `font_size`.
    font      = attr.ib()
    bold_font = attr.ib()
    lines     = attr.ib(default=24)
    columns   = attr.ib(default=80)

    def __attrs_post_init__(self):
        self.cwidth  = self.font.getsize('X')[0]
        self.cheight = self.font_size * 6 // 5
        self.ul_depth = self.font_size

    def render(self, screen: pyte.Screen, block_size=None) -> Image:
        width  = self.columns * self.cwidth
        height = self.lines * self.cheight
        img = Image.new('RGB', (width, height), DEFAULT_BG)
        draw = ImageDraw.Draw(img)
        for y in range(self.lines):
            cy = y * self.cheight
            for x in range(self.columns):
                cx = x * self.cwidth
                c = screen.buffer[y][x]
                fg = FG[c.fg]
                bg = CURSOR_BG if (x,y) == (screen.cursor.x, screen.cursor.y) \
                               else BG[c.bg]
                if c.reverse:
                    fg, bg = bg, fg
                draw.rectangle(
                    [cx, cy, cx + self.cwidth, cy + self.cheight],
                    fill=bg,
                )
                draw.text(
                    (cx, cy),
                    c.data,
                    fill=fg,
                    font=self.bold_font if c.bold else self.font,
                )
                if c.underscore:
                    draw.line(
                        [cx,               cy + self.ul_depth,
                         cx + self.cwidth, cy + self.ul_depth],
                        fill=fg,
                        width=1,  ### Should this be thicker when bold?
                    )
        if block_size is not None:
            wdiff = block_size - (width % block_size  or block_size)
            hdiff = block_size - (height % block_size or block_size)
            bigimg = Image.new(
                'RGB',
                (width + wdiff, height + hdiff),
                DEFAULT_BG,
            )
            bigimg.paste(img, (wdiff // 2, hdiff // 2))
            img = bigimg
        return img

    def render_frames(self, frames, fps: int, block_size=None):
        screen = pyte.Screen(self.columns, self.lines)
        stream = pyte.Stream(screen)
        # Disabling `use_utf8` is necessary for pyte to honor smacs and rmacs
        # sequences (and that's apparently the only thing it controls).  I have
        # yet to figure out why one would ever want to set `use_utf8` to
        # `True`.
        stream.use_utf8 = False
        microframes = 0
        for fr in frames:
            stream.feed(fr.data)
            img = self.render(screen, block_size=block_size)
            d = fr.duration
            if d is not None:
                frqty, microframes = divmod(
                    microframes + (
                        (d.days * 86400 + d.seconds) * 1000000 + d.microseconds
                    ) * fps,
                    1000000,
                )
                for _ in range(frqty):
                    yield img
            else:
                yield img
