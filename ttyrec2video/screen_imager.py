import attr
from   PIL import Image, ImageDraw
import pyte

DEFAULT_BG = (0,0,0)

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
class ScreenImager:
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

    def render(self, screen: pyte.Screen) -> Image:
        img = Image.new(
            'RGB',
            (self.columns * self.cwidth, self.lines * self.cheight),
            DEFAULT_BG,
        )
        draw = ImageDraw.Draw(img)
        for y in range(self.lines):
            for x in range(self.columns):
                c = screen.buffer[y][x]
                fg = FG[c.fg]
                bg = BG[c.bg]
                if c.reverse:
                    fg, bg = bg, fg
                #if c.underline:  # pyte 0.7.0?
                #    ???
                draw.rectangle(
                    [ x    * self.cwidth,  y    * self.cheight,
                     (x+1) * self.cwidth, (y+1) * self.cheight],
                    fill=bg,
                )
                draw.text(
                    (x*self.cwidth, y*self.cheight),
                    c.data,
                    fill=fg,
                    font=self.bold_font if c.bold else self.font,
                )
        return img

    def slideshow(self, frames, fps: int):
        screen = pyte.Screen(self.columns, self.lines)
        stream = pyte.Stream(screen)
        microframes = 0
        for fr in frames:
            stream.feed(fr.data)
            img = self.render(screen)
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
