- This currently requires `imageio ~= 2.1.2`, as version 2.2.0 can't take
  generators of frames.  Try to upgrade?
- Add a progress bar
- Make `ScreenRenderer` return numpy arrays instead of PIL images?
- Always show the initial frame even if it lasts for less than 1/FPS?
- Add special handling for frames that last for less than 1/FPS?
- Support all video output formats that `imageio` supports, not just MP4's?
- Rename `Frame` to something that doesn't conflict with the video meaning of
  the word?
- Write a README
- Handle the user not specifying any fonts
    - Use fontconfig to find fonts?
    - Bundle/autodownload some font?
        - <http://font.ubuntu.com>?

Terminal Features to Support
----------------------------
- Underlines
- xterm/non-VT100 `smacs` and `rmacs` sequences
    - This may require changes to `pyte`
- Different levels of cursor visibility
