- Handle the user not specifying any fonts
    - Use fontconfig to find fonts?
    - Bundle/autodownload some font?
        - <http://font.ubuntu.com>?
- Look into the "proper" default values to use with the Ubuntu font for font
  size, leading, and underline location
- Handle brief frames:
    - Always show the initial frame even if it lasts for less than 1/FPS?
    - Add special handling for frames that last for less than 1/FPS?
        - Blur them together with adjacent frames?
    - Give final frame a non-instant duration?
- Add docstrings
- Include an example ttyrec and video in the repository (and link to it from
  the README) ?
- Prohibit `-` as an infile or outfile name?
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
- Make `ScreenRenderer` return numpy arrays instead of PIL images?
- Rename `Frame` to something that doesn't conflict with the video meaning of
  the word?
- Try to speed up conversion of ttyrec frames with long durations
