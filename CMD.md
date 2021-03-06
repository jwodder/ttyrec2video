    ttyrec2mp4 [<options>] <infile>[.gz|.bz2] [<outfile>]

`<outfile>` defaults to `<infile>` with file extension changed to `.mp4`

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
- `--font-size <int>`
- line height/interline spacing/leading
- `--config <file>` — config file (YAML? INI?); supports defining the
  following:
    - foreground colors
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
    - whether to show a bell symbol in the corner?
- location & format (and font size?) of optional timestamp
    - timezone to convert timestamp to?
    - timezone to assume input timestamps are in (default: UTC)
- maximum wait between tty frames?
- verbosity & quietness options
    - Instead of showing a progress bar, print "Processing|Skipping frame N
      (N-N bytes, YYYY-MM-DD HH:MM:SS) ..." upon processing each frame?
    - Show verbose ffmpeg progress?
- handling of nulls in output?
- FPS
- how long the final frame should be displayed for?
- height & thickness of underline
- Use `'strict'` Unicode error handling instead of `'replace'`?
- options for ffmpeg
- whether to show the cursor
