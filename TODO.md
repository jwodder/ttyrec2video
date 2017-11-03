- Upgrade to pyte 0.7.0
    - Support underlines
- This currently requires `imageio ~= 2.1.2`, as version 2.2.0 can't take
  generators of frames.  Try to upgrade?
- Add a progress bar
- Increase the image dimensions so they're a multiple of `macro_block_size`
- Include cursor highlight
- Make `ScreenRenderer` return numpy arrays instead of PIL images?
- Always show the initial frame even if it lasts for less than 1/FPS?
- Add special handling for frames that last for less than 1/FPS?
- Support xterm ACS sequences
    - This may require changes to `pyte`
- Support all video output formats that `imageio` supports, not just MP4's?
- Rename `Frame` to something that doesn't conflict with the video meaning of
  the word?
- Write a README
- Handle the user not specifying any fonts
    - Use fontconfig to find fonts?
    - Bundle/autodownload some font?
        - <http://font.ubuntu.com>?
