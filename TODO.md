- Handle the user not specifying any fonts
    - Use fontconfig to find fonts?
    - Bundle/autodownload some font?
        - <http://font.ubuntu.com>?
- Look into the "proper" default values to use with the Ubuntu font for font
  size, leading, and underline location
- Handle brief TTY updates:
    - Always show the initial update even if it lasts for less than 1/FPS?
    - Add special handling for updates that last for less than 1/FPS?
        - Blur them together with adjacent updates?
    - Give final update a non-instant duration?
- Add docstrings
- Add tests
- Include an example ttyrec and video in the repository (and link to it from
  the README) ?
- Try to force the output to always be generated with ffmpeg instead of
  imageio's other backends?
- Check that the outfile's file extension is a supported format before scanning
  the ttyrec?

Terminal Features to Support
----------------------------
- different levels of cursor visibility
- bell
- dim
- strikethrough?
- italics?
- blink?

Coding Changes
--------------
- This currently requires `imageio ~= 2.1.2`, as version 2.2.0 can't take
  generators of frames.  Try to upgrade?
    - Solution: Give the generator passed to `mimwrite()` a `__len__`?
      Cf. <https://git.io/vbtCs>
    - Alternatively, just wait for
      <https://github.com/imageio/imageio/issues/295> to be fixed before
      upgrading
- Make `ScreenRenderer` return numpy arrays instead of PIL images?
- Try to speed up conversion of ttyrec updates with long durations
- Replace the `start` and `end` attributes of `TTYUpdate` with just a single
  `offset` attribute
- Eliminate `TTYUpdate.index`?
- Split off screen-rendering code into its own package, `pyte2image`?
