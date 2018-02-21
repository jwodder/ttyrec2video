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
- Support writing output to stdout?
- Add an option for just creating PNGs of each screen update and leaving the
  animation to the user?

Terminal Features to Support
----------------------------
- different levels of cursor visibility
- bell
- dim
- strikethrough?
- italics? (The Ubuntu font has separate fonts for regular & bold italic
  monospace)
- blink?
- poor-man's "animation" via padding NULs in output

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
- Eliminate `TTYUpdate.offset`?
- Split off screen-rendering code into its own package, `pyte2image`?
- Split off ttyrec-reading and -manipulation code into its own package?
