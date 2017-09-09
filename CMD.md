    ttyrec2mpeg [<options>] <infile>[.gz|.bz2] [<outfile>]

`<outfile>` defaults to `<infile>` with file extension changed to `.mpeg` (or
`.mp4`?).

Options:

- screen size
- `--encoding <enc>`, `-E`
- `--ibm` (= `--encoding cp437`)
- `--dec`
- `--start <>` — start at a given frame number, timestamp, or temporal offset
  from start
- `--end <>` — end at a given frame number, timestamp, or temporal offset from
  end
- `--font <???>`
- `--config <file>` — config file (YAML? INI?); supports defining the
  following:
    - foreground colors (normal & bold)
    - background colors
    - default colors
    - font
    - timestamp control
    - cursor color
    - type of cursor (block, bar, or underscore)
    - whether to blink the cursor?
- playback speed
- control of how bells are rendered?
    - pitch
    - duration
    - whether to flash the screen instead (and what that looks like)
- location & format (and font size?) of optional timestamp
- maximum wait between tty frames?
- `-v`, `--verbose` — Instead of showing a progress bar, print
  "Processing|Skipping frame N (N-N bytes, YYYY-MM-DD HH:MM:SS) ..." upon
  processing each frame

--------------------------------------------------------------------------------

    playttyrec <infile>[.gz|.bz2]  # Rethink name

Terminal interface for ttyrec playback with commands for the following:

- jumping to a given frame
- jumping to a given timestamp
- showing the current frame number, timestamp, and file offset
- going back a frame
- dumping the current screen to a file (with or without ANSI sequences)
- quitting
- jumping ahead/backwards a given number of frames
- jumping ahead/backwards a given amount of time
