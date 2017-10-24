import attr
import pyte
from   .read_ttyrec import read_ttyrec

@attr.s
class TTYRec(object):
    # constructor is "private"
    frames = attr.ib()  # list of Frame objects
    clearpoints = attr.ib()
        # ordered tuple of indices of frames that clear the screen or switch
        # to/from the altscreen
        ### Changes in colors & attributes will also have to be recorded
    lines   = attr.ib()
    columns = attr.ib()
    frameno = attr.ib(default=0, init=False)

    def __attrs_post_init__(self):
        self.screen  = pyte.Screen(self.columns, self.lines)
        self._stream = pyte.Stream(screen)

    @classmethod
    def from_file(cls, fp, encoding='utf-8', errors='strict',
                           lines=24, columns=80):
        ???

    def goto_frame(self, i):
        ???

    def goto_timestamp(self, dt, round_later=False):
        ???

    def advance(self):
        self.frameno += 1
        data = self.frames[self.frameno].data
        self._stream.feed(data)
        # In case the caller wants to update the real screen efficiently:
        return data
