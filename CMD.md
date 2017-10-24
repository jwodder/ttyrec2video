    ttyrec2mp4 [<options>] <infile>[.gz|.bz2] [<outfile>]

`<outfile>` defaults to `<infile>` with file extension changed to `.mp4`

Support `<infile>` being an HTTP(S) URL

Options:

- screen size
- `--encoding <enc>`, `-E`
- `--ibm` (= `--encoding cp437`)
- `--dec`
- `--start <>` — start at a given frame number, timestamp, or temporal offset
  from start
- `--end <>` — end at a given frame number, timestamp, or temporal offset from
  end
- `--duration <>` — end at a given offset from `--start`; mutually exclusive
  with `--end`
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
    - whether to use bright colors for bold text
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
- handling of nulls in output?
- FPS

--------------------------------------------------------------------------------

    playttyrec <infile>[.gz|.bz2]  # Rethink name

Terminal interface for ttyrec playback with commands for the following:

- jumping to a given frame
- jumping to a given timestamp
- jumping ahead/backwards a given number of frames
- jumping ahead/backwards a given amount of time
- going back a frame
- showing the current frame number, timestamp, and file offset
- dumping the current screen to a file (with or without ANSI sequences)
- quitting
